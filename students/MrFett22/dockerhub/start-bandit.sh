#!/usr/bin/env bash
set -Eeuo pipefail

: "${BANDIT_LEVEL:?Falta BANDIT_LEVEL}"
: "${BANDIT_PASSWORD:?Falta BANDIT_PASSWORD}"

BANDIT_PORT="${BANDIT_PORT:-2220}"
BANDIT_USER="bandit${BANDIT_LEVEL}"
BANDIT_HOST="bandit.labs.overthewire.org"

mkdir -p /root/.ssh
touch /root/.ssh/known_hosts
chmod 700 /root/.ssh
chmod 600 /root/.ssh/known_hosts

PASSFILE="$(mktemp)"
trap 'rm -f "$PASSFILE"' EXIT
printf '%s' "$BANDIT_PASSWORD" > "$PASSFILE"
chmod 600 "$PASSFILE"

exec sshpass -f "$PASSFILE" ssh \
  -p "$BANDIT_PORT" \
  -o StrictHostKeyChecking=accept-new \
  -o UserKnownHostsFile=/root/.ssh/known_hosts \
  "${BANDIT_USER}@${BANDIT_HOST}"
