import tkinter as tk
from pynput import keyboard
from PIL import ImageGrab
import os
from datetime import datetime
from google import genai

API_KEY = "AIzaSyC_gHChKjuFh66MSniuBvIz8LVmJfxPSyY"

class HiddenApp:
    def __init__(self):
        self.root = tk.Tk()

        # Quitar barra de título y bordes
        self.root.overrideredirect(True)

        # Hacer la ventana transparente
        self.root.attributes('-transparentcolor', 'white')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.4)

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

        # Inicializar cliente Gemini (nueva librería google-genai)
        self.client = genai.Client(api_key=API_KEY)
        # Modelos en orden de preferencia - rota automáticamente si uno agota cuota
        self.models = [
            "gemini-3.1-flash-lite-preview",  # 500 RPD - entra cuando Google lo reactive
            "gemini-2.5-flash-lite",           # 20 RPD
            "gemini-2.5-flash",                # 20 RPD
            "gemini-3-flash-preview",          # 20 RPD
        ]

        # Variable para almacenar la última respuesta
        self.ultima_respuesta = ""

        # Label de respuesta con fondo transparente
        self.label = tk.Label(self.root, text="",
                        font=("Arial", 8, "bold"),
                        fg="black",
                        bg="white")
        self.label.pack(side="bottom", pady=5)

        # Configurar hotkey listener
        self.setup_hotkey()

    def take_screenshot(self):
        """Tomar captura de pantalla y analizar SIN mostrar ventana"""
        self.root.withdraw()
        self.root.after(100, self._capture_and_analyze)

    def _capture_and_analyze(self):
        """Capturar y analizar con Gemini"""
        screenshot = ImageGrab.grab()

        # Guardar con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.screenshot_folder, f"captura_{timestamp}.png")
        screenshot.save(filename)

        prompt = [
            screenshot,
            "Analiza esta imagen que contiene una pregunta de opción múltiple. "
            "Responde ÚNICAMENTE con la letra de la respuesta correcta (A, B, C, o D). "
            "NO agregues ningún texto adicional, solo la letra. "
            "La letra es la de la izquierda en caso de tener dos letras."
        ]

        last_error = None
        for model in self.models:
            try:
                response = self.client.models.generate_content(model=model, contents=prompt)
                self.ultima_respuesta = response.text.strip()
                self.label.config(text=self.ultima_respuesta, font=("Arial", 8, "bold"), fg="black")
                print(f"Respondió: {model}")
                return
            except Exception as e:
                last_error = e
                if "429" in str(e) or "503" in str(e):
                    print(f"{model} no disponible, probando siguiente...")
                    continue
                else:
                    break

        # Todos los modelos fallaron
        err = str(last_error)
        if "429" in err:
            self.ultima_respuesta = "W"
            self.label.config(text="W", font=("Arial", 8, "bold"), fg="orange")
        else:
            self.ultima_respuesta = "X"
            self.label.config(text="X", font=("Arial", 8, "bold"), fg="red")
        print(f"Error final: {last_error}")

    def toggle_window(self):
        """Alternar visibilidad de la ventana"""
        if self.root.state() == 'withdrawn':
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        else:
            self.root.withdraw()

    def setup_hotkey(self):
        """Configurar hotkeys globales"""
        hotkey_toggle = keyboard.HotKey(
            keyboard.HotKey.parse('<ctrl>+<alt>+h'),
            self.toggle_window
        )

        hotkey_screenshot = keyboard.HotKey(
            keyboard.HotKey.parse('<ctrl>+<alt>+s'),
            self.take_screenshot
        )

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
