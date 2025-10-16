#!/usr/bin/env python3
# read_without_simple.py
# Lee una tarjeta MIFARE Classic 1K en modo solo-lectura sin usar SimpleMFRC522 wrapper.
# Busca en todos los bloques accesibles con claves comunes y decodifica texto imprimible.

import RPi.GPIO as GPIO

from funciones_read_without_simple import *


def main():
    try:
        print("Acerca la tarjeta...")
        tagtype = wait_for_card(timeout=12)
        if not tagtype:
            print("No se detectó tarjeta (timeout).")
            return
        uid = get_uid()
        if not uid:
            print("No UID detectado.")
            return
        # escanear sectores y buscar texto
        any_text = scan_and_read(uid)
        if not any_text:
            print("\nNo se detectó texto imprimible en los bloques accesibles con claves comunes.")
        else:
            print("\nLectura finalizada. Si viste el texto esperado, ya está OK.")
    finally:
        try:
            reader.MFRC522_StopCrypto1()
        except Exception:
            pass
        GPIO.cleanup()

if __name__ == "__main__":
    main()

