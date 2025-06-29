#!/usr/bin/python3

import os
import subprocess
import re

def get_newest_gz_version(git_url: str, gz_tag_prefix: str) -> str:
    result = subprocess.run(['git', 'ls-remote', '--tags', git_url], stdout=subprocess.PIPE)
    tags = result.stdout.decode('utf-8').split('\n')
    newest_tag = (0, 0, 0)
    for tag in tags:
        tag_name = tag.split('/')[-1]  # Removes the 'refs/tags/' prefix
        if tag_name.startswith(gz_tag_prefix):
            tag_suffix = tag_name[len(gz_tag_prefix)+1:]
            tag_major, tag_minor, tag_patch = tag_suffix.split('.')
            if tag_major.isnumeric() and tag_minor.isnumeric() and tag_patch.isnumeric():
                tag_version = (int(tag_major), int(tag_minor), int(tag_patch))
                if tag_version > newest_tag:
                    newest_tag = tag_version
    return '.'.join([str(x) for x in newest_tag])

def update_pkgbuild(pkgbuild_dir: str, new_version: str):
    dir_name = os.path.basename(pkgbuild_dir)
    pkgbuild_path = os.path.join(pkgbuild_dir, 'PKGBUILD')

    with open(pkgbuild_path, 'r') as f:
        pkgbuild = f.read()

    # Read the current version
    pkgbuild_lines = pkgbuild.split('\n')
    for i, line in enumerate(pkgbuild_lines):
        if line.startswith('pkgrel='):
            pkgbuild_lines[i] = 'pkgrel=1'
        if line.startswith('pkgver='):
            current_version = line.split('=')[1]
            if current_version != new_version:
                print(f'{dir_name}: {current_version} -> {new_version}')
                pkgbuild_lines[i] = f'pkgver={new_version}'
            else:
                print(f'{dir_name}: {current_version}')
                return

    with open(pkgbuild_path, 'w') as f:
        f.write('\n'.join(pkgbuild_lines))

    # Update package checksums
    subprocess.run(['updpkgsums', pkgbuild_path])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Create mosaic for the specified mission.')
    parser.add_argument('--dir', required=True, default='./src', type=str, help='Target folder')
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.dir):
        if 'PKGBUILD' in files and root[-1].isnumeric():
            gz_name = os.path.basename(root).rstrip('0123456789')
            gz_major = os.path.basename(root)[len(gz_name):]
            gz_ver = get_newest_gz_version(f'https://github.com/gazebosim/{gz_name}.git', f'{gz_name}{gz_major}')
            update_pkgbuild(root, gz_ver)

