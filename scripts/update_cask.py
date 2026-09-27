#!/usr/bin/env python3
"""Update WhisperBar only from a verified, non-legacy public ARM release."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

REPOSITORY = 'kchromik/shoutflow-releases'


def version_tuple(value):
    if not re.fullmatch(r'\d+\.\d+\.\d+', value):
        raise ValueError('Expected a stable three-component version.')
    return tuple(map(int, value.split('.')))


def validate_request(event, event_name, cask):
    payload = event.get('client_payload', {}) if event_name == 'repository_dispatch' else event.get('inputs', {})
    mode = payload.get('release_mode', 'apple-silicon' if event_name == 'workflow_dispatch' else None)
    if mode != 'apple-silicon':
        raise ValueError('Only explicit Apple Silicon releases may update this cask.')
    version = payload.get('version', '')
    current = re.search(r'^  version "([^"]+)"$', cask, re.M)
    if current is None or version_tuple(version) < max(version_tuple(current[1]), (1, 20, 1)):
        raise ValueError('Legacy releases and version downgrades cannot update Homebrew.')
    if not re.search(r'^  depends_on arch: :arm64$', cask, re.M):
        raise ValueError('The Apple Silicon architecture requirement must be preserved.')
    expected_url = f'https://github.com/{REPOSITORY}/releases/download/v{version}/WhisperBar-{version}.dmg'
    if payload.get('download_url') != expected_url:
        raise ValueError('Download URL must match this exact WhisperBar release.')
    return payload, current[1]


def updated_cask(cask, version, sha256):
    if not re.fullmatch('[0-9a-f]{64}', sha256):
        raise ValueError('Invalid SHA-256.')
    cask, count = re.subn(r'^  version "[^"]+"$', f'  version "{version}"', cask, flags=re.M)
    if count != 1:
        raise ValueError('Expected exactly one version stanza.')
    cask, count = re.subn(r'^  sha256 "[^"]+"$', f'  sha256 "{sha256}"', cask, flags=re.M)
    if count != 1:
        raise ValueError('Expected exactly one checksum stanza.')
    return cask


def verify_download(path, digest):
    checksum = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(chunk)
        if stream.tell() < 512:
            raise ValueError('Downloaded file is not a DMG.')
        stream.seek(-512, 2)
        if stream.read(4) != b'koly':
            raise ValueError('Downloaded file is not a UDIF DMG.')
    if checksum.hexdigest() != digest:
        raise ValueError('Downloaded DMG does not match the GitHub asset digest.')


def main():
    cask_path = Path('Casks/w/whisperbar.rb')
    cask = cask_path.read_text()
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    payload, current = validate_request(event, os.environ['GITHUB_EVENT_NAME'], cask)
    version = payload['version']
    release = json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPOSITORY}/releases/tags/v{version}']))
    if release['draft'] or release['prerelease']:
        raise ValueError('Only public stable releases may update Homebrew.')
    asset = next((asset for asset in release['assets'] if asset['name'] == f'WhisperBar-{version}.dmg'), None)
    if not asset or asset['browser_download_url'] != payload['download_url']:
        raise ValueError('Expected release asset is missing.')
    digest = asset.get('digest', '').removeprefix('sha256:')
    if not re.fullmatch('[0-9a-f]{64}', digest):
        raise ValueError('GitHub must provide a SHA-256 digest for the asset.')
    if payload.get('sha256') and payload['sha256'] != digest:
        raise ValueError('Release script and GitHub asset digests differ.')
    destination = Path(os.environ.get('RUNNER_TEMP', '/tmp')) / f'WhisperBar-{version}.dmg'
    # HTTP failures raise before the cask can be edited. Input cannot choose another host.
    with urllib.request.urlopen(payload['download_url'], timeout=120) as response, destination.open('wb') as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
    verify_download(destination, digest)
    current_sha = re.search(r'^  sha256 "([^"]+)"$', cask, re.M)[1]
    if current == version and current_sha != digest:
        raise ValueError('An existing version cannot silently change its release artifact.')
    cask_path.write_text(updated_cask(cask, version, digest))
    with Path(os.environ['GITHUB_OUTPUT']).open('a') as output:
        output.write(f'version={version}\n')
    print(f'Verified WhisperBar {version}: {digest}')


if __name__ == '__main__':
    main()
