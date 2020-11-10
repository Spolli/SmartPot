#!/usr/bin/env python3

import serial

pinSetup = {
    'PIN_MISC': 13,
    'PIN_WATER_WARM': 12,
    'PIN_VENT_OUT': 11,
    'PIN_VENT_IN': 10,
    'PIN_LAMPS': 9,
    'PIN_POMPA': 8
}

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

def PumpOn():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_POMPA"]};1\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def PumpOff():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_POMPA"]};0\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def VentInOn():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_VENT_IN"]};1\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def VentInOff():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_VENT_IN"]};0\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def VentOutOn():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_VENT_OUT"]};1\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def VentOutOff():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_VENT_OUT"]};0\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def LampOn():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_LAMPS"]};1\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def LampOff():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_LAMPS"]};0\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def WaterWarmOn():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_WATER_WARM"]};1\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')

def WaterWarmOff():
    if ser.in_waiting > 0:
        ser.write(f'{pinSetup["PIN_WATER_WARM"]};0\n'.encode())
    else:
        raise Exception('Connessione seriale non disponibile')