#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para consultar facturas vía API
Replica el funcionamiento del curl proporcionado

Uso: python consulta.py <invoice_id> <token> <nombre_archivo>
Ejemplo: python consulta.py 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec 76719.txt
"""

import sys
import requests
import os
from pathlib import Path


def main():
    # Verificar que se proporcionen exactamente 3 parámetros
    if len(sys.argv) != 4:
        print("Error: Se requieren exactamente 3 parámetros")
        print("Uso: consulta.exe <invoice_id> <token> <nombre_archivo>")
        print("Ejemplo: consulta.exe 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec 76719.txt")
        sys.exit(1)
    
    # Obtener parámetros de línea de comandos
    invoice_id = sys.argv[1]
    token = sys.argv[2] 
    nombre_archivo = sys.argv[3]
    
    # Construir la URL
    url = f"https://verifactu.corsoft.es/api/invoices/{invoice_id}"
    
    # Preparar headers
    headers = {
        'Authorization': f'Token {token}'
    }
    
    try:
        print(f"Consultando factura: {invoice_id}")
        print(f"URL: {url}")
        print(f"Guardando en: {nombre_archivo}")
        
        # Realizar la petición HTTP
        response = requests.get(url, headers=headers)
        
        # Verificar si la petición fue exitosa
        if response.status_code == 200:
            # Crear directorio si no existe
            output_path = Path(nombre_archivo)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar el contenido en el archivo
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"✓ Consulta exitosa. Datos guardados en: {nombre_archivo}")
            print(f"✓ Tamaño del archivo: {len(response.text)} caracteres")
            
        else:
            print(f"✗ Error en la petición. Código de estado: {response.status_code}")
            print(f"✗ Mensaje: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()