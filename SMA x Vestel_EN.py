from pymodbus.client import ModbusTcpClient
import time
from datetime import datetime
import configparser
import os

def log_message(message):
    now = datetime.now()
    print(now.strftime("%H:%M:%S") + ": " + message)

log_message("Code started!")
print()

def create_client(ip, port):
    client = ModbusTcpClient(ip, port=port)
    if not client.connect():
        log_message(f"Connection to {ip}:{port} failed!")
        return None
    return client

# Relativer Pfad zur Konfigurationsdatei
config_path = os.path.join(os.path.dirname(__file__), 'config_SMA x Vestel.ini')

# Konfigurationsdatei lesen
config = configparser.ConfigParser()
config.read(config_path)

PV_IP = config['Modbus']['PV_IP']
PV_Port = int(config['Modbus']['PV_Port'])
Wall_IP = config['Modbus']['Wall_IP']
Wall_Port = int(config['Modbus']['Wall_Port'])

client_PV = create_client(PV_IP, PV_Port)
client_Wall = create_client(Wall_IP, Wall_Port)

if client_Wall:
    client_Wall.write_register(2002, 600)

def read_registers(client, address, count):
    result = client.read_holding_registers(address, count)
    if result.isError():
        log_message(f"Error while reading register: {address}: {result}")
        return None
    return result.registers

def PV_Leistung_aktuell():
    if not client_PV:
        log_message("No connection to the inverter available!")
        return None

    registers_PV_Bat = read_registers(client_PV, 30775, 2)
    if registers_PV_Bat is None:
        return None
    PV_Bat = (registers_PV_Bat[0] << 16) + registers_PV_Bat[1]

    registers_Bat = read_registers(client_PV, 31395, 2)
    if registers_Bat is None:
        return None
    Bat = (registers_Bat[0] << 16) + registers_Bat[1]

    return PV_Bat - Bat

def Wallbox(Amps):
    if not client_Wall:
        log_message("No connection to the wallbox available!")
        return

    log_message(f"Wallbox-Leistung: {round(Amps, None) * 690} W")
    client_Wall.write_register(5004, round(Amps, None))
    print()

def Stromberechnung():
    PV_Leistungen = []
    for _ in range(5):
        PV_Leistung = PV_Leistung_aktuell()
        if PV_Leistung is not None:
            PV_Leistungen.append(PV_Leistung)
        time.sleep(10)
    
    if PV_Leistungen:
        PV_Leistung = sum(PV_Leistungen) / len(PV_Leistungen)
        log_message(f"PV-Leistung: {round(PV_Leistung, 2)} W")
        Amps = PV_Leistung / 690
        Amps = max(1, min(16, Amps))
        Wallbox(Amps)
    else:
        log_message("No connection to the inverter available!")

try:
    while True:
        Stromberechnung()
        time.sleep(10)
finally:
    if client_PV:
        client_PV.close()
    if client_Wall:
        client_Wall.close()