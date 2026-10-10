# Gerbera

Creates `/srv/docker/gerbera` and `/srv/media`, then starts the pinned Gerbera image with host networking. `/srv/media` is mounted read-only at `/mnt/content`.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `gerbera_container_image` | `gerbera/gerbera@sha256:…` | Pinned image digest |
| `gerbera_config_dir` | `/srv/docker/gerbera` | Config directory |
| `gerbera_media_dir` | `/srv/media` | Media library directory |

## Tags

`gerbera`, `config`, `docker`
