import base64
import json
import sys
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from rsa_OAEP import cifrar_mensaje, descifrar_mensaje


def texto_a_base64(datos):
    return base64.b64encode(datos).decode("utf-8")


def base64_a_texto(datos):
    return base64.b64decode(datos.encode("utf-8"))


def cifrar_documento(ruta_documento):
    documento = Path(ruta_documento).read_bytes()
    clave_aes = get_random_bytes(32)

    cifrador_aes = AES.new(clave_aes, AES.MODE_GCM)
    ciphertext, tag = cifrador_aes.encrypt_and_digest(documento)

    paquete = {
        "archivo_original": Path(ruta_documento).name,
        "clave_aes_cifrada": texto_a_base64(cifrar_mensaje(clave_aes)),
        "nonce": texto_a_base64(cifrador_aes.nonce),
        "tag": texto_a_base64(tag),
        "ciphertext": texto_a_base64(ciphertext),
    }

    return paquete


def descifrar_paquete(paquete):
    clave_aes = descifrar_mensaje(base64_a_texto(paquete["clave_aes_cifrada"]))
    nonce = base64_a_texto(paquete["nonce"])
    tag = base64_a_texto(paquete["tag"])
    ciphertext = base64_a_texto(paquete["ciphertext"])

    descifrador_aes = AES.new(clave_aes, AES.MODE_GCM, nonce=nonce)
    return descifrador_aes.decrypt_and_verify(ciphertext, tag)


def main():
    ruta_documento = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("documentos_demo/contrato_guatemala.txt")
    )

    salida = Path("salida")
    salida.mkdir(exist_ok=True)

    paquete = cifrar_documento(ruta_documento)
    ruta_paquete = salida / "paquete_cifrado.json"
    ruta_paquete.write_text(json.dumps(paquete, indent=2), encoding="utf-8")

    documento_descifrado = descifrar_paquete(paquete)
    ruta_descifrado = salida / f"{ruta_documento.stem}_descifrado{ruta_documento.suffix}"
    ruta_descifrado.write_bytes(documento_descifrado)

    print("Documento usado :", ruta_documento)
    print("Paquete cifrado :", ruta_paquete)
    print("Documento final :", ruta_descifrado)
    print("Coinciden       :", documento_descifrado == ruta_documento.read_bytes())


if __name__ == "__main__":
    main()
