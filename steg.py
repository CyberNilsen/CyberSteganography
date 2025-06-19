from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_message(message: str, password: str) -> bytes:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    
    encrypted = base64.b64encode(salt + iv + ct)
    return encrypted

def decrypt_message(encrypted: bytes, password: str) -> str:
    try:
        data = base64.b64decode(encrypted)
        salt, iv, ct = data[:16], data[16:32], data[32:]
        key = derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ct) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data.decode()
    except Exception as e:
        raise ValueError("Incorrect password or corrupted data")

def to_bin(data):
    if isinstance(data, str):
        data = data.encode()

    return ''.join(format(byte, '08b') for byte in data) + ''.join(format(ord(c), '08b') for c in "##END##")

def encode_text(image_path, message, output_path, password=None):
    if password:
        message = encrypt_message(message, password).decode()
    img = Image.open(image_path)
    binary = to_bin(message)
    data = iter(img.getdata())
    
    new_pixels = []
    for i in range(0, len(binary), 3):
        pixel = list(next(data))
        for j in range(3):
            if i + j < len(binary):
                pixel[j] = pixel[j] & ~1 | int(binary[i + j])
        new_pixels.append(tuple(pixel))
    img.putdata(new_pixels + list(data))
    img.save(output_path)

def decode_text(image_path, password=None):
    img = Image.open(image_path)
    data = iter(img.getdata())

    bits = []
    end_marker = "##END##"
    end_marker_bin = ''.join(format(ord(c), '08b') for c in end_marker)

    while True:
        try:
            pixel = next(data)
        except StopIteration:
            break

        for val in pixel[:3]:
            bits.append(str(val & 1))

            if len(bits) >= len(end_marker_bin):
                last_bits = bits[-len(end_marker_bin):]

                chars = []
                for i in range(0, len(last_bits), 8):
                    byte = last_bits[i:i+8]
                    chars.append(chr(int(''.join(byte), 2)))
                if ''.join(chars) == end_marker:
                    break
        else:
            continue 
        break 

    message_bits = bits[:-len(end_marker_bin)]
    chars = []
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(''.join(byte), 2)))

    msg = ''.join(chars)

    if password:
        msg = decrypt_message(msg.encode(), password)

    return msg
