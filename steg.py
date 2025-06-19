from PIL import Image

def to_bin(message):
    """Convert text to binary with an END marker."""
    return ''.join(format(ord(i), '08b') for i in message + "##END##")

def encode_text(image_path, message, output_path):
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

    new_pixels.extend(data)  
    img.putdata(new_pixels)
    img.save(output_path)

def decode_text(image_path):
    img = Image.open(image_path)
    data = img.getdata()

    bits = ""
    for pixel in data:
        for value in pixel[:3]:
            bits += str(value & 1)

    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    msg = ""
    for b in chars:
        try:
            char = chr(int(b, 2))
            msg += char
            if msg.endswith("##END##"):
                return msg.replace("##END##", "")
        except:
            break 
    return "No hidden message found."
