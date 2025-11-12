import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from pathlib import Path 

script_dir = Path(__file__).parent 

env_path = script_dir / '.env'

load_dotenv(dotenv_path=env_path) 


api_key = os.getenv("API_KEY")

if not api_key:

    print(f"Error: Api_key no encontrada.")
    print(f"Intento carga env desde: {env_path}")
    exit()

genai.configure(api_key=api_key)

try:
    with open("servicios.txt", "r", encoding="utf-8") as f:
        contexto_peluqueria = f.read()
except FileNotFoundError:
    print("Error: Servicios no encontrado.")
    exit()

prompt_base = f"""
Eres un asistente virtual para la Erik Bernabe's Barber.
Tu unica fuente de información es el siguiente texto:
---
{contexto_peluqueria}
---
Tu trabajo es responder las preguntas de los clientes basandote *unicamente* en esa informacion.
Si la pregunta no se puede responder con la informacion proporcionada, di amablemente
que no tienes esa informacion. No inventes precios ni horarios.
Se amable y conciso.
"""

model = genai.GenerativeModel('models/gemini-flash-latest')
chat = model.start_chat(history=[
 
    {'role': 'user', 'parts': [prompt_base]},
    {'role': 'model', 'parts': ["Hablas con el asistente de Erik Bernabe's Barber, en que puedo ayudarte?"]}
])

def enviar_pregunta():
 
    pregunta = entrada_usuario.get()
    
    if not pregunta:
        return
        
    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, f"Tu: {pregunta}\n\n")
    area_chat.see(tk.END) 
    entrada_usuario.delete(0, tk.END)
    boton_enviar.config(state=tk.DISABLED)

    try:
        response = chat.send_message(pregunta)
        
        respuesta_ia = response.text
        
        area_chat.insert(tk.END, f"Bernabe's Assistant: {respuesta_ia}\n\n")

    except Exception as e:
        area_chat.insert(tk.END, f"Bernabe's Assistant: Lo siento, ha ocurrido un error. Intenta de nuevo. ({e})\n\n")
    
    finally:
        
        boton_enviar.config(state=tk.NORMAL)
        area_chat.config(state=tk.DISABLED)
        area_chat.see(tk.END)

root = tk.Tk()
root.title("Asistente de Erik Bernabe's Barber")
root.geometry("500x600")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

titulo = tk.Label(main_frame, text="Erik Bernabe's Barber", font=("Arial", 16, "bold"))

titulo.pack(side=tk.TOP, pady=5)

frame_entrada = tk.Frame(main_frame)
frame_entrada.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0)) # fill=tk.X para que llene el ancho

area_chat = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 15))
area_chat.pack(fill=tk.BOTH, expand=True, pady=(10, 0)) # pady=(10,0) para que no pegue con el frame_entrada

entrada_usuario = tk.Entry(frame_entrada, font=("Arial", 12), width=35)
entrada_usuario.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))

boton_enviar = tk.Button(frame_entrada, text="Enviar", command=enviar_pregunta, font=("Arial", 10, "bold"))
boton_enviar.pack(side=tk.RIGHT, ipady=5, ipadx=10)


area_chat.config(state=tk.NORMAL)
area_chat.insert(tk.END, "24/7 a tu disposicion, en que podemos ayudarte?\n\n")
area_chat.config(state=tk.DISABLED)

root.mainloop()
