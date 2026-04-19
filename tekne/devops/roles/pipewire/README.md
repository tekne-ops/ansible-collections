# Pipewire Role

Deploys a per-user PipeWire drop-in snippet for clock and resampling settings.

## What It Does

1. Resolves each entry in `users` via `getent passwd`
2. Creates `~/.config/pipewire/pipewire.conf.d/`
3. Copies `files/pipewire.conf` to `~/.config/pipewire/pipewire.conf.d/99-audio-quality.conf`

## Requirements

- `tekne.devops.user` (or equivalent) must run first so `users` is defined.

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `users` | *(required)* | Same list as the user role |
| `default_group` | `users` | Group for files when a user omits `group` |

## Tags

| Tag | Description |
|-----|-------------|
| `pipewire` | All tasks |
| `config` | Directory and file deployment |

## License

MIT-0

## Author

dvaliente
