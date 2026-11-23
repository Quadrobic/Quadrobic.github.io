"""Exercise release eligibility with the real Java implementation, without Android."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ANDROID = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('java') and shutil.which('javac'), 'JDK required')
class ReleaseEligibilityTests(unittest.TestCase):
    def test_only_newer_apks_from_this_repository_are_offered(self):
        with tempfile.TemporaryDirectory() as classes:
            compiled = subprocess.run([
                'javac', '--release', '8', '-Xlint:-options', '-d', classes,
                str(ANDROID / 'src/org/quadrobic/iqj/ReleaseVersion.java'),
                str(ANDROID / 'tests/ReleaseVersionTest.java'),
            ], capture_output=True, text=True)
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            result = subprocess.run([
                'java', '-cp', classes, 'org.quadrobic.iqj.ReleaseVersionTest',
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
