"""Constants and data points of the Daikin dsiot API.

Values were mapped with the ARC466A63 remote on an FTKZ25VVMV.
Data point keys are paths below dgc_status: e_1002 is the indoor unit, e_1003 the outdoor unit.
"""

DOMAIN = "daikin_remote_control"
DEFAULT_SCAN_INTERVAL = 15

INDOOR = "/dsiot/edge/adr_0100.dgc_status"
OUTDOOR = "/dsiot/edge/adr_0200.dgc_status"

POWER = "e_1002/e_A002/p_01"
MODE = "e_1002/e_3001/p_01"
CEILING_AIRFLOW = "e_1002/e_3003/p_1D"
MOLD_PROOF = "e_1002/e_3003/p_4D"
STREAMER = "e_1002/e_3003/p_20"
POWERFUL = "e_1003/e_3002/p_44"
INDOOR_TEMP = "e_1002/e_A00B/p_01"
INDOOR_HUMIDITY = "e_1002/e_A00B/p_02"
OUTDOOR_TEMP = "e_1003/e_A00D/p_01"

MODE_COOL = "0200"
MODE_DRY = "0500"
MODE_FAN = "0000"

# Target temperature, fan speed and airflow direction are stored per mode
MODE_POINTS = {
    MODE_COOL: {
        "temperature": "e_1002/e_3001/p_02",
        "fan": "e_1002/e_3001/p_09",
        "vertical": "e_1002/e_3001/p_05",
        "horizontal": "e_1002/e_3001/p_06",
    },
    MODE_DRY: {
        "temperature": None,
        "fan": None,
        "vertical": "e_1002/e_3001/p_22",
        "horizontal": "e_1002/e_3001/p_23",
    },
    MODE_FAN: {
        "temperature": None,
        "fan": "e_1002/e_3001/p_28",
        "vertical": "e_1002/e_3001/p_24",
        "horizontal": "e_1002/e_3001/p_25",
    },
}

COOL_MIN_TEMP = 18.0
COOL_MAX_TEMP = 32.0

FAN_SPEEDS = {
    "0A00": "Auto",
    "0B00": "Quiet",
    "0300": "1",
    "0400": "2",
    "0500": "3",
    "0600": "4",
    "0700": "5",
}

SWING_ON = "0F"

# Vertical flap positions
VERTICAL = {
    "01000000": "highest",
    "02000000": "high",
    "03000000": "middle",
    "04000000": "low",
    "05000000": "lowest",
    "0F000000": "swing",
}
VERTICAL_MIDDLE = "03000000"
CEILING = "ceiling"  # Ceiling airflow is a separate flag, see CEILING_AIRFLOW

# Horizontal louvre positions
HORIZONTAL = {
    "020000": "far_left",
    "030000": "left",
    "040000": "left_center",
    "050000": "center",
    "060000": "right_center",
    "070000": "right",
    "080000": "far_right",
    "0F0000": "swing",
    "100000": "intelligent_eye",
}
HORIZONTAL_CENTER = "050000"
