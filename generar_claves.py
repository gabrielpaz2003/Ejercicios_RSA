from pathlib import Path

from Crypto.PublicKey import RSA

PASSPHRASE = "lab04uvg"


def generar_claves(bits=3072):
    clave = RSA.generate(bits)

    clave_privada = clave.export_key(
        pkcs=8,
        passphrase=PASSPHRASE,
        protection="scryptAndAES128-CBC",
    )
    clave_publica = clave.publickey().export_key()

    Path("private_key.pem").write_bytes(clave_privada)
    Path("public_key.pem").write_bytes(clave_publica)


def main():
    generar_claves()
    print("Se genero private_key.pem")
    print("Se genero public_key.pem")
    print("Passphrase de la clave privada: lab04uvg")


if __name__ == "__main__":
    main()
