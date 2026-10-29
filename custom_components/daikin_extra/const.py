"""Konstanten und Datenpunkte der Daikin-dsiot-API.

Die Werte sind mit der Fernbedienung ARC466A63 an einer FTKZ25VVMV ermittelt.
"""

DOMAIN = "daikin_extra"
STANDARD_TAKT = 15

INNEN = "/dsiot/edge/adr_0100.dgc_status"
AUSSEN = "/dsiot/edge/adr_0200.dgc_status"

# Klappe oben/unten: e_1002/e_3001/p_05
OBEN_UNTEN = {
    "01000000": "highest",
    "02000000": "high",
    "03000000": "middle",
    "04000000": "low",
    "05000000": "lowest",
    "0F000000": "swing",
}
DECKE = "ceiling"  # Luft zur Decke: eigener Schalter e_3003/p_1D

# Lamellen links/rechts: e_1002/e_3001/p_06
LINKS_RECHTS = {
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
