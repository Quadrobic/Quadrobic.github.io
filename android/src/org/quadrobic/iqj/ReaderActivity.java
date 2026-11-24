package org.quadrobic.iqj;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.WindowInsets;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.Toast;
import android.window.OnBackInvokedCallback;
import android.window.OnBackInvokedDispatcher;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

/** One stable HTTPS origin backed solely by packaged assets, with no JS bridge. */
public final class ReaderActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String HOME = "https://" + HOST + "/site/index.html";
    private static final int SAVE_FILE = 40;
    private WebView reader;
    private SharedPreferences preferences;
    private String pendingAsset;
    private boolean restoreReading;
    private UpdateChecker updates;
    private PageTransition transition;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        restoreReading = state != null;
        preferences = getSharedPreferences("reader", MODE_PRIVATE);
        updates = new UpdateChecker(this, preferences, () -> reader.getUrl());
        if (Build.VERSION.SDK_INT >= 30) getWindow().setDecorFitsSystemWindows(false);
        else getWindow().getDecorView().setSystemUiVisibility(
            android.view.View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | android.view.View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | android.view.View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
        FrameLayout frame = new FrameLayout(this);
        frame.setBackgroundColor(Color.rgb(16, 13, 10));
        reader = new WebView(this);
        reader.setBackgroundColor(Color.rgb(16, 13, 10));
        frame.addView(reader, new FrameLayout.LayoutParams(-1, -1));
        transition = new PageTransition(reader, frame);
        // Android 15 enforces edge-to-edge for target 35. Keep controls clear
        // of system bars and display cutouts without changing the site's CSS.
        frame.setOnApplyWindowInsetsListener((view, insets) -> {
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets safe = insets.getInsets(
                    WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                view.setPadding(safe.left, safe.top, safe.right, safe.bottom);
            } else {
                view.setPadding(insets.getSystemWindowInsetLeft(), insets.getSystemWindowInsetTop(),
                    insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom());
            }
            return insets;
        });
        setContentView(frame);
        frame.requestApplyInsets();

        WebSettings settings = reader.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setSupportMultipleWindows(false);
        reader.setWebViewClient(new LocalClient());
        reader.setDownloadListener((url, agent, disposition, mime, length) -> export(Uri.parse(url)));

        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(
                OnBackInvokedDispatcher.PRIORITY_DEFAULT,
                new OnBackInvokedCallback() {
                    @Override public void onBackInvoked() { back(); }
                });
        }
        if (state != null) pendingAsset = state.getString("pendingAsset");
        if (state == null || reader.restoreState(state) == null) {
            String last = preferences.getString("lastUrl", HOME);
            reader.loadUrl(localPath(Uri.parse(last)) != null && isPage(last) ? last : HOME);
        }
    }

    private static boolean isPage(String url) {
        String path = Uri.parse(url).getPath();
        return path != null && path.endsWith(".html") && !path.startsWith("/site/agda/");
    }

    private static boolean sameDocument(String first, String second) {
        return first != null && second != null
            && Uri.parse(first).buildUpon().fragment(null).build()
                .equals(Uri.parse(second).buildUpon().fragment(null).build());
    }

    /** Uri.getPath decodes once; reject separators and traversal before AssetManager. */
    private static String localPath(Uri uri) {
        if (!"https".equals(uri.getScheme()) || !HOST.equals(uri.getHost())
                || uri.getPort() != -1 || uri.getUserInfo() != null) return null;
        String path = uri.getPath();
        if (path == null || !path.startsWith("/site/")) return null;
        String relative = path.substring(6);
        if (relative.isEmpty() || relative.contains("\\") || relative.contains("%")
                || relative.indexOf('\0') >= 0) return null;
        for (String part : relative.split("/")) {
            if (part.equals("..") || part.equals(".") || part.isEmpty()) return null;
        }
        return "site/" + relative;
    }

    private static String mime(String path) {
        String p = path.toLowerCase(Locale.ROOT);
        if (p.endsWith(".html")) return "text/html";
        if (p.endsWith(".css")) return "text/css";
        if (p.endsWith(".js")) return "text/javascript";
        if (p.endsWith(".json")) return "application/json";
        if (p.endsWith(".svg")) return "image/svg+xml";
        if (p.endsWith(".png")) return "image/png";
        if (p.endsWith(".jpg") || p.endsWith(".jpeg")) return "image/jpeg";
        if (p.endsWith(".mp3")) return "audio/mpeg";
        if (p.endsWith(".woff2")) return "font/woff2";
        if (p.endsWith(".pdf")) return "application/pdf";
        if (p.endsWith(".zip")) return "application/zip";
        return "text/plain";
    }

    private static WebResourceResponse empty(int status, String reason) {
        return new WebResourceResponse("text/plain", "UTF-8", status, reason,
            new HashMap<String, String>(), new ByteArrayInputStream(new byte[0]));
    }

    private final class LocalClient extends WebViewClient {
        @Override public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
            transition.started();
        }

        @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            String path = localPath(request.getUrl());
            if (path == null || !"GET".equals(request.getMethod())) return empty(403, "Offline");
            try {
                String type = mime(path);
                Map<String, String> headers = new HashMap<>();
                headers.put("Cache-Control", "no-store");
                headers.put("X-Content-Type-Options", "nosniff");
                return new WebResourceResponse(type,
                    type.startsWith("text/") || type.equals("application/json") ? "UTF-8" : null,
                    200, "OK", headers, getAssets().open(path));
            } catch (IOException error) {
                return empty(404, "Not Found");
            }
        }

        @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            String path = localPath(uri);
            if (path != null && isPage(uri.toString())) {
                // Same-document anchors must not wait for a page-load callback.
                if (request.isForMainFrame() && !sameDocument(view.getUrl(), uri.toString())) transition.capture();
                return false;
            }
            if (path != null) {
                if (request.hasGesture()) export(uri);
                return true;
            }
            String scheme = uri.getScheme();
            if (request.isForMainFrame() && request.hasGesture()
                    && ("https".equals(scheme) || "http".equals(scheme))) {
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, uri).addCategory(Intent.CATEGORY_BROWSABLE));
                } catch (ActivityNotFoundException error) {
                    message("Не найден браузер / No browser installed");
                }
            }
            return true;
        }

        @Override public void onPageFinished(WebView view, String url) {
            if (localPath(Uri.parse(url)) != null && isPage(url)) {
                preferences.edit().putString("lastUrl", Uri.parse(url).buildUpon().fragment(null).build().toString()).apply();
                if (restoreReading) {
                    view.evaluateJavascript("window.dispatchEvent(new Event('iqj:resume'));", null);
                    restoreReading = false;
                }
                transition.ready();
            }
        }
    }

    private void export(Uri uri) {
        String path = localPath(uri);
        if (path == null || pendingAsset != null) return;
        pendingAsset = path;
        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(mime(path));
        intent.putExtra(Intent.EXTRA_TITLE, path.substring(path.lastIndexOf('/') + 1));
        try {
            startActivityForResult(intent, SAVE_FILE);
        } catch (ActivityNotFoundException error) {
            pendingAsset = null;
            message("Не найдено приложение для сохранения / No document picker installed");
        }
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request != SAVE_FILE) return;
        String path = pendingAsset;
        pendingAsset = null;
        if (result != RESULT_OK || data == null || data.getData() == null || path == null) return;
        final Uri target = data.getData();
        new Thread(() -> {
            try (InputStream input = getAssets().open(path);
                 OutputStream output = getContentResolver().openOutputStream(target)) {
                if (output == null) throw new IOException("No output stream");
                byte[] buffer = new byte[32768];
                int count;
                while ((count = input.read(buffer)) != -1) output.write(buffer, 0, count);
                runOnUiThread(() -> message("Сохранено / Saved"));
            } catch (IOException error) {
                runOnUiThread(() -> message("Не удалось сохранить / Could not save"));
            }
        }, "iqj-export").start();
    }

    private void message(String value) { Toast.makeText(this, value, Toast.LENGTH_LONG).show(); }
    private void back() {
        reader.evaluateJavascript("(function(){window.dispatchEvent(new Event('iqj:save'));"
            + "var overlay=document.querySelector('.mobile-sheet.open, #mobile-sheet.open,"
            + " #model-panel:not([hidden]), #term-tooltip:not([hidden])');"
            + "if(overlay){document.dispatchEvent(new KeyboardEvent('keydown',"
            + "{key:'Escape',code:'Escape',bubbles:true}));return true;}return false;})()", handled -> {
                if (!"true".equals(handled)) {
                    if (reader.canGoBack()) {
                        // History may contain anchors: capture only document changes.
                        android.webkit.WebBackForwardList history = reader.copyBackForwardList();
                        android.webkit.WebHistoryItem previous = history.getItemAtIndex(history.getCurrentIndex() - 1);
                        if (previous != null && !sameDocument(previous.getUrl(), reader.getUrl())) transition.capture();
                        reader.goBack();
                    } else finish();
                }
            });
    }
    @Override public void onBackPressed() { back(); }

    @Override protected void onSaveInstanceState(Bundle state) {
        reader.saveState(state);
        state.putString("pendingAsset", pendingAsset);
        super.onSaveInstanceState(state);
    }
    @Override protected void onPause() {
        updates.pause();
        String url = reader.getUrl();
        if (url != null && localPath(Uri.parse(url)) != null && isPage(url)) {
            preferences.edit().putString("lastUrl", Uri.parse(url).buildUpon().fragment(null).build().toString()).apply();
        }
        reader.evaluateJavascript("window.dispatchEvent(new Event('iqj:save'));"
            + "document.querySelectorAll('audio').forEach(a=>a.pause());", null);
        reader.onPause();
        super.onPause();
    }
    @Override protected void onResume() {
        super.onResume();
        if (reader != null) reader.onResume();
        updates.resume();
    }
    @Override protected void onDestroy() {
        if (transition != null) transition.destroy();
        if (reader != null) { reader.stopLoading(); reader.destroy(); }
        super.onDestroy();
    }
}
