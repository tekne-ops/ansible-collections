# Bootstrap Role

Post-install bootstrap: installs extra packages, runs OneDrive first sync (with interactive auth), creates symlinks from OneDrive to home, configures Bluetooth, and applies XFCE desktop settings (wallpaper, themes, fonts, shortcuts).

## What It Does

**Execution order:**

1. **Network check** – Waits for connectivity (ping archlinux.org) before packages.
2. **Package installation** – Installs `bootstrap_packages` via pacman (e.g. Chrome, Zoom, VS Code, Cursor, gaming/office apps). Verifies installation.
3. **OneDrive sync and desktop startup** (`tasks/onedrive_sync.yml`) – If `~/.config/onedrive/items.sqlite3` does not exist: runs the first sync with `--resync --resync-auth` (required because `sync_list` is already installed) inside a pseudo-terminal so the device-login prompt is flushed to the log, **pauses for user to authenticate** with Microsoft, and waits for sync to finish. Installs an XFCE autostart helper that waits for `org.freedesktop.Notifications` before starting the user `onedrive.service`. Boot-time service enablement and lingering are disabled so the client cannot cache “notification service unavailable” before login. If the database already exists but `.sync_list.hash` is still the client's `initial-hash` sentinel, runs the same repair resync.
4. **Symlinks** (`tasks/symlinks.yml`) – Ensures parent dirs exist; for each entry in `bootstrap_symlinks`, creates a symlink from OneDrive path to home path (only if source exists). Sets `~/.ssh` to mode 0700. Runs `bootstrap_cursor_restore` as `bootstrap_user`. Skips and warns when a symlink source is missing.
5. **Bluetooth** (`tasks/bluetooth.yml`) – When `/etc/bluetooth/main.conf` exists, applies `bootstrap_bluetooth_config` (lineinfile) and notifies `restart bluetooth`.
6. **XFCE** (`tasks/xfce.yml`) – Configures desktop for `bootstrap_user`: wallpaper per monitor, cursor/GTK/WM/icon themes, keyboard shortcuts (Super+t terminal, Super+b browser), workspace count, Smooth event sounds, fonts, predictable sessions (`SaveOnExit=false`), fullscreen compositor unredirect, and automatic display extension/profile activation. Uses `xfconf-query` against the active user session.

## Requirements

- `tekne.devops.user` run first (users exist).
- OneDrive client installed and configured (`tekne.devops.onedrive`).
- For OneDrive sync: `bootstrap_user`, `bootstrap_onedrive_config_dir`, `bootstrap_onedrive_binary`; first sync is **interactive** (pause for auth).
- For XFCE: an XFCE session and display. Tasks resolve `bootstrap_user` through `getent` and use that account's runtime directory.

## Role Variables

### defaults/main.yml

| Variable | Default | Description |
|----------|---------|-------------|
| `bootstrap_user` | `dvaliente` | User for OneDrive sync and XFCE config |
| `bootstrap_group` | `users` | User's group |
| `bootstrap_home` | `/home/{{ bootstrap_user }}` | Home directory |
| `bootstrap_onedrive` | `/srv/OneDrive` | OneDrive sync directory |
| `bootstrap_onedrive_config_dir` | `{{ bootstrap_home }}/.config/onedrive` | OneDrive config dir (config file inside) |
| `bootstrap_onedrive_binary` | `/usr/bin/onedrive` | OneDrive binary |
| `bootstrap_onedrive_sync_options` | `--sync --download-only --verbose --resync --resync-auth` | First sync options |
| `bootstrap_onedrive_sync_timeout` | `3600` | First sync timeout (seconds) |
| `bootstrap_bluetooth_name` | `{{ ansible_hostname \| default('BlueZ') }}` | Bluetooth device name |
| `bootstrap_xfce_wallpaper` | Path in Pictures/Wallpapers | Wallpaper image path |
| `bootstrap_xfce_monitors` | empty | Monitor names for wallpaper. Tekne host profiles set the outputs. |
| `bootstrap_xfce_cursor_theme` | `Bibata-Original-Amber` | Cursor theme |
| `bootstrap_xfce_wm_theme` | `minimal-grey2` | Window manager theme |
| `bootstrap_xfce_gtk_theme` | `Adwaita-dark` | GTK theme |
| `bootstrap_xfce_icon_theme` | `Flat-Remix-Cyan-Dark` | Icon theme |
| `bootstrap_xfce_font` | `Sans 11` | Default font |
| `bootstrap_xfce_monospace_font` | `Monospace 11` | Monospace font |
| `bootstrap_xfce_font_rgba` | `rgb` | Font RGBA |
| `bootstrap_xfce_workspace_count` | `1` | Workspace count |
| `bootstrap_xfce_skip_if_no_display` | `true` | Skip XFCE when no display (behavior may depend on `xfce_display_available`) |
| `bootstrap_packages` | See below | Pacman packages to install |
| `bootstrap_cursor_restore` | `/srv/code/tekne/bash/bin/restore-cursor` | Script that restores Cursor configuration |

**Default `bootstrap_packages`:** google-chrome, zoom, ventoy-bin, visual-studio-code-bin, cursor-bin, teams-for-linux-bin, httpfs2-2gbplus, crossover, deezer, asar, imagemagick, liblqr, omnissa-horizon-client, transmission-qt, microsoft-edge-stable-bin, ocs-url, bitwarden-bin, yubico-authenticator-bin.

### vars/main.yml

- **OneDrive:** `bootstrap_onedrive_config_dir: "/home/dvaliente/.config/onedrive"` (fixed path for sync/service).
- **Symlinks:** `bootstrap_symlinks` – list of `src`/`dest`. Examples: Documents, notes, bashrc, Remmina, SSH config, Pictures, avatar (`.face`, `.face.icon`), `bin/asd`. SSH identity keys come from the user role. Cursor is restored by `bootstrap_cursor_restore`.
- **Bluetooth:** `bootstrap_bluetooth_config` – list of `regexp`/`line` for `/etc/bluetooth/main.conf` (Name, AutoEnable, SessionMode, StreamMode, NameResolving, MultiProfile, ControllerMode, FastConnectable, JustWorksRepairing). `JustWorksRepairing` is `always` so a mouse can initiate Just Works pairing without a confirmation dialog. `FastConnectable` stays `false` because the Aerox 9 Bluetooth link is BLE and classic fast page scan prevents that connection.

## Task Files

| File | Purpose |
|------|---------|
| `main.yml` | Network wait, package install, include onedrive_sync, symlinks, bluetooth, xfce |
| `onedrive_sync.yml` | First sync (with pause for auth), desktop-aware user service startup |
| `symlinks.yml` | Create symlinks from `bootstrap_symlinks`, keep `~/.ssh` at mode 0700, run `restore-cursor` |
| `bluetooth.yml` | lineinfile on `/etc/bluetooth/main.conf`, notify restart bluetooth |
| `xfce.yml` | xfconf-query for wallpaper, themes, shortcuts, workspaces, sounds, fonts, sessions, compositor and displays |

## Handlers

The role notifies **`restart bluetooth`** after changing `/etc/bluetooth/main.conf`. The `tekne.devops.os` role provides that handler when it runs before bootstrap.

## Symlinks (from vars)

Typical links (customize via `bootstrap_symlinks`): OneDrive/Documents → ~/Documents; Documents/notes → ~/.local/share/notes; bashrc.txt → ~/.bashrc; Remmina config; SSH config; Pictures; avatar → .face / .face.icon; bin/asd from script. Cursor is restored by `/srv/code/tekne/bash/bin/restore-cursor`.

## Tags

| Tag | Description |
|-----|-------------|
| `bootstrap` | All bootstrap tasks |
| `network` | Network wait |
| `packages` | Package install and verify |
| `onedrive` | OneDrive sync and service |
| `sync` | First sync and auth pause |
| `service` | OneDrive XFCE autostart and user-service lifecycle |
| `symlinks` | Symlink creation and SSH permissions |
| `ssh` | SSH dir and key permissions (inside symlinks) |
| `bluetooth` | Bluetooth config |
| `xfce` | XFCE desktop config |
| `wallpaper` | Wallpaper per monitor |
| `cursor` | `restore-cursor` and the XFCE cursor theme |
| `theme` | WM/GTK/icon themes |
| `shortcuts` | Keyboard shortcuts |
| `workspaces` | Workspace count |
| `sounds` | Input/event sounds |
| `fonts` | Font and RGBA |
| `verify` | Package verification |

## Example Playbook

Tekne playbooks set `bootstrap_xfce_monitors` from `inventories/host_profiles`. ASTER uses `eDP-1` and `DP-1-1`. YUGEN uses `DP-1`, `DP-2`, and `DP-3`.

```yaml
- hosts: localhost
  roles:
    - tekne.devops.user
    - tekne.devops.onedrive
    - role: tekne.devops.bootstrap
      vars:
        bootstrap_user: dvaliente
        bootstrap_xfce_monitors: ["DP-1", "DP-2", "DP-3"]
```

## Notes

- **OneDrive first sync** pauses for user authentication; follow on-screen URL/code steps.
- OneDrive monitor mode starts only in XFCE after the notification service is
  available. The user service is intentionally not enabled at
  `default.target`, and lingering is intentionally disabled.
- Symlinks are created only when the **source** exists; missing sources are reported and skipped.
- XFCE tasks resolve `bootstrap_user` through `getent` and use that account's
  runtime directory; no fixed UID is assumed.
- Ensure a `restart bluetooth` handler exists in the play (the `os` role provides it).

## License

MIT-0

## Author

dvaliente
