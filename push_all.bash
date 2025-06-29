#!/usr/bin/env bash
eval $(ssh-agent)
ssh-add
vcs push -w 1 ./src
