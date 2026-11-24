"""Exercise release eligibility and scheduling with real Java, without Android."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ANDROID = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('java') and shutil.which('javac'), 'JDK required')
class ReleaseEligibilityTests(unittest.TestCase):
    def run_java(self, name):
        with tempfile.TemporaryDirectory() as classes:
            compiled = subprocess.run([
                'javac', '--release', '8', '-Xlint:-options', '-d', classes,
                str(ANDROID / f'src/org/quadrobic/iqj/{name}.java'),
                str(ANDROID / f'tests/{name}Test.java'),
            ], capture_output=True, text=True)
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            result = subprocess.run([
                'java', '-cp', classes, f'org.quadrobic.iqj.{name}Test',
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_only_newer_apks_from_this_repository_are_offered(self):
        self.run_java('ReleaseVersion')

    def test_upgrade_and_manual_check_ignore_old_cooldown(self):
        self.run_java('UpdateSchedule')


if __name__ == '__main__':
    unittest.main()
