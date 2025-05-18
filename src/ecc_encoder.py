# ecc_encoder.py
# Modul ini berisi: Hamming Encode + Decode, Fragmentasi, dan Proteksi untuk ECC Ciphertext

from typing import List

# Hamming(7,4) encoding

def hamming_encode(bits: str) -> str:
    def encode_block(block: str) -> str:
        d = list(map(int, block.ljust(4, '0')))
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p3 = d[1] ^ d[2] ^ d[3]
        return f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}"

    return ''.join(encode_block(bits[i:i+4]) for i in range(0, len(bits), 4))

# Hamming(7,4) decoding

def hamming_decode(bits: str) -> str:
    def decode_block(block: str) -> str:
        b = list(map(int, block))
        p1 = b[0] ^ b[2] ^ b[4] ^ b[6]
        p2 = b[1] ^ b[2] ^ b[5] ^ b[6]
        p3 = b[3] ^ b[4] ^ b[5] ^ b[6]
        error = p1 * 1 + p2 * 2 + p3 * 4
        if error != 0:
            b[error-1] ^= 1
        return f"{b[2]}{b[4]}{b[5]}{b[6]}"

    return ''.join(decode_block(bits[i:i+7]) for i in range(0, len(bits), 7))

# Bit fragmentation (optional if needed)
def fragment_bits(bits: str, chunk_size: int = 64) -> List[str]:
    return [bits[i:i+chunk_size] for i in range(0, len(bits), chunk_size)]

# Add checksum (8-bit count of 1s)
def add_checksum(bits: str) -> str:
    count = bits.count('1') % 256
    checksum = format(count, '08b')
    return bits + checksum

# Verify checksum

def verify_checksum(bits: str) -> bool:
    if len(bits) < 8:
        return False
    payload, checksum = bits[:-8], bits[-8:]
    count = payload.count('1') % 256
    return format(count, '08b') == checksum

# PSNR evaluation between original and stego images

def evaluate_psnr(original_path: str, stego_path: str) -> float:
    from PIL import Image
    import numpy as np
    from skimage.metrics import peak_signal_noise_ratio

    ori = np.array(Image.open(original_path).convert('L'))
    stego = np.array(Image.open(stego_path).convert('L'))
    return peak_signal_noise_ratio(ori, stego)
