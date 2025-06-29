# gz-arch
Archlinux AUR Gazebo packages

## Checkout

```bash
vcs import -w 1 --input gz-aur.repos ./src
```

## Update version from github tag
```bash
python update_tags.py --dir ./src
```

## After tag update and verified build
```bash
./update_srcinfo.bash
vcs custom --git --args add PKGBUILD .SRCINFO
vcs custom --git --args commit "Update version"
```