from tinyec import registry
import secrets
import hashlib

curve = registry.get_curve('brainpoolP256r1')

def encrypt_ECC(msg, pubKey):
    msg_int = int.from_bytes(hashlib.sha256(msg.encode()).digest(), 'big')
    k = secrets.randbelow(curve.field.n)
    C1 = k * curve.g
    C2 = msg_int * curve.g + k * pubKey
    return C1, C2

def decrypt_ECC(C1, C2, privKey):
    shared = privKey * C1
    msg_point = C2 - shared
    return msg_point

def generate_keys():
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g
    return privKey, pubKey
