package org.quadrobic.iqj;

/** A persisted cooldown belongs to the installed build that performed the check. */
final class UpdateSchedule {
    static final long HOUR = 60 * 60 * 1000L;
    static final long CHECK_INTERVAL = HOUR;
    static final long RETRY_INTERVAL = HOUR / 4;

    static boolean due(String installed, String checked, long now, long next, boolean manual) {
        return manual || !installed.equals(checked) || next <= now || next - now > CHECK_INTERVAL;
    }
}
