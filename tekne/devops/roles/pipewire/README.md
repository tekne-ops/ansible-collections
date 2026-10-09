# Pipewire Role

Deploys PipeWire and WirePlumber user configuration on Arch Linux.

PipeWire itself is installed earlier, by pacstrap (`pipewire`, `pipewire-alsa`, `pipewire-jack`, `pipewire-pulse`, `wireplumber`). This role adds the Bluetooth codec libraries and per-user drop-ins.

## What It Does

1. **Installs codec libraries** (`libldac`, `libfreeaptx`)
2. **Creates user config directories** for each entry in `pipewire_users`
3. **Deploys drop-ins** under `~/.config/pipewire/pipewire.conf.d` and `~/.config/wireplumber/wireplumber.conf.d`
4. **Removes retired drop-ins** (`60-volume-boost.conf`, `99-ldac.conf`, `60-soft-limiter.conf`)
5. **Restarts user services** when a config file changes and that user has a running session

## Requirements

- `community.general` collection (for `pacman`)
- Target users must already exist
- Run `tekne.devops.user` first when it creates those users

```bash
ansible-galaxy collection install community.general
```

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `pipewire_codec_packages` | `libldac`, `libfreeaptx` | Bluetooth codec libraries |
| `pipewire_users` | See defaults | Users that receive configuration |
| `pipewire_default_group` | `users` | Fallback group for new directories |
| `pipewire_user_services` | `pipewire`, `pipewire-pulse`, `wireplumber` | User units restarted after a change |
| `pipewire_install_chroot_phase` | `install_chroot_phase` | Skip the network wait and service restart in the install chroot |

Each `pipewire_users` entry:

| Field | Description |
|-------|-------------|
| `name` | Account name |
| `group` | Group owner for the drop-ins |
| `hd660s_eq` | Deploy the Sennheiser HD 660S filter-chain sink. Default `false`. Enabled for `dvaliente`. |

## Files

| Source | Destination |
|--------|-------------|
| `files/pipewire.conf` | `~/.config/pipewire/pipewire.conf.d/99-audio-quality.conf` |
| `files/sink-eq06-sony.conf` | `~/.config/pipewire/pipewire.conf.d/sink-eq06.conf` when `hd660s_eq` is true |
| `files/50-bluetooth-quality.conf` | `~/.config/wireplumber/wireplumber.conf.d/50-bluetooth-quality.conf` |

`99-audio-quality.conf` sets a 48 kHz clock, allows 44.1–96 kHz, and uses resample quality 10.

`50-bluetooth-quality.conf` keeps A2DP roles, disables headset-profile autoswitch, holds the Bluetooth link at 48 kHz, and sets LDAC quality to `auto` so the bitrate drops instead of chopping. SBC-XQ and hardware volume stay on the device quirk list. Bluetooth nodes resample at quality 4; other streams stay at 10.

The HD 660S sink is optional. Select "Sennheiser HD 660S EQ" in pavucontrol; it is not the default output.

A changed drop-in restarts the user services only when `/run/user/<uid>` exists. Otherwise the new files apply at the next login.

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
| `network` | Network connectivity wait before packages |
| `packages` | Codec library install |
| `config` | Configuration directories and files |
| `service` | User session check and service restart |

## License

MIT-0

## Author

dvaliente
