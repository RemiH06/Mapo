import requests
import json
import pandas as pd
import customtkinter as ctk
from tkinter import ttk
from datetime import datetime

class INEGIDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Dashboard INEGI - Indicador Ejemplo")
        self.geometry("800x600")
        
        # Obtener token
        self.token = self.get_token()
        
        # URL de la API
        self.url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000041/es/0700/false/BISE/2.0/{self.token}?type=json"
        
        # Crear widgets
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_data()
    
    def get_token(self):
        try:
            with open('.secrets') as f:
                secrets = json.load(f)
            return secrets['token']
        except Exception as e:
            print(f"Error al leer el token: {e}")
            return ""
    
    def create_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabla para mostrar datos
        self.tree = ttk.Treeview(self.main_frame)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Botón para actualizar
        self.refresh_btn = ctk.CTkButton(
            self.main_frame, 
            text="Actualizar Datos", 
            command=self.load_data
        )
        self.refresh_btn.pack(pady=5)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(self.main_frame, text="", text_color="gray")
        self.status_label.pack(pady=5)
    
    def load_data(self):
        self.status_label.configure(text="Cargando datos...", text_color="gray")
        self.update()
        
        try:
            response = requests.get(self.url)
            
            if response.status_code != 200:
                self.status_label.configure(
                    text=f"Error al obtener datos del INEGI: {response.status_code}", 
                    text_color="red"
                )
                return
            
            data = response.json()
            
            # Extraer las observaciones
            series = data.get('Series', [])
            if not series:
                self.status_label.configure(text="No se encontraron observaciones", text_color="orange")
                return
            
            observations = series[0].get('OBSERVATIONS', [])
            
            # Crear DataFrame
            df = pd.DataFrame(observations)
            
            # Mostrar datos en la tabla
            self.display_data(df)
            
            self.status_label.configure(
                text=f"Datos actualizados: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                text_color="green"
            )
            
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")
    
    def display_data(self, df):
        # Limpiar tabla existente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Configurar columnas
        columns = list(df.columns)
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # Agregar encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        # Agregar datos
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Puedes cambiar a "Dark" o "Light"
    ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"
    
    app = INEGIDashboard()
    app.mainloop()