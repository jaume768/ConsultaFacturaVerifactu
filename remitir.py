#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remitir facturas vía API
Replica el funcionamiento del curl POST proporcionado

Uso: python remitir.py <token> <json> <ruta_archivo>
Ejemplo: python remitir.py "fsdfsdfsdf" '{"invoice_type":"F1",...}' "C:\VELNEO\TRASPASOS\bugaderia\5.txt"
"""

import sys
import requests
import json
import os
from pathlib import Path


def mostrar_ayuda():
    """Muestra el mensaje de ayuda del programa"""
    print("\n📤 Remisión de Facturas - API Verifactu")
    print("=" * 50)
    print("\n🎯 DESCRIPCIÓN:")
    print("   Este programa envía facturas a la API de Verifactu mediante POST")
    print("   y guarda la respuesta JSON en un archivo local.")
    print("\n📋 USO:")
    print("   remitir.exe <token> <json_data> <ruta_archivo>")
    print("\n📝 PARÁMETROS:")
    print("   token       : Token de autorización de la API")
    print("   json_data   : Datos JSON de la factura (string)")
    print("   ruta_archivo: Ruta completa donde guardar la respuesta")
    print("\n💡 EJEMPLO:")
    print('   remitir.exe "fsdfsdfsdf" \\')
    print('               \'{"invoice_type":"F1","customer_name":"A.C.E.S., S.L.",...}\' \\')
    print('               "C:\\VELNEO\\TRASPASOS\\bugaderia\\5.txt"')
    print("\n🌐 EQUIVALE AL COMANDO CURL:")
    print("   curl --location 'https://verifactu.corsoft.com.es/api/invoices/' \\")
    print("        --header 'Content-Type: application/json' \\")
    print("        --header 'Authorization: Token <token>' \\")
    print("        --data '<json_data>' > <ruta_archivo>")
    print("\n🔒 NOTA DE SEGURIDAD:")
    print("   - Nunca hardcodees tokens en el código")
    print("   - Mantén los tokens seguros y rótalos regularmente")
    print("\n📊 FORMATO JSON ESPERADO:")
    print("   El JSON debe contener los campos requeridos por la API:")
    print("   - invoice_type, customer_name, customer_country, etc.")
    print("\n" + "=" * 50)
    print("\n⏸️  Presiona ENTER para continuar...")
    input()


def arreglar_json_powershell(json_string, debug=False):
    """
    Arregla JSON dañado por PowerShell que elimina comillas dobles
    
    Args:
        json_string (str): JSON potencialmente dañado por PowerShell
        debug (bool): Si mostrar información de debug
    
    Returns:
        str: JSON corregido con comillas apropiadas
    """
    import re
    
    # Si ya es JSON válido, devolverlo tal como está
    try:
        json.loads(json_string)
        return json_string
    except json.JSONDecodeError:
        pass
    
    if debug:
        print(f"🔧 Arreglando JSON dañado por PowerShell...")
        print(f"📝 JSON original: {json_string}")
    
    # Paso 0: Remover comillas simples externas si están presentes
    # PowerShell puede pasar las comillas simples como parte del string
    if json_string.startswith("'") and json_string.endswith("'"):
        json_string = json_string[1:-1]  # Remover primera y última comilla simple
        if debug:
            print(f"📝 Después de remover comillas simples externas: {json_string[:100]}...")
    
    # Paso 1: Agregar comillas alrededor de nombres de propiedades
    # Patrón: {word: o ,word:
    json_string = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)', r'\1"\2"\3', json_string)
    if debug:
        print(f"📝 Después de agregar comillas a propiedades: {json_string[:100]}...")
    
    # Paso 2: Arreglar valores vacíos (:"," o :})
    # Patrón: : seguido de coma o llave de cierre
    json_string = re.sub(r'(:\s*)(,|[}\]])', r'\1""\2', json_string)
    if debug:
        print(f"📝 Después de arreglar valores vacíos: {json_string[:100]}...")
    
    # Paso 3: Agregar comillas alrededor de valores de string
    def quote_string_values(match):
        colon_space = match.group(1)  # : y espacios opcionales
        value = match.group(2)        # el valor
        comma_or_end = match.group(3) # , } ] o final
        
        value_clean = value.strip()
        
        # Si está vacío, ya se manejó en el paso 2
        if not value_clean:
            return match.group(0)
        
        # Si es número (entero o decimal), no cambiar
        if re.match(r'^-?\d+(\.\d+)?$', value_clean):
            return match.group(0)
        
        # Si es booleano o null, no cambiar
        if value_clean in ['true', 'false', 'null']:
            return match.group(0)
        
        # Si ya tiene comillas, no cambiar
        if value_clean.startswith('"') and value_clean.endswith('"'):
            return match.group(0)
        
        # Agregar comillas alrededor del valor
        return f'{colon_space}"{value_clean}"{comma_or_end}'
    
    # Patrón para capturar valores: : seguido de cualquier contenido hasta , } ]
    json_string = re.sub(r'(:\s*)([^,}\]]*?)(\s*[,}\]])', quote_string_values, json_string)
    if debug:
        print(f"📝 JSON final arreglado: {json_string[:100]}...")
    
    return json_string


def validar_json(json_string, debug=False):
    """
    Valida que el string proporcionado sea un JSON válido
    Intenta arreglar automáticamente JSON dañado por PowerShell
    
    Args:
        json_string (str): String que debe ser JSON válido
        debug (bool): Si mostrar información de debug
    
    Returns:
        dict: JSON parseado si es válido
        None: Si no es válido
    """
    try:
        # Intentar parsear tal como está
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        if debug:
            print(f"⚠️  JSON inválido detectado. Detalle: {e}")
            print(f"🔧 Intentando arreglar JSON dañado por PowerShell...")
        
        try:
            # Intentar arreglar el JSON
            json_arreglado = arreglar_json_powershell(json_string, debug)
            resultado = json.loads(json_arreglado)
            if debug:
                print(f"🎉 ¡JSON arreglado exitosamente!")
            return resultado
            
        except json.JSONDecodeError as e2:
            # Solo mostrar error si debug está activado
            if debug:
                print(f"❌ Error: No se pudo arreglar el JSON automáticamente")
                print(f"   Error original: {e}")
                print(f"   Error después del arreglo: {e2}")
            return None


def main():
    # Verificar que se proporcionen exactamente 3 parámetros
    if len(sys.argv) != 4:
        if len(sys.argv) == 1:
            # Si no se proporcionan parámetros, mostrar ayuda completa
            mostrar_ayuda()
        else:
            # Si se proporcionan parámetros incorrectos, mostrar error y ayuda breve
            print(f"\n❌ Error: Se requieren exactamente 3 parámetros (se proporcionaron {len(sys.argv)-1})")
            print("\n📋 USO CORRECTO:")
            print("   remitir.exe <token> <json_data> <ruta_archivo>")
            print("\n💡 EJEMPLO:")
            print('   remitir.exe "mi_token_api" \\')
            print('               \'{"invoice_type":"F1","customer_name":"Cliente"}\' \\')
            print('               "C:\\ruta\\archivo.txt"')
            print("\n💬 Para más información, ejecuta el programa sin parámetros.")
            print("\n⏸️  Presiona ENTER para continuar...")
            input()
        sys.exit(1)
    
    # Obtener parámetros de línea de comandos
    token = sys.argv[1]
    json_data_string = sys.argv[2]
    ruta_archivo = sys.argv[3]
    
    # Validar que el JSON sea válido
    json_data = validar_json(json_data_string)
    if json_data is None:
        # Mostrar detalles del error solo cuando falla
        print(f"\n🔍 DEBUG - JSON recibido (primeros 100 chars): {json_data_string[:100]}...")
        print(f"🔍 DEBUG - Longitud: {len(json_data_string)} caracteres")
        
        # Intentar de nuevo con debug activado para mostrar detalles
        print("\n🔍 Intentando de nuevo con información detallada...")
        json_data = validar_json(json_data_string, debug=True)
        
        if json_data is None:
            print("\n💬 Tip: Asegúrate de que el JSON esté entre comillas simples")
            print("💬      y que todos los campos tengan el formato correcto")
            print("\n⏸️  Presiona ENTER para continuar...")
            input()
            sys.exit(1)
    
    # URL de la API
    url = "https://verifactu.corsoft.com.es/api/invoices/"
    
    # Preparar headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }
    
    try:
        print(f"🚀 Enviando factura a la API...")
        print(f"📍 URL: {url}")
        print(f"🔑 Token: {token[:10]}...")  # Mostrar solo los primeros 10 caracteres por seguridad
        print(f"📄 Guardando en: {ruta_archivo}")
        
        # Realizar la petición HTTP POST
        response = requests.post(url, headers=headers, json=json_data)
        
        # Verificar si la petición fue exitosa
        if response.status_code in [200, 201]:
            # Crear directorio si no existe
            output_path = Path(ruta_archivo)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar el contenido en el archivo
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Ejecutión exitosa: no mostrar nada y salir silenciosamente
            # Solo en caso de que quieras ver confirmación, descomenta las siguientes líneas:
            # print(f"✓ Factura enviada exitosamente!")
            # print(f"✓ Código de respuesta: {response.status_code}")
            # print(f"✓ Respuesta guardada en: {ruta_archivo}")
            
        else:
            print(f"✗ Error en la petición. Código de estado: {response.status_code}")
            print(f"✗ Mensaje: {response.text}")
            
            # Intentar guardar la respuesta de error también
            try:
                output_path = Path(ruta_archivo)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✓ Respuesta de error guardada en: {ruta_archivo}")
            except Exception as save_error:
                print(f"✗ Error al guardar respuesta de error: {save_error}")
            
            print("\n⏸️  Presiona ENTER para continuar...")
            input()
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        print("\n⏸️  Presiona ENTER para continuar...")
        input()
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        print("\n⏸️  Presiona ENTER para continuar...")
        input()
        sys.exit(1)


if __name__ == "__main__":
    main()
