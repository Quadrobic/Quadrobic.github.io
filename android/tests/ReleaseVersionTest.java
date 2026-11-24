package org.quadrobic.iqj;

/** Runs on the host JVM: release metadata must never offer an older or foreign APK. */
public final class ReleaseVersionTest {
    private static void require(boolean condition) {
        if (!condition) throw new AssertionError("Unexpected release eligibility");
    }

    public static void main(String[] args) {
        String version = "2026.11.23.10";
        String name = "quadrobic-" + version + ".apk";
        String root = "https://github.com/Quadrobic/Quadrobic.github.io/releases/download/";
        String url = root + version + "/" + name;
        require(version.equals(ReleaseVersion.fromAsset(name, url)));
        require(version.equals(ReleaseVersion.fromAsset(name, root + "v" + version + "/" + name)));
        require(ReleaseVersion.newer(version, "2026.11.18.9"));
        require(!ReleaseVersion.newer(version, version));
        require(!ReleaseVersion.newer("2026.12.01.8", version));
        require(ReleaseVersion.newer("2026.11.22.11", version));
        String published = "2026.11.24.13";
        String apk = "quadrobic-" + published + ".apk";
        require(published.equals(ReleaseVersion.fromAsset(apk, root + published + "/" + apk)));
        require(ReleaseVersion.newer(published, "2026.11.24.12"));
        for (String invalid : new String[] {
                null, "", "preview", "2026.11.23", "2026.11.23.10-beta", "2026.0.23.11",
                "2026.11.32.11", "2026.11.23.0", "2026.11.23.9999999999" }) {
            require(!ReleaseVersion.newer(invalid, version));
            require(!ReleaseVersion.newer(version, invalid));
        }
        for (String foreign : new String[] {
                url.replace("https:", "http:"), url.replace("github.com", "github.com.evil.example"),
                url.replace("github.com", "evil.example@github.com"),
                url.replace("github.com", "github.com:443"),
                url.replace("/Quadrobic/", "/AnotherOwner/"),
                root + "2026.11.18.9/" + name, url + "?redirect=elsewhere", url + "#fragment",
                url.replace("/releases/", "/%72eleases/"), url.replace("/download/", "/download/../") })
            require(ReleaseVersion.fromAsset(name, foreign) == null);
        require(ReleaseVersion.fromAsset("other.apk", url) == null);
        require(ReleaseVersion.fromAsset(name, null) == null);
        require(ReleaseVersion.fromAsset(name, url.replace(name, "different.apk")) == null);
        System.out.println("PASS: APK identity, release paths, numeric version codes and downgrade rejection");
    }
}
