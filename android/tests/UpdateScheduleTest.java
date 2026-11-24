package org.quadrobic.iqj;

/** Model the real regression: a new installed build inherits a future cooldown. */
public final class UpdateScheduleTest {
    private static void require(boolean condition) {
        if (!condition) throw new AssertionError("Unexpected update schedule");
    }

    public static void main(String[] args) {
        long now = 100 * UpdateSchedule.HOUR;
        long next = now + UpdateSchedule.CHECK_INTERVAL;
        require(!UpdateSchedule.due("2026.11.24.12", "2026.11.24.12", now, next, false));
        require(UpdateSchedule.due("2026.11.24.13", "2026.11.24.12", now, next, false));
        require(UpdateSchedule.due("2026.11.24.12", "", now, next, false));
        require(UpdateSchedule.due("2026.11.24.12", "2026.11.24.12", now, next, true));
        require(UpdateSchedule.due("2026.11.24.12", "2026.11.24.12", next, next, false));
        require(UpdateSchedule.due("2026.11.24.12", "2026.11.24.12", now,
            now + 12 * UpdateSchedule.HOUR, false));
        require(!UpdateSchedule.due("2026.11.24.12", "2026.11.24.12", now,
            now + UpdateSchedule.RETRY_INTERVAL, false));
        require(UpdateSchedule.due("2026.11.24.12", "2026.11.24.12",
            now + UpdateSchedule.RETRY_INTERVAL, now + UpdateSchedule.RETRY_INTERVAL, false));
        System.out.println("PASS: upgrade, legacy cooldown, manual override, expiry and retry");
    }
}
