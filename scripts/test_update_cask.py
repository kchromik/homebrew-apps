import hashlib
from pathlib import Path
import tempfile
import unittest

from update_cask import updated_cask, validate_request, verify_download


class CaskGuardTests(unittest.TestCase):
    def setUp(self):
        self.cask = 'cask "whisperbar" do\n  version "1.20.0"\n  sha256 "' + 'a' * 64 + '"\n  depends_on arch: :arm64\nend\n'
        self.payload = {'version': '1.20.1', 'release_mode': 'apple-silicon',
                        'download_url': 'https://github.com/kchromik/shoutflow-releases/releases/download/v1.20.1/WhisperBar-1.20.1.dmg'}

    def validate(self):
        return validate_request({'client_payload': self.payload}, 'repository_dispatch', self.cask)

    def test_regular_release_preserves_intel_exclusion(self):
        payload, old = self.validate()
        self.assertEqual(old, '1.20.0')
        new = updated_cask(self.cask, payload['version'], 'b' * 64)
        self.assertIn('depends_on arch: :arm64', new)
        self.assertIn('version "1.20.1"', new)

    def test_bridge_dispatch_is_rejected(self):
        self.payload['release_mode'] = 'legacy-universal'
        with self.assertRaises(ValueError):
            self.validate()

    def test_legacy_and_out_of_order_releases_are_rejected(self):
        for version in ['1.19.2', '1.19.1', '1.20.0']:
            self.payload['version'] = version
            with self.assertRaises(ValueError):
                self.validate()
        self.cask = self.cask.replace('1.20.0', '1.21.0')
        self.payload['version'] = '1.20.1'
        with self.assertRaises(ValueError):
            self.validate()

    def test_foreign_download_is_rejected(self):
        self.payload['download_url'] = 'https://example.com/update.dmg'
        with self.assertRaises(ValueError):
            self.validate()

    def test_missing_arm_requirement_is_rejected(self):
        self.cask = self.cask.replace('depends_on arch: :arm64', 'depends_on arch: :x86_64')
        with self.assertRaises(ValueError):
            self.validate()

    def test_download_requires_valid_dmg_and_matching_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'release.dmg'
            path.write_bytes(b'<html>404 Not Found</html>')
            with self.assertRaises(ValueError):
                verify_download(path, hashlib.sha256(path.read_bytes()).hexdigest())
            data = bytes(100) + b'koly' + bytes(508)
            path.write_bytes(data)
            with self.assertRaises(ValueError):
                verify_download(path, 'f' * 64)
            verify_download(path, hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    unittest.main()
