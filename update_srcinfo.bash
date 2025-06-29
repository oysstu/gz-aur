 #!/usr/bin/env bash
 for d in ./src/*/ ; do (cd "$d" && makepkg --printsrcinfo > .SRCINFO); done
