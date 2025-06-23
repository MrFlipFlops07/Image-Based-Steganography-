import cv2
import numpy as np

# Convert message to binary
def message_to_binary(msg):
    return ''.join([format(ord(char), '08b') for char in msg])

# Convert binary to message
def binary_to_message(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''.join([chr(int(b, 2)) for b in chars])
    return message

# Encode message into image
def encode_message(image_path, message, output_path='output_image.png'):
    img = cv2.imread(image_path)
    if img is None:
        print("[-] Image not found. Check the file path.")
        return

    # Add delimiter
    delimiter = "$$END$$"
    full_msg = message + delimiter
    binary_msg = message_to_binary(full_msg)
    data_index = 0
    msg_len = len(binary_msg)

    for row in img:
        for pixel in row:
            for n in range(3):  # BGR
                if data_index < msg_len:
                    pixel[n] = (int(pixel[n]) & 254) | int(binary_msg[data_index])
                    data_index += 1
                else:
                    break

    cv2.imwrite(output_path, img)
    print(f"[+] Message encoded into {output_path}")

# Decode message from image
def decode_message(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("[-] Image not found. Check the file path.")
        return

    binary_msg = ''
    for row in img:
        for pixel in row:
            for n in range(3):
                binary_msg += str(pixel[n] & 1)

    # Split into 8-bit chunks
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    message = ''
    for b in chars:
        try:
            char = chr(int(b, 2))
        except:
            break
        message += char
        if "$$END$$" in message:
            break

    message = message.replace("$$END$$", "")
    print(f"[+] Decoded Message: {message}")
    return message

# Main menu
if __name__ == "__main__":
    mode = input("Enter mode (e to encode / d to decode): ").strip().lower()
    
    if mode == 'e':
        img_path = input("Enter path to image (PNG): ").strip()
        msg = input("Enter secret message: ").strip()
        encode_message(img_path, msg)
    
    elif mode == 'd':
        img_path = input("Enter path to stego image: ").strip()
        decode_message(img_path)
    
    else:
        print("Invalid mode. Use 'e' to encode or 'd' to decode.")