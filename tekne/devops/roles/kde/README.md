# KDE Plasma

Waits until `archlinux.org` answers, installs `plasma-meta`, `kde-applications-meta`, and `plasma-login-manager`, then enables `plasmalogin.service`.

Set `kde_install_chroot_phase` (or the play variable `install_chroot_phase`) to skip the connectivity check while PID 1 is still the live ISO.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `kde_packages` | Plasma and KDE application metas | Packages passed to pacman |
| `kde_login_service` | `plasmalogin.service` | Display manager unit |
| `kde_install_chroot_phase` | `install_chroot_phase` | Skip the ping check during install |

## Tags

`kde`, `network`, `packages`
