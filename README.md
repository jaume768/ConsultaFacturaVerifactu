# 📄 API Verifactu - Scripts de Consulta y Remisión

Este proyecto contiene scripts en Python que replican la funcionalidad de comandos `curl` para interactuar con la API de Verifactu:
- **consulta.py**: Consultar facturas existentes (GET)
- **remitir.py**: Enviar/remitir nuevas facturas (POST)

## 🎯 Funcionalidades

### 📥 consulta.py - Consultar Facturas
Realiza una petición GET a la API de Verifactu para consultar facturas existentes con autenticación por token y guarda la respuesta JSON en un archivo especificado.

**Equivale a este comando curl:**
```bash
curl --location 'https://verifactu.corsoft.com.es/api/invoices/40b8a275-83e9-4aec-9133-b7b0462a1877' \
     --header 'Authorization: Token 4ed052656e3fdb3baefb5126f0044dd67c350bec' \
     > C:\TWS\76719.txt
```

### 📤 remitir.py - Enviar Facturas
Realiza una petición POST a la API de Verifactu para enviar nuevas facturas con datos JSON y guarda la respuesta en un archivo especificado.

**Equivale a este comando curl:**
```bash
curl --location 'https://verifactu.corsoft.com.es/api/invoices/' \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Token fsdfsdfsdf' \
     --data '{"invoice_type":"F1","customer_name":"A.C.E.S., S.L.","customer_country":"ES",...}' \
     > C:\VELNEO\TRASPASOS\bugaderia\5.txt
```

## 📋 Requisitos

- Python 3.7 o superior
- Biblioteca `requests` (incluida en `requirements.txt`)

## 🚀 Uso de los Scripts

### 📥 consulta.py - Para Consultar Facturas

### Como script Python:

**En Windows:**
```cmd
python consulta.py <invoice_id> <token> <nombre_archivo>
```

**En Linux/MacOS:**
```bash
python3 consulta.py <invoice_id> <token> <nombre_archivo>
```

### Como ejecutable:

**En Windows:**
```cmd
consulta.exe <invoice_id> <token> <nombre_archivo>
```

**En Linux/MacOS:**
```bash
./consulta <invoice_id> <token> <nombre_archivo>
```

### Ejemplo:

**En Windows:**
```cmd
python consulta.py 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec 76719.txt
```

**En Linux/MacOS:**
```bash
python3 consulta.py 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec 76719.txt
```

### 📤 remitir.py - Para Enviar Facturas

### Como script Python:

**En Windows:**
```cmd
python remitir.py <token> <json_data> <ruta_archivo>
```

**En Linux/MacOS:**
```bash
python3 remitir.py <token> <json_data> <ruta_archivo>
```

### Como ejecutable:

**En Windows:**
```cmd
remitir.exe <token> <json_data> <ruta_archivo>
```

**En Linux/MacOS:**
```bash
./remitir <token> <json_data> <ruta_archivo>
```

### Ejemplo:

**En Windows:**
```cmd
remitir.exe "fsdfsdfsdf" "{\"invoice_type\":\"F1\",\"customer_name\":\"A.C.E.S., S.L.\",\"customer_country\":\"ES\",\"customer_nif\":\"B07055858\",\"serie\":\"25\",\"number\":\"4\",\"base_1\":4.22,\"tax_percentage_1\":21,\"tax_cuota_1\":0.88,\"operation_clasification_1\":\"S1\",\"regime_key_1\":\"\",\"total\":5.1,\"date\":\"20-06-2025\",\"time\":\"9:32\",\"claveapi\":\"-128\"}" "C:\\VELNEO\\TRASPASOS\\bugaderia\\5.txt"
```

**En Linux/MacOS:**
```bash
./remitir "fsdfsdfsdf" '{"invoice_type":"F1","customer_name":"A.C.E.S., S.L.","customer_country":"ES","customer_nif":"B07055858","serie":"25","number":"4","base_1":4.22,"tax_percentage_1":21,"tax_cuota_1":0.88,"operation_clasification_1":"S1","regime_key_1":"","total":5.1,"date":"20-06-2025","time":"9:32","claveapi":"-128"}' "C:/VELNEO/TRASPASOS/bugaderia/5.txt"
```

## 📂 Estructura del Proyecto

```
ConsultaFacturaVerifactu/
│
├── consulta.py          # Script para consultar facturas (GET)
├── remitir.py           # Script para enviar facturas (POST)
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Este archivo
├── venv/               # Entorno virtual (generado)
├── build/              # Archivos temporales de PyInstaller
├── dist/               # Ejecutables generados
│   ├── consulta.exe    # Ejecutable para consultas
│   └── remitir.exe     # Ejecutable para remisiones
├── consulta.spec       # Configuración de PyInstaller para consulta
└── remitir.spec        # Configuración de PyInstaller para remitir
```

## 🔧 Instalación y Configuración

### 1. Clonar o descargar el proyecto

**En Windows:**
```cmd
cd C:\ruta\al\proyecto\ExeConsultaEstado
```

**En Linux/MacOS:**
```bash
cd /ruta/al/proyecto/ExeConsultaEstado
```

### 2. Crear entorno virtual

**En Windows:**
```cmd
python -m venv venv
```

**En Linux/MacOS:**
```bash
python3 -m venv venv
```

### 3. Activar entorno virtual

**En Linux/MacOS:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

**En Windows:**
```cmd
pip install -r requirements.txt
```

**En Linux/MacOS:**
```bash
pip install -r requirements.txt
```

### 5. Probar el script

**En Windows:**
```cmd
python consulta.py <tu_invoice_id> <tu_token> <archivo_destino.txt>
```

**En Linux/MacOS:**
```bash
python3 consulta.py <tu_invoice_id> <tu_token> <archivo_destino.txt>
```

## 🏗️ Generar Ejecutable

### 1. Instalar PyInstaller (dentro del venv activado)

**En Windows:**
```cmd
pip install pyinstaller
```

**En Linux/MacOS:**
```bash
pip install pyinstaller
```

### 2. Generar el ejecutable

**En Windows:**
```cmd
pyinstaller --onefile --name consulta consulta.py
```

**En Linux/MacOS:**
```bash
pyinstaller --onefile --name consulta consulta.py
```

### 3. Ubicación del ejecutable
El ejecutable se generará en:
- **Linux/MacOS:** `dist/consulta`
- **Windows:** `dist/consulta.exe`

### 4. Usar el ejecutable

**En Windows:**
```cmd
dist\consulta.exe 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec 76719.txt
```

**En Linux/MacOS:**
```bash
./dist/consulta 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec 76719.txt
```

## 🔧 Proceso Completo de Desarrollo

### Script para automatizar todo el proceso:

**Para Linux/MacOS (setup_project.sh):**
```bash
#!/bin/bash
# setup_project.sh

echo "🚀 Configurando proyecto Consulta de Facturas..."

# 1. Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# 2. Activar entorno virtual
echo "⚡ Activando entorno virtual..."
source venv/bin/activate

# 3. Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# 4. Instalar PyInstaller
echo "🔨 Instalando PyInstaller..."
pip install pyinstaller

# 5. Generar ejecutable
echo "🏗️ Generando ejecutable..."
pyinstaller --onefile --name consulta consulta.py

echo "✅ ¡Proyecto configurado exitosamente!"
echo "📁 Ejecutable disponible en: dist/consulta"
echo ""
echo "🎯 Uso del ejecutable:"
echo "./dist/consulta <invoice_id> <token> <archivo_destino>"
```

**Para Windows (setup_project.bat):**
```batch
@echo off
REM setup_project.bat

echo 🚀 Configurando proyecto Consulta de Facturas...

REM 1. Crear entorno virtual
echo 📦 Creando entorno virtual...
python -m venv venv

REM 2. Activar entorno virtual
echo ⚡ Activando entorno virtual...
call venv\Scripts\activate

REM 3. Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt

REM 4. Instalar PyInstaller
echo 🔨 Instalando PyInstaller...
pip install pyinstaller

REM 5. Generar ejecutable
echo 🏗️ Generando ejecutable...
pyinstaller --onefile --name consulta consulta.py

echo ✅ ¡Proyecto configurado exitosamente!
echo 📁 Ejecutable disponible en: dist\consulta.exe
echo.
echo 🎯 Uso del ejecutable:
echo dist\consulta.exe ^<invoice_id^> ^<token^> ^<archivo_destino^>
pause
```

## 📝 Parámetros

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `invoice_id` | ID único de la factura | `40b8a275-83e9-4aec-9133-b7b0462a1877` |
| `token` | Token de autorización de la API | `4ed052656e3fdb3baefb5126f0044dd67c350bec` |
| `nombre_archivo` | Nombre del archivo donde guardar la respuesta | `76719.txt` |

## ✅ Validaciones

El script incluye las siguientes validaciones:

- ✅ Verificación de número correcto de parámetros
- ✅ Manejo de errores de conexión HTTP
- ✅ Verificación de códigos de estado de respuesta
- ✅ Creación automática de directorios si no existen
- ✅ Mensajes informativos durante la ejecución

## 🐛 Solución de Problemas

### Error: "requests module not found"

**En Windows:**
```cmd
REM Solución: Activar el entorno virtual e instalar dependencias
venv\Scripts\activate
pip install -r requirements.txt
```

**En Linux/MacOS:**
```bash
# Solución: Activar el entorno virtual e instalar dependencias
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "pyinstaller command not found"

**En Windows:**
```cmd
REM Solución: Instalar PyInstaller en el entorno virtual
venv\Scripts\activate
pip install pyinstaller
```

**En Linux/MacOS:**
```bash
# Solución: Instalar PyInstaller en el entorno virtual
source venv/bin/activate
pip install pyinstaller
```

### Error de permisos en Linux/MacOS
```bash
# Solución: Dar permisos de ejecución al ejecutable
chmod +x dist/consulta
```

### Error de ejecución en Windows
```cmd
REM Si el ejecutable no se ejecuta, verificar que esté en la ruta correcta
dir dist\consulta.exe
REM O ejecutar desde la carpeta dist
cd dist
consulta.exe <parametros>
```

## 📊 Ejemplo de Salida

**En Windows:**
```cmd
C:\proyecto> dist\consulta.exe 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec factura_76719.txt

Consultando factura: 40b8a275-83e9-4aec-9133-b7b0462a1877
URL: https://verifactu.corsoft.com.es/api/invoices/40b8a275-83e9-4aec-9133-b7b0462a1877
Guardando en: factura_76719.txt
✓ Consulta exitosa. Datos guardados en: factura_76719.txt
✓ Tamaño del archivo: 1247 caracteres
```

**En Linux/MacOS:**
```bash
$ ./dist/consulta 40b8a275-83e9-4aec-9133-b7b0462a1877 4ed052656e3fdb3baefb5126f0044dd67c350bec factura_76719.txt

Consultando factura: 40b8a275-83e9-4aec-9133-b7b0462a1877
URL: https://verifactu.corsoft.com.es/api/invoices/40b8a275-83e9-4aec-9133-b7b0462a1877
Guardando en: factura_76719.txt
✓ Consulta exitosa. Datos guardados en: factura_76719.txt
✓ Tamaño del archivo: 1247 caracteres
```

## 🔒 Consideraciones de Seguridad

- 🔑 **Nunca hardcodees tokens** en el código fuente
- 🔐 Mantén los tokens como parámetros de línea de comandos
- 📝 No registres tokens en logs
- 🔄 Rota tokens regularmente según las políticas de seguridad

## 📞 Soporte

Si tienes problemas:

1. Verifica que el entorno virtual esté activado
2. Confirma que todas las dependencias estén instaladas
3. Verifica la conectividad con la API
4. Revisa que el token sea válido

---

**Desarrollado para consultas eficientes de la API de Verifactu** 🚀
