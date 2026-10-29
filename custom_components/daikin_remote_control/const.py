"""Constants and data points of the Daikin dsiot API.

Values were mapped with the ARC466A63 remote on an FTKZ25VVMV.
"""

DOMAIN = "daikin_remote_control"
DEFAULT_SCAN_INTERVAL = 15

INDOOR = "/dsiot/edge/adr_0100.dgc_status"
OUTDOOR = "/dsiot/edge/adr_0200.dgc_status"

# Vertical flap: e_1002/e_3001/p_05
VERTICAL = {
    "01000000": "highest",
    "02000000": "high",
    "03000000": "middle",
    "04000000": "low",
    "05000000": "lowest",
    "0F000000": "swing",
}
CEILING = "ceiling"  # Ceiling airflow is a separate flag: e_3003/p_1D

# Horizontal louvres: e_1002/e_3001/p_06
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
