from PIL import Image
import numpy as np

def embed_msg(image_path, data_bits, out_path):
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    flat = arr.flatten()

    print("[INFO] Bit yang akan disisipkan:", len(data_bits))
    print("[INFO] Jumlah piksel:", len(flat))
    print("[INFO] Estimasi maksimum bit (approx):", (len(flat) // 2) * 4)

    i = 0
    bit_idx = 0
    while bit_idx < len(data_bits) and i < len(flat) - 1:
        p1, p2 = int(flat[i]), int(flat[i+1])
        d = abs(p1 - p2)
        if d < 16:
            bits_to_embed = 2
        elif d < 32:
            bits_to_embed = 3
        else:
            bits_to_embed = 4

        bits = data_bits[bit_idx:bit_idx + bits_to_embed]
        if len(bits) < bits_to_embed:
            bits += '0' * (bits_to_embed - len(bits))

        embed_val = int(bits, 2)
        avg = (p1 + p2) // 2
        flat[i] = np.clip(avg - embed_val // 2, 0, 255)
        flat[i + 1] = np.clip(avg + embed_val // 2, 0, 255)

        bit_idx += bits_to_embed
        i += 2

    if bit_idx < len(data_bits):
        print(f"⚠️ Warning: {len(data_bits) - bit_idx} bit tidak disisipkan (melebihi kapasitas gambar)")

    new_img = Image.fromarray(flat.reshape(arr.shape).astype(np.uint8))
    new_img.save(out_path)
    print(f"✅ Gambar stego berhasil disimpan: {out_path}")


def extract_msg(image_path, bit_len):
    img = Image.open(image_path).convert('L')
    arr = np.array(img)
    flat = arr.flatten()

    max_possible = (len(flat) // 2) * 4
    if bit_len > max_possible:
        print(f"❌ bit_len terlalu besar! Maksimum {max_possible} bit bisa diekstrak.")
        return ""

    i = 0
    bits_out = ''
    while len(bits_out) < bit_len and i < len(flat) - 1:
        p1, p2 = int(flat[i]), int(flat[i+1])
        d = abs(p1 - p2)
        if d < 16:
            bits_to_read = 2
        elif d < 32:
            bits_to_read = 3
        else:
            bits_to_read = 4

        diff = abs(p1 - p2)
        bits = bin(diff)[2:].zfill(bits_to_read)
        bits_out += bits
        i += 2

    if len(bits_out) < bit_len:
        print(f"⚠️ Ekstraksi gagal: hanya {len(bits_out)} dari {bit_len} bit yang berhasil dibaca.")

    return bits_out[:bit_len]
