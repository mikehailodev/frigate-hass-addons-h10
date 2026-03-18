# Frigate Hailo-10H Add-ons for Home Assistant

> Frigate NVR with **Hailo-10H** AI accelerator support. This is a temporary
> fork of the [official Frigate add-ons](https://github.com/blakeblackshear/frigate-hass-addons)
> that replaces HailoRT 4.x (Hailo-8/8L) with HailoRT 5.2.0 (Hailo-10H).
>
> Once Hailo-8 and Hailo-10H co-existence is supported upstream, this fork
> will be retired in favor of the official repository.

## Installing

Click the button below to add this repository:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmikehailodev%2Ffrigate-hass-addons-h10)

Or manually: **Settings** → **Add-ons** → **Add-on Store** → **⋮** → **Repositories** and add:
```
https://github.com/mikehailodev/frigate-hass-addons-h10
```

## Add-ons provided by this repository

- **[Frigate (Full Access) — Hailo-10H](frigate_fa/)** — NVR with realtime object detection using Hailo-10H

## What's different from the official Frigate add-on?

| | Official Frigate | This fork |
|---|---|---|
| **HailoRT** | 4.21.0 | 5.2.0 |
| **Hailo hardware** | Hailo-8, Hailo-8L | Hailo-10H |
| **Kernel driver** | `hailo_pci` | `hailo1x_pci` |
| **Device node** | `/dev/hailo0` | `/dev/hailo0` |
| **Detector config** | `type: hailo8l` | `type: hailo8l` (same key) |

The Frigate configuration is identical — the detector type remains `hailo8l` for
compatibility. The plugin auto-detects Hailo-10H hardware and selects the
appropriate model.

## Prerequisites

- **HAOS** built with `hailo10h-pci` driver and `hailo10h-firmware`
  ([operating-system fork](https://github.com/mikehailodev/operating-system),
  branch `feature/hailort-package`)
- **Raspberry Pi 5** with Hailo-10H AI HAT+
- Disable **Protection Mode** on the add-on (required for `/dev/hailo0` access)

## Frigate Configuration

```yaml
mqtt:
  enabled: true
  host: <your-mqtt-broker>
  user: <user>
  password: <password>

cameras:
  my_camera:
    enabled: true
    ffmpeg:
      inputs:
        - path: <rtsp-url>
          roles:
            - detect
            - record

detectors:
  hailo:
    type: hailo8l
    device: PCIe

model:
  width: 640
  height: 640
  input_tensor: nhwc
  input_pixel_format: rgb
  input_dtype: int
  model_type: yolo-generic

detect:
  enabled: true
  width: 1280
  height: 720
  fps: 5

version: 0.17-0
```
