# GPU Role

Installs GPU drivers based on hostname. YUGEN gets discrete NVIDIA drivers. ASTER gets hybrid Intel plus NVIDIA, including PRIME. THEMIS, KVM, and HEPHAESTUS get Intel/Mesa.

## What It Does

1. **Detects GPU type** from the hostname lists (`nvidia`, `hybrid`, or `intel`)
2. **Installs the matching drivers**
3. **Verifies installation** of those packages

## Requirements

- `community.general` collection (for `pacman` module)
- GPU host check uses `ansible_hostname` (from gathered facts); no extra role required

```bash
ansible-galaxy collection install community.general
```

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `gpu_nvidia_hostnames` | `YUGEN` | Discrete NVIDIA hosts |
| `gpu_hybrid_hostnames` | `ASTER` | Hybrid Intel iGPU plus NVIDIA dGPU hosts |
| `gpu_intel_hostnames` | `THEMIS`, `HEPHAESTUS`, `KVM` | Intel/Mesa hosts |
| `gpu_nvidia_packages` | See defaults | NVIDIA packages for YUGEN and ASTER |
| `gpu_hybrid_extra_packages` | `nvidia-prime` | Extra packages for hybrid hosts |
| `gpu_intel_packages` | See defaults | Intel/Mesa packages for Intel and hybrid hosts |

### NVIDIA Packages (YUGEN and ASTER)

- lib32-opencl-nvidia-tkg, lib32-vulkan-icd-loader, lib32-nvidia-utils-tkg
- nvidia-open-dkms-tkg, nvidia-settings-tkg, opencl-nvidia-tkg
- vulkan-icd-loader, nvidia-utils-tkg

### Intel/Mesa Packages (THEMIS, KVM, HEPHAESTUS, and ASTER)

- mesa, lib32-mesa, vulkan-intel, lib32-vulkan-intel

## Dependencies

None. The role classifies the hostname as `nvidia`, `hybrid`, or `intel` using `gpu_nvidia_hostnames`, `gpu_hybrid_hostnames`, and `gpu_intel_hostnames`.

## Example Playbook

```yaml
- hosts: workstations
  roles:
    - tekne.devops.gpu
```

## Tags

| Tag | Description |
|-----|-------------|
| `gpu` | All GPU tasks |
| `config` | Configuration/detection |
| `nvidia` | NVIDIA specific tasks |
| `intel` | Intel/Mesa specific tasks |
| `packages` | Package installation |
| `verify` | Verification tasks |

## Host-Specific Behavior

| Hostname | GPU Type | Packages Installed |
|----------|----------|-------------------|
| YUGEN | NVIDIA | NVIDIA/TKG packages |
| ASTER | Hybrid | NVIDIA/TKG, Intel/Mesa, and `nvidia-prime` |
| THEMIS, KVM, HEPHAESTUS | Intel/Mesa | Mesa and Vulkan packages |

## License

MIT-0

## Author

dvaliente
