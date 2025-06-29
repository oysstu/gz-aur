#!/usr/bin/env bash
eval $(ssh-agent)
ssh-add
vcs pull -w 1 ./src
