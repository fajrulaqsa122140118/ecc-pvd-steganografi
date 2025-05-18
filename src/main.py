from ecc_utils import generate_keys, encrypt_ECC
from pvd_stego import embed_msg, extract_msg
from PIL import Image

# 🔄 Konversi test.png ke grayscale dan simpan sebagai test_gray.png
Image.open("images/test.png").convert("L").save("images/test_gray.png")

# ✅ Setup
plaintext = "SAYA CINTA KODE ECC DAN STEGANOGRAFI"
privKey, pubKey = generate_keys()
C1, C2 = encrypt_ECC(plaintext, pubKey)

# 🔐 Encode titik ECC sebagai byte
ct_str = f"{C1.x},{C1.y},{C2.x},{C2.y}"
ct_bytes = ct_str.encode('utf-8')
bin_data = ''.join(format(byte, '08b') for byte in ct_bytes)

print("🔐 Ciphertext ECC sebelum embedding:")
print(ct_str)
print("📎 Menggunakan test_gray.png untuk embedding")

# 🖼️ Steganografi: Penyisipan
embed_msg("images/test_gray.png", bin_data, "images/stego.png")

# 📤 Ekstraksi
bit_len = len(bin_data)
bits_out = extract_msg("images/stego.png", bit_len)

print(f"🔢 Diharapkan bit_len: {bit_len}")
print(f"🧾 Panjang bits_out: {len(bits_out)}")
print(f"🧾 Contoh bits_out: {bits_out[:64]}...")

# 🧠 Perbandingan byte hasil ekstraksi dengan byte asli
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
