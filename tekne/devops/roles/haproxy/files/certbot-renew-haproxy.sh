#!/usr/bin/env bash
# Rebuild HAProxy PEM after certbot renew and reload the container.
set -euo pipefail

DOMAIN="tekne.sv"
LIVE="/etc/letsencrypt/live/${DOMAIN}"
COMBINED="${LIVE}/haproxy.pem"
DOCKER_PEM="/srv/docker/haproxy/tekne.sv.pem"

cat "${LIVE}/fullchain.pem" "${LIVE}/privkey.pem" > "${COMBINED}"
chmod 600 "${COMBINED}"
cp "${COMBINED}" "${DOCKER_PEM}"
chmod 600 "${DOCKER_PEM}"

if docker ps --format '{{.Names}}' | grep -qx haproxy; then
  docker kill -s HUP haproxy 2>/dev/null || docker restart haproxy
fi
