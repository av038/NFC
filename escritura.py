#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('Dato nuevo:')
        print("Coloque la tajeta a editar...")
        reader.write(text)
        print("Tarjeta actualizada")
finally:
        GPIO.cleanup()
