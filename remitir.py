#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
remitir.py – Envía facturas a la API de Verifactu y guarda la respuesta.

USO
----
remitir.exe <token> <json_o_ruta_json> <ruta_archivo>

• <token>            → Token de autenticación API
• <json_o_ruta_json> → Cadena JSON (puede ir sin comillas dobles) o ruta a un .json
• <ruta_archivo>     → Dónde guardar la respuesta de la API

Ejemplo PowerShell
------------------
$j = '{"invoice_type":"F1", ... }'
.\remitir.exe 4ed052656e3fd... $j 'C:\salida.txt'

Ejemplo CMD clásico
-------------------
.\remitir.exe 4ed052656e3fd... "{""invoice_type"":""F1"", ...}" C:\salida.txt
"""

import sys
import json
import re
from pathlib import Path
import requests

# ───────────────────── DEPENDENCIA OPCIONAL ──────────────────────
# pip install json5   (si no lo instalas, el script sigue funcionando)
try:
    import json5  # type: ignore
except ModuleNotFoundError:
    json5 = None

# Expresión para separar pares clave:valor sin cortar comas internas
PAIR_SPLITTER = re.compile(r',\s*(?=[A-Za-z_][A-Za-z0-9_]*\s*:)')

# Expresiones numéricas refinadas
INT_RE   = re.compile(r'^-?(0|[1-9][0-9]*)$')          # entero (permite 0 solo)
INT_Z0   = re.compile(r'^-?0[0-9]+$')                  # entero con cero inicial → mantener string
FLOAT_RE = re.compile(r'^-?(?:0|[1-9][0-9]*)\.[0-9]+$')  # decimal


# ╭───────────── UTILIDADES DE CONSOLA ─────────────╮
def mostrar_ayuda() -> None:
    print(__doc__)
    input("\n⏸️  Pulsa ENTER para salir...")


# ╭───────────────── NORMALIZAR JSON ───────────────╮
def arreglar_json_relajado(cadena: str, debug: bool = False) -> str:
    """
    Convierte {invoice_type:F1,...} en JSON válido.
    Mantiene como *texto* los literales con ceros iniciales (p.ej. 01).
    """
    if debug:
        print("🔧 Normalizando JSON “relajado”…")

    # Quitar comillas simples externas
    if cadena.startswith("'") and cadena.endswith("'"):
        cadena = cadena[1:-1]

    cuerpo = cadena.strip()
    if cuerpo.startswith('{') and cuerpo.endswith('}'):
        cuerpo = cuerpo[1:-1]

    pares = PAIR_SPLITTER.split(cuerpo)
    datos: dict[str, object] = {}

    for par in pares:
        if ':' not in par:
            continue
        k, v = par.split(':', 1)
        k = k.strip().strip('"\'')
        v = v.strip()

        # Si viene con comillas → string literal tal cual
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            datos[k] = v[1:-1]
            continue

        # Decimal
        if FLOAT_RE.match(v):
            datos[k] = float(v)
            continue

        # Entero sin cero inicial
        if INT_RE.match(v) and not INT_Z0.match(v):
            datos[k] = int(v)
            continue

        # Booleano / null
        if v.lower() in {"true", "false"}:
            datos[k] = v.lower() == "true"
            continue
        if v.lower() == "null":
            datos[k] = None
            continue

        # Todo lo demás → string
        datos[k] = v

    json_str = json.dumps(datos, ensure_ascii=False)
    if debug:
        print(f"📝 JSON normalizado: {json_str[:120]}…")
    return json_str


def validar_json(cadena: str, debug: bool = False):
    """
    Devuelve un dict a partir de la cadena dada.
    1) JSON estricto        2) JSON5 (si disponible)        3) heurística
    """
    # 1. JSON estricto
    try:
        return json.loads(cadena)
    except json.JSONDecodeError:
        if debug:
            print("❌ No es JSON estricto válido.")

    # 2. JSON5 (opcional)
    if json5 is not None:
        try:
            return json5.loads(cadena)
        except Exception:
            if debug:
                print("❌ Tampoco es JSON5 válido.")

    # 3. Heurística final
    if debug:
        print("🔄 Aplicando heurística de normalización…")
    cadena_normalizada = arreglar_json_relajado(cadena, debug)
    return json.loads(cadena_normalizada)


# ╭────────────────────────── MAIN ──────────────────────────╮
def main() -> None:
    if len(sys.argv) != 4:
        mostrar_ayuda()
        sys.exit(1)

    token, json_input, ruta_archivo = sys.argv[1], sys.argv[2], sys.argv[3]

    # Si es ruta a archivo JSON -> cargar
    path_json = Path(json_input)
    if path_json.is_file():
        json_raw = path_json.read_text(encoding="utf-8")
    else:
        json_raw = json_input

    # Validar / normalizar
    json_data = validar_json(json_raw, debug=True)
    if json_data is None:
        print("✗ No se pudo interpretar el JSON de entrada.")
        sys.exit(1)

    url = "https://verifactu.corsoft.es/api/invoices/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {token}",
    }

    try:
        print("🚀 Enviando factura…")
        resp = requests.post(url, headers=headers, json=json_data)

        # Guardar siempre la respuesta
        out = Path(ruta_archivo)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(resp.text, encoding="utf-8")

        if resp.status_code in {200, 201}:
            print("✓ Factura enviada correctamente.")
        else:
            print(f"✗ Error {resp.status_code}:\n{resp.text}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
