# Ejercicio RSA

Repositorio para el laboratorio de RSA del curso **Cifrado de Informacion**.

La solucion se organizo en scripts pequenos para que cada parte del ejercicio se pueda ejecutar y explicar por separado, igual que en el laboratorio de hashes y firmas.

## Objetivo

Este proyecto cubre los siguientes temas:

- generacion de claves RSA en formato PEM
- cifrado y descifrado directo con RSA-OAEP
- cifrado hibrido con RSA-OAEP + AES-256-GCM
- diferencias entre PKCS#1 v1.5 y OAEP
- uso de RSA en TLS 1.3, certificados X.509 y SSH

## Prompt utilizado

Si se quiere dejar constancia del apoyo recibido, un prompt transparente para este proyecto seria el siguiente:

```text
Necesito ayuda con mi ejercicio de RSA. Quiero un folder completo, con codigo sencillo, README claro, ejemplos de ejecucion y respuestas cortas de analisis, siguiendo el mismo estilo del ejercicio de Hashes y Firmas.
```

## Estructura del proyecto

```text
EjercicioRSA/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- generar_claves.py
|-- rsa_OAEP.py
|-- rsa_AES_GCM.py
|-- Ejercicio RSA.pdf
|-- documentos_demo/
|   |-- contrato_guatemala.txt
|   |-- acuerdo_miami.txt
|   `-- nda_madrid.txt
`-- tests/
    `-- test_pending.py
```

## Requisitos

- Python 3.10 o superior
- `pip`

## Instalacion

Desde la carpeta raiz del proyecto:

```bash
py -3 -m pip install -r requirements.txt
```

Dependencias:

- `pycryptodome`
- `pytest`

## Como ejecutar

Todos los scripts se ejecutan desde la carpeta raiz del proyecto.

### Comando base

```bash
py -3 nombre_del_script.py
```

### Orden sugerido

1. `py -3 generar_claves.py`
2. `py -3 rsa_OAEP.py`
3. `py -3 rsa_AES_GCM.py`

### Scripts disponibles

| Script | Que hace |
|---|---|
| `generar_claves.py` | Genera `private_key.pem` protegida con la passphrase `lab04uvg` y `public_key.pem`. |
| `rsa_OAEP.py` | Cifra y descifra un mensaje corto con RSA-OAEP y demuestra que dos cifrados del mismo mensaje no salen iguales. |
| `rsa_AES_GCM.py` | Cifra un archivo con AES-256-GCM, cifra la clave AES con RSA-OAEP y luego recupera el archivo original. |

### Ejemplos de ejecucion

Generar las claves:

```bash
py -3 generar_claves.py
```

Probar RSA-OAEP con un mensaje corto:

```bash
py -3 rsa_OAEP.py
```

Cifrar el documento de ejemplo:

```bash
py -3 rsa_AES_GCM.py
```

Cifrar otro archivo:

```bash
py -3 rsa_AES_GCM.py documentos_demo\acuerdo_miami.txt
```

## Respuestas de analisis

### 1. Por que no cifrar un documento completo directamente con RSA

RSA funciona bien para datos pequenos, pero no para archivos completos. Un documento grande tendria que dividirse en partes y el proceso seria lento. Por eso se usa un esquema hibrido: RSA protege una clave corta y AES cifra el contenido real del documento.

### 2. Que contiene un archivo `.pem`

Un archivo PEM guarda una clave en texto, usando Base64 y encabezados faciles de reconocer. Por ejemplo:

```text
-----BEGIN PUBLIC KEY-----
MIIB...
-----END PUBLIC KEY-----
```

En `public_key.pem` esta la clave publica RSA. En `private_key.pem` esta la clave privada, y en este laboratorio queda protegida con la passphrase `lab04uvg`.

### 3. Por que el mismo mensaje cifrado dos veces con OAEP produce resultados distintos

Porque OAEP agrega aleatoriedad antes de aplicar RSA. Aunque el mensaje sea igual, el relleno cambia en cada intento y por eso el ciphertext final tambien cambia.

### 4. PKCS#1 v1.5 vs OAEP

PKCS#1 v1.5 es un padding mas antiguo y ha tenido problemas cuando se usa mal. OAEP fue creado para mejorar eso y agregar mas seguridad. Para este laboratorio conviene usar OAEP porque es la opcion moderna y recomendada.

### 5. Presencia de RSA en protocolos reales

- En **TLS 1.3**, RSA ya no se usa para intercambio de clave. Su papel principal es firmar certificados.
- En **X.509**, RSA sigue apareciendo mucho en claves publicas y firmas de certificados.
- En **SSH**, RSA todavia existe, aunque hoy se prefieren variantes de firma mas modernas que `ssh-rsa`.

## Notas de implementacion

- El codigo se mantuvo sencillo para que sea facil de leer y explicar.
- `rsa_AES_GCM.py` guarda un paquete JSON con `clave_aes_cifrada`, `nonce`, `tag` y `ciphertext`.
- El archivo descifrado se guarda en la carpeta `salida/`.

## Ejecutar pruebas

Para correr las pruebas:

```bash
py -3 -m pytest
```

## Documento de referencia

El enunciado del ejercicio esta incluido en:

```text
Ejercicio RSA.pdf
```
