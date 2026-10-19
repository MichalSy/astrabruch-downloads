#!/usr/bin/env python3
"""Build the public download page solely from complete public GitHub releases."""
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote

REPO = 'MichalSy/astrabruch-downloads'
PLATFORMS = (
    ('linux', 'Linux', 'x86_64 · TAR.GZ', 'linux-x86_64.tar.gz', 'Entpacken und Astrabruch.x86_64 starten.'),
    ('windows', 'Windows', '64 Bit · ZIP', 'windows-x86_64.zip', 'Entpacken und Astrabruch.exe starten.'),
    ('macos', 'macOS', 'Intel + Apple Silicon · ZIP', 'macos-universal.zip', 'Entpacken und Astrabruch.app öffnen.'),
    ('android', 'Android', 'ARM64 · APK', 'android-arm64.apk', 'APK herunterladen und auf dem Gerät installieren.'),
)
VERSION = re.compile(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)')


def complete_releases(releases):
    result = []
    for release in releases:
        match = VERSION.fullmatch(release.get('tag_name', ''))
        if not match or release.get('draft') or not release.get('published_at'):
            continue
        version = release['tag_name'][1:]
        expected = {f'Astrabruch-{version}-{p[3]}' for p in PLATFORMS} | {'SHA256SUMS.txt'}
        assets = {a['name']: a for a in release.get('assets', []) if a.get('size', 0) > 0}
        if not expected <= assets.keys():
            continue
        result.append((tuple(map(int, match.groups())), release, assets))
    return sorted(result, key=lambda item: item[0], reverse=True)


def asset_url(tag, filename):
    return f'https://github.com/{REPO}/releases/download/{quote(tag, safe="")}/{quote(filename, safe="")}'


def render(releases):
    complete = complete_releases(releases)
    cards = []
    if complete:
        _, release, assets = complete[0]
        tag = release['tag_name']; version = tag[1:]
        channel = 'Testversion' if release.get('prerelease') else 'Release'
        status = f'<span class="status">{channel}</span><strong>{escape(tag)}</strong><span>{escape(release["published_at"][:10])}</span>'
        for key, label, architecture, suffix, instruction in PLATFORMS:
            filename = f'Astrabruch-{version}-{suffix}'
            size = f'{assets[filename]["size"] / 1024 / 1024:.0f} MB'
            cards.append(f'''<article class="platform" data-platform="{key}">
<div class="platform-top"><span class="platform-number">0{len(cards)+1}</span><span class="recommendation" hidden>Dein System</span></div>
<h3>{label}</h3><p class="architecture">{architecture}</p><p class="instruction">{instruction}</p>
<a class="download" href="{asset_url(tag, filename)}" aria-label="{label} {escape(tag)} herunterladen">Herunterladen <span>{size}</span></a>
<a class="install-link" href="#install-{key}">Installation &amp; Hinweise</a></article>''')
        footer = f'<a href="{asset_url(tag, "SHA256SUMS.txt")}">SHA256-Prüfsummen</a><a href="https://github.com/{REPO}/releases/tag/{tag}">Details zu {tag}</a>'
    else:
        status = '<span class="status">In Vorbereitung</span>'
        cards = ['<div class="empty"><h3>Der erste Flug wird vorbereitet.</h3><p>Hier erscheint die spielbare Testversion, sobald alle Plattformpakete fertig sind.</p></div>']
        footer = ''
    archive = ''.join(f'<a href="https://github.com/{REPO}/releases/tag/{item[1]["tag_name"]}">{item[1]["tag_name"]}</a>' for item in complete[1:6])
    template = (Path(__file__).parent / 'site/index.template.html').read_text()
    return template.replace('@@STATUS@@', status).replace('@@DOWNLOADS@@', '\n'.join(cards)).replace('@@RELEASE_LINKS@@', footer).replace('@@ARCHIVE@@', archive)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--releases', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    releases = json.loads(args.releases.read_text())
    if not isinstance(releases, list):
        raise ValueError('Expected a release list')
    if releases and isinstance(releases[0], list):
        releases = [release for page in releases for release in page]
    args.output.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).parent / 'site'
    for name in ('style.css', 'site.js'):
        shutil.copyfile(source / name, args.output / name)
    shutil.copytree(source / 'assets', args.output / 'assets', dirs_exist_ok=True)
    (args.output / 'index.html').write_text(render(releases))
    (args.output / '.nojekyll').touch()
    print('Built download page:', args.output)


if __name__ == '__main__':
    main()
