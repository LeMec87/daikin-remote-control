# Daikin Extra

Home-Assistant-Integration für die Funktionen der Daikin-Fernbedienung, die die eingebaute
Daikin-Integration nicht kann. Getestet mit einer **FTKZ25VVMV** (Fernbedienung ARC466A63) und
einem WLAN-Adapter mit der **dsiot-API** (`POST /dsiot/multireq`).

Die Daikin-Integration bleibt für Ein/Aus, Modus, Temperatur, Lüfter und Schwenken zuständig.
Daikin Extra ergänzt sie um:

| Entität | Typ | Funktion |
|---|---|---|
| Luft oben/unten | `select` | Ganz oben, Oben, Mitte, Unten, Ganz unten, Schwenken, Zur Decke |
| Luft links/rechts | `select` | Ganz links … Ganz rechts, Schwenken, Intelligent Eye |
| Schimmelschutz | `switch` | Ein/Aus |
| Streamer | `binary_sensor` | nur Anzeige |
| Powerful | `binary_sensor` | nur Anzeige |

Streamer, Powerful, Econo und Quiet außen nimmt die Anlage über WLAN nicht an; die schaltet nur
die Fernbedienung. Die Richtung, in die Intelligent Eye gerade bläst, meldet die Anlage nicht.

Die Anlage wird regelmäßig gelesen (Standard: alle 15 Sekunden), damit Änderungen über die
Fernbedienung auch in Home Assistant ankommen.

## Installation über HACS

1. HACS → Menü oben rechts → **Benutzerdefinierte Repositories**
2. Repository `https://github.com/LeMec87/daikin-extra`, Typ **Integration**, hinzufügen
3. **Daikin Extra** herunterladen und Home Assistant neu starten
4. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → *Daikin Extra*
5. IP-Adresse der Klimaanlage und einen Namen eingeben

Die Abfragezeit lässt sich danach unter **Konfigurieren** ändern (5 bis 300 Sekunden).

## Datenpunkte

Alle am Innengerät `adr_0100.dgc_status`, Gruppe `e_1002`, außer Powerful.

| Funktion | Datenpunkt | Werte |
|---|---|---|
| Klappe oben/unten | `e_3001/p_05` | `01000000`–`05000000` Positionen, `0F000000` Schwenken |
| Lamellen links/rechts | `e_3001/p_06` | `020000`–`080000` Positionen, `0F0000` Schwenken, `100000` Intelligent Eye |
| Luft zur Decke | `e_3003/p_1D` | `01` / `00` |
| Schimmelschutz | `e_3003/p_4D` | `01` / `00` |
| Streamer | `e_3003/p_20` | nur lesbar |
| Powerful | Außengerät `adr_0200`, `e_1003/e_3002/p_44` | nur lesbar |

Geschrieben wird mit `op 3`; die Anlage bestätigt mit `rsc 2004`.
