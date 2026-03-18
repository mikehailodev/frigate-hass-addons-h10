This add-on provides Frigate NVR with Hailo-10H AI accelerator support.

You must create a config file at `/addon_configs/<slug>/config.yml`
([click here to learn more](https://docs.frigate.video/configuration/#accessing-add-on-config-dir)).

## Hailo-10H Specific Notes

- Uses HailoRT 5.2.0 (replacing the default 4.21.0 for Hailo-8)
- Requires HAOS built with `hailo10h-pci` driver
- Disable **Protection Mode** in the add-on's Info tab
- Detector type in Frigate config is still `hailo8l` (for compatibility)
- The detector auto-detects Hailo-10H hardware

## Required Dependencies

- MQTT: Frigate communicates with Home Assistant via MQTT

## Support

Please [open an issue](https://github.com/mikehailodev/frigate-hass-addons-h10/issues/new) if you need support.
