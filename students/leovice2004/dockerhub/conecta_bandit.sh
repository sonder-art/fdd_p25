#!/usr/bin/env bash

nivel=${NIVEL}
contra=${PASSWORD}

SSH_OPTS="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 2220"

sshpass -p "$contra" ssh $SSH_OPTS "bandit${nivel}@bandit.labs.overthewire.org"
