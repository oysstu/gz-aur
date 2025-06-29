#!/usr/bin/env bash
for d in ./src/*/ ; do (cd "$d" && updpkgsums); done
