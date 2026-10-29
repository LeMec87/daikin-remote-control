# Daikin Remote Control

Standalone Home Assistant integration for Daikin air conditioners with a Wi-Fi adapter that
speaks the **dsiot API** (`POST /dsiot/multireq`). It covers everything the remote control can
switch over Wi-Fi, so the built-in Daikin integration is not needed.

[![Validate](https://github.com/LeMec87/daikin-remote-control/actions/workflows/validate.yml/badge.svg)](https://github.com/LeMec87/daikin-remote-control/actions/workflows/validate.yml)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/docs/faq/custom_repositories)

Everything runs locally: no cloud account, no Daikin app, no internet connection needed.

## Supported units

| Indoor unit | Remote | Status |
|---|---|---|
| FTKZ25VVMV (cooling only) | ARC466A63 | tested |

Other Daikin units with a dsiot Wi-Fi adapter (firmware 2.8 and newer) will probably work for
power, mode, temperature and fan, but the airflow positions and extra functions may differ.
Please [report your model](https://github.com/LeMec87/daikin-remote-control/issues/new?template=new_model.md),
whether it works or not.

To check whether your adapter speaks the dsiot API, run the `curl` command from the
[model report template](.github/ISSUE_TEMPLATE/new_model.md). A JSON answer with `responses`
means the unit is compatible. The integration setup also tests the connection and tells you if
the unit does not answer.

## Features

| Entity | Type | Function |
|---|---|---|
| *(device name)* | `climate` | Off, Cool, Dry, Fan only; target temperature 18–32 °C (cool only); fan Auto, Quiet, 1–5; swing Off, Vertical, Horizontal, 3D |
| Airflow up/down | `select` | Highest, High, Middle, Low, Lowest, Swing, Ceiling |
| Airflow left/right | `select` | Far left … Far right, Swing, Intelligent Eye |
| Mold proof | `switch` | On/Off |
| Streamer | `binary_sensor` | display only |
| Powerful | `binary_sensor` | display only |
| Indoor temperature | `sensor` | °C |
| Indoor humidity | `sensor` | % |
| Outdoor temperature | `sensor` | °C |

The unit does not accept Streamer, Powerful, Econo or Outdoor Quiet over Wi-Fi; these can only be
switched with the remote. The unit does not report which direction Intelligent Eye is currently
blowing. Dry mode has no target temperature and no fan speed setting.

The unit is polled regularly (default: every 15 seconds) so that changes made with the remote
show up in Home Assistant.

If the built-in Daikin integration is set up for the same unit, remove it to avoid two
integrations controlling one device.

Tip: give the unit a fixed IP address in your router, so the integration keeps finding it.

## Installation via HACS

> **Note:** This is an integration, not an app (add-on). Adding the repository under
> Settings → Apps → Repositories fails with *"is not a valid app repository"*. Add it in
> **HACS** as described below.

1. HACS → menu in the top right → **Custom repositories**
2. Add `https://github.com/LeMec87/daikin-remote-control` with type **Integration**
3. Download **Daikin Remote Control** and restart Home Assistant
4. Settings → Devices & services → **Add integration** → *Daikin Remote Control*
5. Enter the IP address of the air conditioner and a name

The polling interval can be changed afterwards under **Configure** (5 to 300 seconds).
Entity names are available in English and German.

### Manual installation

Copy `custom_components/daikin_remote_control` into the `custom_components` folder of your
Home Assistant configuration and restart Home Assistant.

## Data points

Paths below `dgc_status`. `e_1002` is the indoor unit (`adr_0100`), `e_1003` the outdoor unit
(`adr_0200`).

| Function | Data point | Values |
|---|---|---|
| Power | `e_1002/e_A002/p_01` | `01` / `00` |
| Mode | `e_1002/e_3001/p_01` | `0200` cool, `0500` dry, `0000` fan only |
| Target temperature (cool) | `e_1002/e_3001/p_02` | half degrees, e.g. `34` = 26 °C |
| Fan speed | cool `p_09`, fan only `p_28` (in `e_1002/e_3001`) | `0A00` auto, `0B00` quiet, `0300`–`0700` = 1–5 |
| Vertical flap | cool `p_05`, dry `p_22`, fan only `p_24` | `01000000`–`05000000` positions, `0F000000` swing |
| Horizontal louvres | cool `p_06`, dry `p_23`, fan only `p_25` | `020000`–`080000` positions, `0F0000` swing, `100000` Intelligent Eye |
| Ceiling airflow | `e_1002/e_3003/p_1D` | `01` / `00` |
| Mold proof | `e_1002/e_3003/p_4D` | `01` / `00` |
| Streamer | `e_1002/e_3003/p_20` | read only |
| Powerful | `e_1003/e_3002/p_44` | read only |
| Indoor temperature | `e_1002/e_A00B/p_01` | signed byte, whole degrees |
| Indoor humidity | `e_1002/e_A00B/p_02` | percent |
| Outdoor temperature | `e_1003/e_A00D/p_01` | signed little-endian, half degrees |

Writes use `op 3` on the indoor unit; the unit confirms with `rsc 2004`.

## Contributing

Pull requests and model reports are welcome. The data points above were found by pressing each
button on the remote and comparing the unit's state before and after; the same method works for
other models.

## Credits

The per-mode data points for temperature, fan and swing follow
[pydaikin](https://github.com/fredrike/pydaikin), which the built-in Daikin integration uses.

## License

[MIT](LICENSE)
