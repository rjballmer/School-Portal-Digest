import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "school-portal-digest" / "scripts" / "init_school_portal_digest.py"


def run_script(*args, check=True):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"command failed\nstdout={result.stdout}\nstderr={result.stderr}")
    return result


class InitSchoolPortalDigestTests(unittest.TestCase):
    def test_init_creates_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "school-portal"
            result = run_script(
                "--target", str(target),
                "--portal-name", "ParentSquare",
                "--login-url", "https://school.example/login",
                "--home-url", "https://school.example/home",
                "--children", "A, B",
                "--quiet",
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue((target / "config.json").exists())
            self.assertTrue((target / "site-config.json").exists())
            self.assertTrue((target / "action-items.json").exists())
            self.assertTrue((target / "calendar").is_dir())
            self.assertTrue(list(target.glob("summary-*.md")))

            config = json.loads((target / "config.json").read_text())
            self.assertEqual(config["portal"]["name"], "ParentSquare")
            self.assertEqual([child["label"] for child in config["family"]["children"]], ["A", "B"])

            site_config = json.loads((target / "site-config.json").read_text())
            self.assertEqual(site_config["baseUrl"], "https://school.example")

    def test_init_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "school-portal"
            first = run_script("--target", str(target), "--quiet")
            second = run_script("--target", str(target), "--quiet")

            self.assertEqual(first.returncode, 0)
            self.assertEqual(second.returncode, 0)
            self.assertIn("exists:", second.stdout)

    def test_validate_accepts_initialized_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "school-portal"
            run_script("--target", str(target), "--quiet")

            result = run_script("--target", str(target), "--validate")

            self.assertEqual(result.returncode, 0)
            self.assertIn("validation passed", result.stdout)

    def test_validate_rejects_broken_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "school-portal"
            run_script("--target", str(target), "--quiet")
            config = json.loads((target / "config.json").read_text())
            config["family"]["children"] = []
            (target / "config.json").write_text(json.dumps(config), encoding="utf-8")

            result = run_script("--target", str(target), "--validate", check=False)

            self.assertEqual(result.returncode, 1)
            self.assertIn("family.children", result.stdout)

    def test_rejects_empty_children_argument(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "school-portal"
            result = run_script("--target", str(target), "--children", " , ", check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("--children must include", result.stderr)
            self.assertFalse(target.exists())

    def test_rejects_invalid_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "school-portal"
            result = run_script("--target", str(target), "--login-url", "not-a-url", check=False)

            self.assertEqual(result.returncode, 2)
            self.assertIn("must be an absolute http(s) URL", result.stderr)
            self.assertFalse(target.exists())

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "school-portal"
            result = run_script("--target", str(target), "--dry-run")

            self.assertEqual(result.returncode, 0)
            self.assertIn("would create", result.stdout)
            self.assertFalse(target.exists())

    def test_version_flag(self):
        result = run_script("--version")

        self.assertEqual(result.returncode, 0)
        self.assertIn("initializer", result.stdout)


if __name__ == "__main__":
    unittest.main()
