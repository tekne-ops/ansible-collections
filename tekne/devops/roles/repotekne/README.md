# repotekne

Creates the Tekne package-repo data and AUR cache directories, then starts `fiercebrake/arch:1.1.0` on the `dockers` network at `192.168.75.13`.

`/srv/docker/repotekne` is the published repo. `/mnt/cache/aur-build-tekne` is the build cache. Image, network, and volume comparisons are strict. The role waits until the container accepts an exec.

## Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `repotekne_container_image` | `fiercebrake/arch:1.1.0` | Image tag |
| `repotekne_docker_ip` | `192.168.75.13` | Address on `dockers` |
| `repotekne_data_dir` | `/srv/docker/repotekne` | Repository data |
| `repotekne_cache_dir` | `/mnt/cache/aur-build-tekne` | AUR build cache |

## Tags

`repotekne`, `config`, `docker`
