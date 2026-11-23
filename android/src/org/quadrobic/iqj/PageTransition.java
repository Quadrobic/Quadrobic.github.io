package org.quadrobic.iqj;

import android.animation.ValueAnimator;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.view.View;
import android.webkit.WebView;
import android.widget.FrameLayout;
import android.widget.ImageView;

/** Keep the previous frame until fonts, reading position and WebView paint agree. */
final class PageTransition {
    private final WebView reader;
    private final ImageView cover;
    private boolean painted, destroyed;
    private int navigation;

    PageTransition(WebView reader, FrameLayout frame) {
        this.reader = reader;
        cover = new ImageView(reader.getContext());
        cover.setScaleType(ImageView.ScaleType.FIT_XY);
        cover.setVisibility(View.GONE);
        cover.setClickable(true);
        cover.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);
        frame.addView(cover, new FrameLayout.LayoutParams(-1, -1));
    }

    // Called before load/goBack, while WebView still contains the previous page.
    void capture() {
        if (!painted || destroyed || cover.getVisibility() == View.VISIBLE
                || reader.getWidth() == 0 || reader.getHeight() == 0) return;
        try {
            Bitmap image = Bitmap.createBitmap(reader.getWidth(), reader.getHeight(), Bitmap.Config.ARGB_8888);
            reader.draw(new Canvas(image));
            cover.animate().cancel();
            cover.setImageBitmap(image);
            cover.setAlpha(1f);
            cover.setVisibility(View.VISIBLE);
        } catch (RuntimeException | OutOfMemoryError ignored) {
            // A large viewport must not make navigation depend on bitmap memory.
            clear();
        }
    }

    void started() {
        capture();
        if (cover.getVisibility() == View.VISIBLE) {
            cover.animate().cancel();
            cover.setAlpha(1f);
        }
        final int current = ++navigation;
        // Also release the cover on an error page or an interrupted local load.
        reader.postDelayed(() -> reveal(current, false), 5000);
    }

    void ready() { awaitLayout(navigation, 0); }

    private boolean isCurrent(int value) { return !destroyed && value == navigation; }

    private void awaitLayout(int current, int attempt) {
        if (!isCurrent(current)) return;
        reader.evaluateJavascript(
            "document.readyState==='complete' && window.iqjOfflineReady===true"
            + " ? (matchMedia('(prefers-reduced-motion: reduce)').matches ? 'reduce' : 'ready') : 'wait'",
            result -> {
                if (!isCurrent(current)) return;
                if ("\"wait\"".equals(result) && attempt < 40) {
                    reader.postDelayed(() -> awaitLayout(current, attempt + 1), 50);
                    return;
                }
                boolean animate = "\"ready\"".equals(result) && ValueAnimator.areAnimatorsEnabled();
                // onPageFinished alone does not guarantee that the renderer has
                // submitted the frame containing the restored document.
                reader.postVisualStateCallback(current, new WebView.VisualStateCallback() {
                    @Override public void onComplete(long request) { reveal(current, animate); }
                });
            });
    }

    private void reveal(int current, boolean animate) {
        if (!isCurrent(current)) return;
        painted = true;
        if (cover.getVisibility() != View.VISIBLE) return;
        if (animate) cover.animate().alpha(0f).setDuration(160).withEndAction(() -> {
            if (isCurrent(current)) clear();
        }).start();
        else clear();
    }

    private void clear() {
        cover.animate().cancel();
        cover.setVisibility(View.GONE);
        cover.setImageDrawable(null); // Release the in-memory frame; never save it to disk.
    }

    void destroy() {
        destroyed = true;
        ++navigation;
        clear();
    }
}
