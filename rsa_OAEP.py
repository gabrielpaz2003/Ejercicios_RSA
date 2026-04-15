from pathlib import Path

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

PASSPHRASE = "lab04uvg"


def cifrar_mensaje(mensaje):
    clave_publica = RSA.import_key(Path("public_key.pem").read_bytes())
    cifrador = PKCS1_OAEP.new(clave_publica)
    return cifrador.encrypt(mensaje)


def descifrar_mensaje(cifrado):
    clave_privada = RSA.import_key(
        Path("private_key.pem").read_bytes(),
        passphrase=PASSPHRASE,
    )
    descifrador = PKCS1_OAEP.new(clave_privada)
    return descifrador.decrypt(cifrado)


def main():
    mensaje = b"Clave AES del documento legal"

    cifrado_1 = cifrar_mensaje(mensaje)
    cifrado_2 = cifrar_mensaje(mensaje)
    descifrado = descifrar_mensaje(cifrado_1)

    print("Mensaje original:", mensaje.decode())
    print("Primer cifrado :", cifrado_1.hex()[:80] + "...")
    print("Segundo cifrado:", cifrado_2.hex()[:80] + "...")
    print("Descifrado     :", descifrado.decode())
    print("Los dos cifrados son iguales:", cifrado_1 == cifrado_2)


if __name__ == "__main__":
    main()
