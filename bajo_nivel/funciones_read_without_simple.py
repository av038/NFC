#!/usr/bin/env python3

from mfrc522 import MFRC522
import time
import string

from CLAVES_NFC import *
reader = MFRC522()
MI_OK = reader.MI_OK


def wait_for_card(timeout=None):
    start = time.time()
    while True:
        (status, tagtype) = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status == MI_OK:
            return tagtype
        if timeout and (time.time() - start) > timeout:
            return None
        time.sleep(0.12)

def get_uid():
    (status, uid) = reader.MFRC522_Anticoll()
    if status == MI_OK:
        return uid
    return None

def select_tag(uid):
    try:
        return reader.MFRC522_SelectTag(uid)
    except Exception:
        return None

def auth_with_key(block_addr, key, uid):
    """Intenta autenticar block_addr con Key A (por defecto). uid debe ser lista; la librería espera 4 bytes en muchas implementaciones."""
    try:
        # la función devuelve MI_OK cuando autentica correctamente
        status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, block_addr, key, uid[:4])
        return status == MI_OK
    except Exception:
        return False

def read_block(block_addr):
    """Lee block_addr usando MFRC522_Read. Devuelve lista de 16 bytes o None."""
    try:
        data = reader.MFRC522_Read(block_addr)
        return data
    except Exception:
        return None

def is_printable_text(byte_list, min_len=4):
    """Devuelve True si en byte_list hay al menos min_len bytes imprimibles contiguos (ASCII)."""
    if not byte_list:
        return False
    s = ''.join(chr(b) if 32 <= b < 127 else '.' for b in byte_list)
    # cuenta secuencias imprimibles
    max_run = 0
    cur = 0
    for ch in s:
        if ch in string.printable and ch != '\t' and ch != '\n' and ch != '\r':
            cur += 1
            if cur > max_run:
                max_run = cur
        else:
            cur = 0
    return max_run >= min_len

def extract_printable(byte_list):
    """Intenta devolver la mejor cadena ASCII imprimible encontrada en byte_list."""
    if not byte_list:
        return ""
    s = ''.join(chr(b) if 32 <= b < 127 else ' ' for b in byte_list)
    # colapsa espacios múltiples y strip
    return ' '.join(s.split()).strip()

def scan_and_read(uid):
    """Para cada sector (0..15) intenta autenticar con keys comunes y leer los 4 bloques del sector.
       Imprime cualquier bloque que contenga texto imprimible."""
    print("UID:", ["%02X" % b for b in uid], "len:", len(uid))
    select_tag(uid)
    found_any = False
    for sector in range(16):
        sector_base = sector * 4
        authenticated = False
        used_key = None
        for key in COMMON_KEYS:
            if auth_with_key(sector_base, key, uid):
                authenticated = True
                used_key = key
                break
        if not authenticated:
            print(f"Sector {sector:02d}: Auth FAIL (claves comunes)")
            continue
        print(f"Sector {sector:02d}: Auth OK with key {''.join('%02X'%b for b in used_key)}")
        # leer 4 bloques del sector
        for block_offset in range(4):
            block_addr = sector_base + block_offset
            data = read_block(block_addr)
            # data puede ser None o lista de 16 ints
            if data is None:
                print(f"  Block {block_addr:02d}: READ FAIL")
                continue
            # muestra raw
            hexd = " ".join("%02X" % b for b in data)
            # comprobar si contiene texto imprimible
            if is_printable_text(data):
                text = extract_printable(data)
                print(f"  Block {block_addr:02d}: {hexd}  => TEXT: '{text}'")
                found_any = True
            else:
                print(f"  Block {block_addr:02d}: {hexd}")
        # limpiar estado crypto entre sectores
#        try:
#            reader.MFRC522_StopCrypto1()
#        except Exception:
#            pass
    return found_any
