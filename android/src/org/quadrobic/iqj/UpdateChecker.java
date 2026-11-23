package org.quadrobic.iqj;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.Uri;
import android.widget.Toast;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.function.Supplier;
import javax.net.ssl.HttpsURLConnection;
import org.json.JSONArray;
import org.json.JSONObject;

/** Foreground-only native metadata checks; no APK downloads or WebView networking. */
final class UpdateChecker {
    private static final String ENDPOINT =
        "https://api.github.com/repos/Quadrobic/Quadrobic.github.io/releases/latest";
    private static final long HOUR = 60 * 60 * 1000L;
    private final Activity activity;
    private final SharedPreferences preferences;
    private final Supplier<String> page;
    private final ConnectivityManager connectivity;
    private boolean active, checking, listening;
    private AlertDialog dialog;
    private Release pending;

    private static final class Release {
        final String version, url;
        Release(String version, String url) { this.version = version; this.url = url; }
    }

    UpdateChecker(Activity activity, SharedPreferences preferences, Supplier<String> page) {
        this.activity = activity;
        this.preferences = preferences;
        this.page = page;
        connectivity = activity.getSystemService(ConnectivityManager.class);
    }

    private final ConnectivityManager.NetworkCallback network = new ConnectivityManager.NetworkCallback() {
        @Override public void onCapabilitiesChanged(Network network, NetworkCapabilities capabilities) {
            if (capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_VALIDATED))
                activity.runOnUiThread(() -> check());
        }
    };

    void resume() {
        active = true;
        if (connectivity != null && !listening) {
            try {
                connectivity.registerDefaultNetworkCallback(network);
                listening = true;
            } catch (RuntimeException ignored) { /* A resume-time check still works. */ }
        }
        offer();
        check();
    }

    void pause() {
        active = false;
        if (listening) {
            connectivity.unregisterNetworkCallback(network);
            listening = false;
        }
        if (dialog != null) { dialog.dismiss(); dialog = null; }
    }

    private boolean online() {
        if (connectivity == null) return false;
        NetworkCapabilities caps = connectivity.getNetworkCapabilities(connectivity.getActiveNetwork());
        return caps != null && caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_VALIDATED);
    }

    private void check() {
        if (!active || checking || !online()) return;
        long now = System.currentTimeMillis();
        long next = preferences.getLong("updateNextCheck", 0);
        // Do not let a clock correction suppress checks indefinitely.
        if (next > now && next - now <= 12 * HOUR) return;
        checking = true;
        new Thread(() -> {
            Release result = null;
            boolean success = false;
            try {
                String installed = activity.getPackageManager()
                    .getPackageInfo(activity.getPackageName(), 0).versionName;
                JSONObject release = fetch();
                if (!release.getBoolean("draft") && !release.getBoolean("prerelease")) {
                    JSONArray assets = release.getJSONArray("assets");
                    for (int i = 0; i < assets.length(); i++) {
                        JSONObject asset = assets.getJSONObject(i);
                        if (!"uploaded".equals(asset.optString("state"))) continue;
                        String url = asset.optString("browser_download_url");
                        String version = ReleaseVersion.fromAsset(asset.optString("name"), url);
                        if (ReleaseVersion.newer(version, installed)
                                && (result == null || ReleaseVersion.newer(version, result.version)))
                            result = new Release(version, url);
                    }
                }
                success = true;
            } catch (Exception ignored) { /* Offline, rate-limited or invalid: keep reading quietly. */ }
            preferences.edit().putLong("updateNextCheck",
                System.currentTimeMillis() + (success ? 12 * HOUR : HOUR / 4)).apply();
            final Release found = result;
            activity.runOnUiThread(() -> {
                checking = false;
                pending = found;
                offer();
            });
        }, "iqj-updates").start();
    }

    private static JSONObject fetch() throws Exception {
        HttpsURLConnection connection = (HttpsURLConnection) new URL(ENDPOINT).openConnection();
        connection.setConnectTimeout(5000);
        connection.setReadTimeout(8000);
        connection.setInstanceFollowRedirects(false);
        connection.setRequestProperty("Accept", "application/vnd.github+json");
        connection.setRequestProperty("User-Agent", "Quadrobic-Android-Reader");
        connection.setRequestProperty("X-GitHub-Api-Version", "2022-11-28");
        try {
            if (connection.getResponseCode() != 200) throw new java.io.IOException("Release unavailable");
            try (InputStream input = connection.getInputStream();
                 ByteArrayOutputStream output = new ByteArrayOutputStream()) {
                byte[] buffer = new byte[8192];
                int count;
                while ((count = input.read(buffer)) != -1) {
                    if (output.size() + count > 1024 * 1024) throw new java.io.IOException("Release too large");
                    output.write(buffer, 0, count);
                }
                return new JSONObject(new String(output.toByteArray(), StandardCharsets.UTF_8));
            }
        } finally { connection.disconnect(); }
    }

    private void offer() {
        if (!active || pending == null || dialog != null || activity.isFinishing() || activity.isDestroyed()) return;
        Release release = pending;
        long now = System.currentTimeMillis();
        long offered = preferences.getLong("updateOfferedAt", 0);
        if (release.version.equals(preferences.getString("updateOfferedVersion", ""))
                && now >= offered && now - offered < 24 * HOUR) return;
        String url = page.get();
        boolean ru = url != null && !url.contains(".en.html") && !url.contains(".th.html");
        boolean th = url != null && url.contains(".th.html");
        String title = th ? "มีเวอร์ชันใหม่" : ru ? "Доступно обновление" : "Update available";
        String body = th ? "Quadrobic " + release.version + "\nดาวน์โหลด APK ผ่านเบราว์เซอร์ แล้วติดตั้งทับแอปเดิม ตำแหน่งอ่านจะยังอยู่"
            : ru ? "Quadrobic " + release.version + "\nСкачать APK через браузер и установить поверх приложения? Место чтения сохранится."
            : "Quadrobic " + release.version + "\nDownload the APK in your browser and install it over this app? Your reading position will be kept.";
        dialog = new AlertDialog.Builder(activity)
            .setTitle(title).setMessage(body)
            .setNegativeButton(th ? "ภายหลัง" : ru ? "Позже" : "Later", (d, which) -> {})
            .setPositiveButton(th ? "ดาวน์โหลด" : ru ? "Скачать" : "Download", (d, which) -> {
                try {
                    activity.startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(release.url))
                        .addCategory(Intent.CATEGORY_BROWSABLE));
                } catch (ActivityNotFoundException error) {
                    Toast.makeText(activity, ru ? "Не найден браузер" : "No browser installed", Toast.LENGTH_LONG).show();
                }
            }).create();
        dialog.setOnDismissListener(d -> dialog = null);
        dialog.show();
        preferences.edit().putString("updateOfferedVersion", release.version)
            .putLong("updateOfferedAt", now).apply();
    }
}
