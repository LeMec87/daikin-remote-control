# Daikin Remote Control

Standalone Home Assistant integration for Daikin air conditioners with a Wi-Fi adapter that
speaks the **dsiot API** (`POST /dsiot/multireq`). It covers everything the remote control can
switch over Wi-Fi, so the built-in Daikin integration is not needed.

Tested with an **FTKZ25VVMV** (remote ARC466A63, cooling only).

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

## Installation via HACS

1. HACS → menu in the top right → **Custom repositories**
2. Add `https://github.com/LeMec87/daikin-remote-control` with type **Integration**
3. Download **Daikin Remote Control** and restart Home Assistant
4. Settings → Devices & services → **Add integration** → *Daikin Remote Control*
5. Enter the IP address of the air conditioner and a name

The polling interval can be changed afterwards under **Configure** (5 to 300 seconds).
Entity names are available in English and German.

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
