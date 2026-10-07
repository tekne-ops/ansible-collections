# Pipewire Role

Installs and configures Pipewire audio system for Arch Linux, replacing conflicting audio packages.

## What It Does

1. **Removes conflicting packages** (jack, ffmpeg, jack2, etc.)
2. **Installs Pipewire stack** (pipewire, wireplumber, pavucontrol, etc.)
3. **Creates user config directories** for each entry in `pipewire_users`
4. **Deploys configuration files** to user directories
5. **Enables user service** (without starting it)
6. **Verifies installation** and service state

## Requirements

- `community.general` collection (for `pacman` module)
- Target users must already exist.

```bash
ansible-galaxy collection install community.general
```

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `pipewire_conflicting_packages` | See defaults | Packages to remove before install |
| `pipewire_packages` | See defaults | Pipewire packages to install |
| `pipewire_user_service` | `pipewire` | User service to enable |
| `pipewire_users` | See defaults | Users that receive PipeWire configuration |
| `pipewire_default_group` | `users` | Fallback primary group |

### Conflicting Packages (removed)

- jack, ffmpeg, jack2, libjack, portaudio, libopenmpt, freerdp

### Pipewire Packages (installed)

- pipewire, pipewire-audio, pipewire-libcamera, pipewire-jack
- pipewire-alsa, pipewire-pulse, lib32-pipewire, lib32-pipewire-jack
- wireplumber, pavucontrol, sound-theme-smooth

## Dependencies

- Run `tekne.devops.user` first when it is responsible for creating the target users.

## Files

| Source | Destination |
|--------|-------------|
| `files/pipewire.conf` | `~/.config/pipewire/pipewire.conf` |
| `files/sink-eq06-sony.conf` | `~/.config/pipewire/pipewire.conf.d/sink-eq06.conf` |

## Created Directories

For each user:
- `~/.config/wireplumber/wireplumber.conf.d/`
- `~/.config/pipewire/pipewire.conf.d/`

## Example Playbook

```yaml
- hosts: workstations
  roles:
    - tekne.devops.user
    - tekne.devops.pipewire
```

## Tags

| Tag | Description |
|-----|-------------|
| `pipewire` | All pipewire tasks |
| `network` | Network connectivity wait (before packages) |
| `packages` | Package install/remove only |
| `config` | Configuration directories and files |
| `service` | User service management |
| `verify` | Verification tasks |

## License

MIT-0

## Author

dvaliente
