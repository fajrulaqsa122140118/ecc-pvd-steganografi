from ecc_utils import generate_keys, encrypt_ECC
from pvd_stego import embed_msg, extract_msg
from skimage.metrics import structural_similarity as ssim

# ✅ Inisialisasi kunci dan input plaintext
plaintext = "SAYA CINTA KODE ECC DAN STEGANOGRAFI"
privKey, pubKey = generate_keys()

import time
start = time.time()  # ⏱️ Mulai pengukuran waktu enkripsi

# 🔐 Enkripsi plaintext menggunakan ECC → menghasilkan titik C1 dan C2
C1, C2 = encrypt_ECC(plaintext, pubKey)
print("⏱️ Waktu enkripsi ECC:", round(time.time() - start, 6), "detik")  # ⏱️ Selesai pengukuran

# 🔐 Format titik ECC menjadi string dan encode ke byte
ct_str = f"{C1.x},{C1.y},{C2.x},{C2.y}"
ct_bytes = ct_str.encode('utf-8')

# ℹ️ Tampilkan ukuran ciphertext dalam byte dan panjang string
print("🔢 Ukuran ciphertext (byte):", len(ct_bytes))
print("🧾 Panjang string ciphertext:", len(ct_str))

# 🔃 Konversi byte ciphertext menjadi string biner
bin_data = ''.join(format(byte, '08b') for byte in ct_bytes)

# 🖨️ Tampilkan isi ciphertext dalam bentuk string (sebelum disisipkan)
print("🔐 Ciphertext ECC sebelum embedding:")
print(ct_str)
print("📎 Menggunakan test_gray.png untuk embedding")

from ecc_encoder import hamming_encode, add_checksum, hamming_decode, verify_checksum, evaluate_psnr

# 🛡️ Lindungi data dengan Hamming Code dan tambahkan checksum
protected = hamming_encode(bin_data)
final_bits = add_checksum(protected)

# 💾 Sisipkan bit yang telah dilindungi ke dalam gambar grayscale menggunakan metode PVD
embed_msg("../images/test_gray.png", final_bits, "../images/stego.png")

# 📏 Hitung kapasitas penyisipan yang digunakan (dari total kapasitas PVD gambar)
from PIL import Image
import numpy as np

gray_img = Image.open("../images/test_gray.png").convert('L')
flat = np.array(gray_img).flatten()

max_capacity = (len(flat) // 2) * 4
used_capacity = len(final_bits)
print("💡 Rasio penggunaan kapasitas:", round(used_capacity / max_capacity * 100, 2), "%")

# 📈 Evaluasi kualitas visual dengan PSNR
psnr = evaluate_psnr("../images/test_gray.png", "../images/stego.png")
print(f"📈 PSNR antara gambar asli dan stego: {psnr:.2f} dB")

# 🔍 Evaluasi kualitas visual dengan SSIM
try:
    img1 = Image.open("../images/test_gray.png").convert("L")
    img2 = Image.open("../images/stego.png").convert("L")

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    ssim_score, _ = ssim(arr1, arr2, channel_axis=None, full=True)  # type: ignore # ⬅️ Fix ini penting!
    print("📊 SSIM antara gambar asli dan stego:", round(ssim_score, 4))

except Exception as e:
    print("❌ Gagal menghitung SSIM:", e)

# 📤 Ekstraksi bit dari gambar stego (jumlah bit sama seperti yang disisipkan)
bit_len = len(bin_data)
bits_out = extract_msg("../images/stego.png", bit_len)

# 🧾 Tampilkan ringkasan hasil ekstraksi bit
print(f"🔢 Diharapkan bit_len: {bit_len}")
print(f"🧾 Panjang bits_out: {len(bits_out)}")
print(f"🧾 Contoh bits_out: {bits_out[:64]}...")

# 🧠 Bandingkan hasil ekstraksi dengan ciphertext asli (dalam bentuk byte)
try:
    cutoff = len(bits_out) - (len(bits_out) % 8)
    extracted_bytes = bytearray(int(bits_out[i:i+8], 2) for i in range(0, cutoff, 8))

    if extracted_bytes == ct_bytes:
        print("✅ ECC ciphertext berhasil disisipkan dan diekstrak kembali secara utuh!")
    else:
        print("❌ Ciphertext tidak cocok setelah ekstraksi.")
        print("📤 Original (bytes):", ct_bytes)
        print("📥 Extracted (bytes):", extracted_bytes)

except Exception as e:
    print("❌ Terjadi kesalahan saat konversi bit ke byte.")
    print("🔍 Error:", e)
