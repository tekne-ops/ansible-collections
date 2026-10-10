# n8n

Creates the `n8n_data` volume and starts the pinned n8n image on the `dockers` network at `192.168.75.14`. Timezone defaults to `America/El_Salvador`. Image, network, and volume comparisons are strict.

The server role list does not import this role. Apply it with `--tags n8n` from a play that includes it, after Docker has created the `dockers` network.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `n8n_docker_image` | `docker.n8n.io/n8nio/n8n:1.113.3` | Image tag |
| `n8n_docker_network` | `dockers` | Docker network |
| `n8n_docker_ip` | `192.168.75.14` | Address on that network |
| `n8n_volume_name` | `n8n_data` | Named volume mounted at `/home/node/.n8n` |
| `n8n_timezone` | `America/El_Salvador` | `TZ` and `GENERIC_TIMEZONE` |

## Tags

`n8n`, `docker`
