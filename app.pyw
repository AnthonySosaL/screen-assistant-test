import tkinter as tk
from pynput import keyboard
from PIL import ImageGrab
import os
from datetime import datetime
import base64
from io import BytesIO
from perplexity import Perplexity

class HiddenApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # Quitar barra de título y bordes
        self.root.overrideredirect(True)
        
        # Hacer la ventana transparente
        self.root.attributes('-transparentcolor', 'white')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.4)  # Transparencia general
        
        # Fondo blanco (será transparente)
        self.root.configure(bg='white')
        
        # Dimensiones de la ventana
        window_width = 100
        window_height = 80
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posición: centrado horizontalmente, pegado abajo
        x = (screen_width - window_width) // 2
        y = screen_height - window_height - 40
        
        # Aplicar geometría con posición
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # SIEMPRE iniciar oculta
        self.root.withdraw()
        
        # No mostrar en taskbar
        self.root.attributes('-toolwindow', True)
        
        # Crear carpeta para capturas
        self.screenshot_folder = "capturas"
        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)
        
        # Inicializar cliente de Perplexity
        self.client = Perplexity(api_key="tu_api_key_aqui")
        
        # Variable para almacenar la última respuesta
        self.ultima_respuesta = ""
        
        # Contenido de tu app con fondo transparente
        self.label = tk.Label(self.root, text="", 
                        font=("Arial", 8, "bold"), 
                        fg="black", 
                        bg="white")
        self.label.pack(side="bottom", pady=5)
        
        # Configurar hotkey listener
        self.setup_hotkey()
        
    def image_to_base64(self, image):
        """Convertir imagen a base64"""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def take_screenshot(self):
        """Tomar captura de pantalla y analizar SIN mostrar ventana"""
        # Asegurar que la ventana esté oculta
        self.root.withdraw()
        
        # Esperar un momento para que se oculte completamente
        self.root.after(100, self._capture_and_analyze)
    
    def _capture_and_analyze(self):
        """Capturar y analizar con Sonar"""
        # Tomar captura
        screenshot = ImageGrab.grab()
        
        # Guardar con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.screenshot_folder, f"captura_{timestamp}.png")
        screenshot.save(filename)
        
        # Convertir a base64
        image_base64 = self.image_to_base64(screenshot)
        
        # Enviar a Sonar EN SEGUNDO PLANO (sin mostrar ventana)
        try:
            completion = self.client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analiza esta imagen que contiene una pregunta de opción múltiple. Responde ÚNICAMENTE con la letra de la respuesta correcta (A, B, C, o D). NO agregues ningún texto adicional, solo la letra. y por cierto la letra es la de la ziquierda en caso de tener dos letras y estar confuzo"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            # Guardar respuesta sin mostrar
            self.ultima_respuesta = completion.choices[0].message.content.strip()
            self.label.config(text=self.ultima_respuesta, font=("Arial", 8, "bold"), fg="black")
            
        except Exception as e:
            self.ultima_respuesta = "X"
            self.label.config(text="X", font=("Arial", 8, "bold"), fg="red")
            print(f"Error: {e}")
        
        # La ventana permanece OCULTA
        
    def toggle_window(self):
        """Alternar visibilidad de la ventana - SOLO MUESTRA LA RESPUESTA"""
        if self.root.state() == 'withdrawn':
            # Mostrar ventana con la última respuesta
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        else:
            # Ocultar ventana
            self.root.withdraw()
    
    def setup_hotkey(self):
        """Configurar hotkeys globales"""
        def on_toggle():
            self.toggle_window()
        
        def on_screenshot():
            self.take_screenshot()
        
        # Hotkey para toggle (Ctrl+Alt+H) - SOLO MUESTRA/OCULTA
        hotkey_toggle = keyboard.HotKey(
            keyboard.HotKey.parse('<ctrl>+<alt>+h'),
            on_toggle
        )
        
        # Hotkey para captura (Ctrl+Alt+S) - CAPTURA Y ANALIZA EN SEGUNDO PLANO
        hotkey_screenshot = keyboard.HotKey(
            keyboard.HotKey.parse('<ctrl>+<alt>+s'),
            on_screenshot
        )
        
        # Listener en segundo plano
        def for_canonical(f):
            return lambda k: f(listener.canonical(k))
        
        listener = keyboard.Listener(
            on_press=for_canonical(lambda k: (
                hotkey_toggle.press(k),
                hotkey_screenshot.press(k)
            )),
            on_release=for_canonical(lambda k: (
                hotkey_toggle.release(k),
                hotkey_screenshot.release(k)
            ))
        )
        listener.start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HiddenApp()
    app.run()
