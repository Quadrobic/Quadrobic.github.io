package org.quadrobic.iqj;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.regex.Pattern;

/** Release filenames and versionName share the builder's YYYY.MM.DD.counter format. */
final class ReleaseVersion {
    private static final Pattern VERSION = Pattern.compile("[0-9]{4}\\.[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{1,10}");

    private static long[] parts(String version) {
        if (version == null || !VERSION.matcher(version).matches()) return null;
        String[] pieces = version.split("\\.");
        long[] result = new long[4];
        for (int i = 0; i < 4; i++) result[i] = Long.parseLong(pieces[i]);
        if (result[1] < 1 || result[1] > 12 || result[2] < 1 || result[2] > 31
                || result[3] < 1 || result[3] > 2100000000L) return null;
        return result;
    }

    static boolean newer(String candidate, String installed) {
        long[] next = parts(candidate), current = parts(installed);
        if (next == null || current == null) return false;
        // Android refuses downgrades even if a date in the release name is newer.
        return next[3] > current[3];
    }

    static String fromAsset(String name, String downloadUrl) {
        if (name == null || !name.startsWith("quadrobic-") || !name.endsWith(".apk")) return null;
        String version = name.substring(10, name.length() - 4);
        if (parts(version) == null || downloadUrl == null) return null;
        try {
            URI uri = new URI(downloadUrl);
            if (!"https".equals(uri.getScheme()) || !"github.com".equals(uri.getHost())
                    || uri.getPort() != -1 || uri.getUserInfo() != null
                    || uri.getQuery() != null || uri.getFragment() != null) return null;
            String prefix = "/Quadrobic/Quadrobic.github.io/releases/download/";
            String path = uri.getRawPath();
            if (path == null || !path.startsWith(prefix)) return null;
            String[] tail = path.substring(prefix.length()).split("/", -1);
            if (tail.length != 2 || !tail[1].equals(name)
                    || !(tail[0].equals(version) || tail[0].equals("v" + version))) return null;
            return version;
        } catch (URISyntaxException error) {
            return null;
        }
    }
}
