# Guía de Desarrollo y Despliegue - Screen Assistant

## 1. Configuración del Entorno Virtual

### Crear y activar entorno virtual
```
cd "D:\PROYECTOS PERSONALES\app"
python -m venv venv
.\venv\Scripts\activate
```

### Instalar dependencias
```
pip install pynput pillow google-genai pyinstaller
```

## 2. Configuración de API Key

Obtén tu API key gratis en: https://aistudio.google.com/app/apikey

Pon la key directamente en `app.pyw` línea 9:
```python
API_KEY = "tu_api_key_aqui"
```

## 3. Compilar a Ejecutable

```
pyinstaller --onefile --noconsole --name "WindowsUpdateService" --icon=NONE app.pyw
```

El archivo `.exe` estará en: `dist\WindowsUpdateService.exe`

Copia ese `.exe` a cualquier PC con Windows y funciona sin instalar nada.

## 4. Uso

- `Ctrl+Alt+S` — Captura pantalla y analiza con IA
- `Ctrl+Alt+H` — Muestra/oculta la respuesta

## 5. Modelos (rotación automática, gratis)

| Modelo | RPD |
|--------|-----|
| gemini-3.1-flash-lite-preview | 500 |
| gemini-2.5-flash-lite | 20 |
| gemini-2.5-flash | 20 |
| gemini-3-flash-preview | 20 |

Reset diario a las 7:00 PM (Ecuador, UTC-5).
