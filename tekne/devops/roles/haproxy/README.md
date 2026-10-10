# HAProxy

Writes `/srv/docker/haproxy/haproxy.cfg` and starts `haproxytech/haproxy-alpine:3.3`. TLS material comes from the vault variable `haproxy_ssl_pem` or from `haproxy_ssl_pem_path`. The role fails when neither source is present.

Set `haproxy_certbot_enabled` to issue the certificate with Certbot and a Cloudflare token instead of supplying a PEM. Certbot runs in `/opt/certbot` and writes the combined PEM for `tekne.sv`.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `haproxy_ssl_pem` | `null` | Full PEM contents, usually from vault |
| `haproxy_ssl_pem_path` | `null` | Controller path to a PEM file |
| `haproxy_container_image` | `haproxytech/haproxy-alpine:3.3` | Image tag |
| `haproxy_certbot_enabled` | `false` | Issue the certificate on the host |
| `haproxy_certbot_domain` | `tekne.sv` | Certificate name |
| `haproxy_cloudflare_api_token` | `null` | Token used when Certbot is enabled |

## Tags

`haproxy`, `config`, `certbot`
