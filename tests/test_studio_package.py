import hashlib
import json
from pathlib import Path
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'studio/build/package/package-manifest.json'


@unittest.skipUnless(MANIFEST.exists(),'Build the optional Windows executable first')
class StudioPackageChecks(unittest.TestCase):
    def test_single_exe_is_bound_to_current_jar_launcher_and_tool(self):
        manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
        sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        exe=ROOT/manifest['exe']
        self.assertEqual(['NebulithStudio.exe'],sorted(p.name for p in exe.parent.iterdir()))
        with exe.open('rb') as stream:self.assertEqual(b'MZ',stream.read(2))
        self.assertEqual(manifest['exeSha256'],sha(exe))
        self.assertEqual(manifest['jarSha256'],sha(ROOT/'studio/build/NebulithStudio.jar'))
        for path,digest in manifest['launcherSources'].items():self.assertEqual(digest,sha(ROOT/path))
        self.assertEqual(manifest['packageToolSha256'],sha(ROOT/'tools/package_studio.py'))
        for kind in ['selfTest','windowSelfTest']:
            evidence=manifest[kind]
            self.assertEqual(0,evidence['javaExitCode'])
            self.assertTrue(evidence['noSystemJavaRequired'])
            self.assertTrue(Path(evidence['runtime']).is_relative_to(evidence['cache']))
            self.assertIn('PASS:',evidence['stdout'])

    def test_embedded_payload_has_runtime_notices_and_checksums(self):
        manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
        payload=ROOT/'studio/build/package/payload.zip'
        self.assertEqual(manifest['payloadSha256'],hashlib.sha256(payload.read_bytes()).hexdigest())
        with zipfile.ZipFile(payload) as archive:
            names=archive.namelist()
            self.assertEqual(len(names),len(set(names)))
            self.assertIn('runtime/bin/java.exe',names)
            self.assertTrue(any(n.startswith('runtime/legal/') for n in names))
            self.assertIn('licenses/dotnet/LICENSE.TXT',names)
            self.assertIn('licenses/kotlin/LICENSE.txt',names)
            hashes=json.loads(archive.read('files.json'))
            for name,digest in hashes.items():self.assertEqual(digest,hashlib.sha256(archive.read(name)).hexdigest())
            self.assertEqual(manifest['jarSha256'],hashes['NebulithStudio.jar'])


if __name__=='__main__':unittest.main()
