# Daikin Remote Control

Home Assistant integration for the Daikin remote control functions that the built-in Daikin
integration does not offer. Tested with an **FTKZ25VVMV** (remote ARC466A63) and a Wi-Fi adapter
that speaks the **dsiot API** (`POST /dsiot/multireq`).

The built-in Daikin integration stays in charge of power, mode, temperature, fan speed and swing.
Daikin Remote Control adds:

| Entity | Type | Function |
|---|---|---|
| Airflow up/down | `select` | Highest, High, Middle, Low, Lowest, Swing, Ceiling |
| Airflow left/right | `select` | Far left … Far right, Swing, Intelligent Eye |
| Mold proof | `switch` | On/Off |
| Streamer | `binary_sensor` | display only |
| Powerful | `binary_sensor` | display only |

The unit does not accept Streamer, Powerful, Econo or Outdoor Quiet over Wi-Fi; these can only be
switched with the remote. The unit does not report which direction Intelligent Eye is currently
blowing.

The unit is polled regularly (default: every 15 seconds) so that changes made with the remote
show up in Home Assistant.

## Installation via HACS

1. HACS → menu in the top right → **Custom repositories**
2. Add `https://github.com/LeMec87/daikin-remote-control` with type **Integration**
3. Download **Daikin Remote Control** and restart Home Assistant
4. Settings → Devices & services → **Add integration** → *Daikin Remote Control*
5. Enter the IP address of the air conditioner and a name

The polling interval can be changed afterwards under **Configure** (5 to 300 seconds).
Entity names are available in English and German.

## Data points

All on the indoor unit `adr_0100.dgc_status`, group `e_1002`, except Powerful.

| Function | Data point | Values |
|---|---|---|
| Vertical flap | `e_3001/p_05` | `01000000`–`05000000` positions, `0F000000` swing |
| Horizontal louvres | `e_3001/p_06` | `020000`–`080000` positions, `0F0000` swing, `100000` Intelligent Eye |
| Ceiling airflow | `e_3003/p_1D` | `01` / `00` |
| Mold proof | `e_3003/p_4D` | `01` / `00` |
| Streamer | `e_3003/p_20` | read only |
| Powerful | outdoor unit `adr_0200`, `e_1003/e_3002/p_44` | read only |

Writes use `op 3`; the unit confirms with `rsc 2004`.
