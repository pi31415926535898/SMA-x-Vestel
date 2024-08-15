# SMA-x-Vestel
Energiemanagment zwischen SMA Wechselrichtern und der Wallbox "EVC 04" von Vestel mittels Modbus-Protokoll.
## Features

- Auslesen der Wechselrichterleistung alle 10 Sekunden
- Aktualisieren der Wallboxausgangsleistung ein mal pro Minute
- Anpassung der Ausgangsleistung auf die aktuelle Wechselrichterleistung

## Installation

Sowohl für die Wallbox als auch für den Wechselrichter muss das Modbus-Protokoll aktiviert sein. Dafür auf die jeweilige Benutzeroberfläche gehen.

Für Windows gibt es eine ".exe" zum Download unter "Releases". Andernfalls muss die Python-Datei, sowie die Konfig-Datei heruntergeladen werden.

In die Konfigurationsdatei müssen IP und Port für beide Geräte festgelegt werden. Der Standardport ist 502.
Man findet die Konfig-Datei für den Windows Release unter "_internal" und "Konfiguration_SMA x Vestel.ini".

Das Programm sollte ständig laufen. Wird es unterbrochen, lädt die Wallbox nach 10 Minuten Kommunikationsausfall wieder standardmäßg mit der maximalen Ladeleistung.

#### Für die Python-Datei muss Python installiert sein (3.11+). Außerdem die Bibliothek "pymodbus".
```bash
  pip install pymodbus 
```
