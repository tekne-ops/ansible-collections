# XFCE4 Role

Installs XFCE4 desktop environment and related packages for Arch Linux. Optionally installs and configures LightDM (including slick greeter) on a specific hostname.

## What It Does

1. **Reads hostname** from `/etc/hostname` and sets facts for the role.
2. **Installs XFCE4** package groups and packages on all hosts (desktop, themes, portals, Xorg, bluetooth, first-boot apps).
3. **On hosts in `xfce4_lightdm_hosts` (ASTER, YUGEN):** installs LightDM and slick-greeter, enables LightDM, and sets `greeter-session=lightdm-slick-greeter` and `user-session=xfce` in `/etc/lightdm/lightdm.conf`.
4. **User configuration** – creates per-user directories and copies portal config and the `minimal-grey2` window theme. ASTER also receives an ACPI media-key handler for `xfce4_acpi_user`.
5. **Verifies** package and service state.

## Requirements

- `community.general` collection (for `pacman` module)
- LightDM host check uses the hostname read from `/etc/hostname`; no extra role required

```bash
ansible-galaxy collection install community.general
```

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `xfce4_packages` | See defaults | XFCE4 packages to install on all hosts |
| `xfce4_lightdm_packages` | See defaults | LightDM packages for specific hosts |
| `xfce4_lightdm_hosts` | ASTER, YUGEN | Hostnames that receive LightDM |
| `xfce4_lightdm_service` | `lightdm` | LightDM service name |

### XFCE4 Packages (all hosts)

- xfce4, xfce4-goodies
- gnome-keyring, seahorse
- xdg-desktop-portal, xdg-desktop-portal-gtk, xdg-desktop-portal-xapp, libportal
- bibata-cursor-theme-bin, flat-remix, kora-icon-theme
- xorg-server, xdotool, playerctl

### LightDM Packages (ASTER, YUGEN)

- lightdm, lightdm-slick-greeter
- light-locker and the GTK and WebKit greeters are removed

The role also replaces `#greeter-session=example-gtk-gnome` with `greeter-session=lightdm-slick-greeter` in `/etc/lightdm/lightdm.conf`.

## Dependencies

None. The role reads the hostname from `/etc/hostname` and installs LightDM when it is in `xfce4_lightdm_hosts` (case-insensitive).

## Example Playbook

```yaml
- hosts: workstations
  roles:
    - ansible-role-xfce4   # Installs XFCE4; LightDM on ASTER and YUGEN
```

## Tags

| Tag | Description |
|-----|-------------|
| `xfce4` | All XFCE4 tasks |
| `packages` | Package installation only |
| `lightdm` | LightDM packages, service, and lightdm.conf |
| `config` | LightDM config file and user/portal config |
| `service` | Service management |
| `verify` | Verification tasks |

## Host-Specific Behavior

| Hostname | XFCE4 Packages | LightDM Packages | LightDM Service |
|----------|----------------|------------------|-----------------|
| ASTER, YUGEN | Installed | Installed | Enabled (stopped) |
| Others | Installed | Skipped | Skipped |

## License

MIT-0

## Author

dvaliente
