text
# Guía de Desarrollo y Despliegue - Screen Assistant

## 1. Configuración del Entorno Virtual

### Crear y activar entorno virtual
cd "D:\PROYECTOS PERSONALES\app"
python -m venv venv
.\venv\Scripts\activate

text

### Instalar dependencias
pip install pynput pillow perplexityai pyinstaller

text

## 2. Configuración de API Key

Antes de compilar, asegúrate de configurar tu API key de Perplexity como variable de entorno:

**Opción 1: Variable de entorno (Recomendado)**
Windows PowerShell
$env:PERPLEXITY_API_KEY="tu_api_key_aqui"

Windows CMD
set PERPLEXITY_API_KEY=tu_api_key_aqui

text

**Opción 2: Archivo .env**
Crea un archivo `.env` en la raíz del proyecto:
PERPLEXITY_API_KEY=tu_api_key_aqui

text

Y modifica el código para leer desde `.env`:
import os
from dotenv import load_dotenv

load_dotenv()
self.client = Perplexity(api_key=os.getenv('PERPLEXITY_API_KEY'))

text

## 3. Compilar a Ejecutable

pyinstaller --onefile --noconsole --name "WindowsUpdateService" --icon=NONE app.pyw

text

El archivo `.exe` estará en: `dist\WindowsUpdateService.exe`
