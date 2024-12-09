import tkinter as tk
import random
import tkinter.messagebox

# Lista de palabras por temas
temas_palabras = {
    "Animales": ["TIGRE", "LEON", "ELEFANTE", "DELFIN", "CABALLO", "CEBRA"],
    "Frutas": ["MANZANA", "BANANA", "FRUTILLA", "MANGO", "KIWI", "MANDARINA"],
    "Paises": ["ARGENTINA", "MEXICO", "CANADA", "JAPON", "BRAZIL"],
    "Dioses": ["LUCIFER", "AMENADIEL", "AZRAEL", "MICHAEL", "GABRIEL"]
}

tema_actual = "Frutas"  # Tema por defecto
palabra_secreta = random.choice(temas_palabras[tema_actual]).upper()
letras_adivinadas = ["_"] * len(palabra_secreta)
letras_incorrectas = []
intentos = 6
tiempo_restante = 300  # 5 minutos en segundos
palabras_ganadas = []  # Lista de palabras ganadas
puntos = 0  # Puntos acumulados

# Función para dibujar el muñeco


def dibujar_muneco(canvas, errores):
    canvas.delete("all")
    if errores >= 1:
        canvas.create_oval(60, 20, 140, 100, outline="black",
                           fill="yellow", width=3)  # Cabeza
    if errores >= 2:
        canvas.create_line(100, 100, 100, 200, fill="blue", width=3)  # Cuerpo
    if errores >= 3:
        canvas.create_line(100, 120, 60, 160, fill="red",
                           width=3)  # Brazo izquierdo
    if errores >= 4:
        canvas.create_line(100, 120, 140, 160, fill="red",
                           width=3)  # Brazo derecho
    if errores >= 5:
        canvas.create_line(100, 200, 70, 250, fill="green",
                           width=3)  # Pierna izquierda
    if errores >= 6:
        canvas.create_line(100, 200, 130, 250, fill="green",
                           width=3)  # Pierna derecha

# Función para actualizar la interfaz


def actualizar_interfaz():
    # Declarar la variable global
    global tiempo_restante, tema_actual, palabra_secreta, letras_adivinadas, letras_incorrectas

    tema_label.config(text=f"Tema elegido: {tema_actual}")
    palabra_label.config(text=" ".join(letras_adivinadas))
    errores_label.config(text="Letras incorrectas: " +
                         ", ".join(letras_incorrectas))
    dibujar_muneco(canvas, len(letras_incorrectas))

    # Si adivinó toda la palabra
    if "_" not in letras_adivinadas:
        resultado_label.config(
            text=f"¡Ganaste! La palabra es: {palabra_secreta}")
        entry_letra.config(state='disabled')
        boton_adivinar.config(state='disabled')

        # Evitar duplicados en la lista de palabras ganadas
        if palabra_secreta not in palabras_ganadas:
            palabras_ganadas.append(palabra_secreta)

        global puntos
        puntos += 20  # Sumar puntos por cada palabra ganada
        puntos_label.config(text=f"Puntos totales: {puntos}")

        # Actualizar la lista de palabras ganadas en la interfaz
        actualizar_palabras_ganadas()

        # Añadir 30 segundos extra
        tiempo_restante += 30
        mensaje_temporal("¡Ganaste 30 segundos más!")

        # Mostrar el mensaje temporal y pasar a la siguiente palabra después de 2 segundos
        root.after(2000, lambda: resultado_label.config(
            text=""))  # Eliminar mensaje
        # Cambiar palabra o tema
        root.after(2000, lambda: siguiente_palabra_o_tema())

    elif len(letras_incorrectas) >= intentos:
        resultado_label.config(
            text="¡Perdiste! La palabra era: " + palabra_secreta)
        entry_letra.config(state='disabled')
        boton_adivinar.config(state='disabled')


def siguiente_palabra_o_tema():
    global palabra_secreta, letras_adivinadas, letras_incorrectas, tema_actual

    # Elegir otra palabra del mismo tema si hay palabras disponibles
    if temas_palabras[tema_actual]:
        palabra_secreta = random.choice(temas_palabras[tema_actual]).upper()
        letras_adivinadas = ["_"] * len(palabra_secreta)
        letras_incorrectas = []
        entry_letra.config(state='normal')
        boton_adivinar.config(state='normal')
        actualizar_interfaz()  # Actualizar la interfaz con la nueva palabra
    else:
        # Si el tema se quedó sin palabras, cambiar a otro tema con palabras disponibles
        temas_disponibles = [tema for tema,
                             palabras in temas_palabras.items() if palabras]
        if temas_disponibles:
            tema_actual = random.choice(temas_disponibles)
            reiniciar_juego()  # Seleccionar palabra del nuevo tema
        else:
            resultado_label.config(text="¡No quedan palabras en ningún tema!")
            entry_letra.config(state='disabled')
            boton_adivinar.config(state='disabled')


def mensaje_temporal(mensaje):
    temp_label = tk.Label(root, text=mensaje, font=(
        "Arial", 16), bg="blue", fg="yellow")
    temp_label.pack()
    root.after(3000, temp_label.destroy)


def siguiente_palabra():
    reiniciar_juego()


def adivinar_letra():
    letra = entry_letra.get().upper()
    entry_letra.delete(0, tk.END)

    if letra in palabra_secreta:
        for i, l in enumerate(palabra_secreta):
            if l == letra:
                letras_adivinadas[i] = letra
    else:
        if letra not in letras_incorrectas:
            letras_incorrectas.append(letra)

    actualizar_interfaz()


def reiniciar_juego():
    global palabra_secreta, letras_adivinadas, letras_incorrectas, tiempo_restante, tema_actual, palabras_ganadas

    # Reiniciar los puntos
    global puntos
    puntos = 0
    puntos_label.config(text="Puntos totales: 0")

    # Limpiar lista de palabras ganadas
    palabras_ganadas.clear()
    actualizar_palabras_ganadas()

    # Verificar si ya no hay palabras en el tema actual
    if not temas_palabras[tema_actual]:  # Si el tema actual ya no tiene palabras
        # Cambiar al siguiente tema disponible
        temas_disponibles = [tema for tema,
                             palabras in temas_palabras.items() if palabras]
        if temas_disponibles:
            tema_actual = random.choice(temas_disponibles)
        else:
            # Si no hay más temas, elegir uno al azar
            tema_actual = random.choice(list(temas_palabras.keys()))

    # Elegir una palabra aleatoria del tema actual y reiniciar las variables
    palabra_secreta = random.choice(temas_palabras[tema_actual]).upper()
    letras_adivinadas = ["_"] * len(palabra_secreta)
    letras_incorrectas = []
    tiempo_restante = 300
    resultado_label.config(text="")

    # Restablecer el muñeco
    canvas.delete("all")  # Borrar el muñeco
    entry_letra.config(state='normal')
    boton_adivinar.config(state='normal')

    # Agregar la palabra ganada a la lista de palabras ganadas (si no está ya en la lista)
    if palabra_secreta not in palabras_ganadas:
        palabras_ganadas.append(palabra_secreta)

    # Restaurar las palabras ya usadas al tema (si es necesario)
    temas_palabras[tema_actual].append(palabra_secreta)

    # Actualizar la interfaz
    actualizar_interfaz()


def seleccionar_tema(tema):
    global tema_actual
    tema_actual = tema
    reiniciar_juego()


def actualizar_temporizador():
    global tiempo_restante  # Declara que estás usando la variable global
    if tiempo_restante > 0:
        minutos, segundos = divmod(tiempo_restante, 60)
        temporizador_label.config(
            text=f"Tiempo restante: {minutos:02}:{segundos:02}")
        tiempo_restante -= 1
        root.after(1000, actualizar_temporizador)
    else:
        resultado_label.config(
            text="¡Tiempo agotado! La palabra era: " + palabra_secreta)
        entry_letra.config(state='disabled')
        boton_adivinar.config(state='disabled')


root = tk.Tk()
root.title("Juego del Ahorcado DAVID & CLARK")
root.geometry("1000x700")  # Establecer tamaño inicial de la ventana
root.minsize(1000, 700)
root.config(bg="blue")

# Calcular el centro de la pantalla
ancho_ventana = 1000
alto_ventana = 700
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Ajustar la posición de la ventana
pos_x = int((ancho_pantalla - ancho_ventana) / 2)
# Correcto cálculo para estar a 100 px del borde inferior
pos_y = alto_pantalla - alto_ventana - 100

root.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")

# texto tema elegido
tema_label = tk.Label(root, text=f"Tema elegido: {tema_actual}", font=(
    "Arial", 16), bg="red", fg="white")
tema_label.pack()

# Canvas para el dibujo del muñeco
canvas = tk.Canvas(root, width=200, height=300, bg="white")
canvas.pack(pady=10)

# Frame para el cuadro de palabras ganadas y puntos
frame_palabras = tk.Frame(root, width=200, height=400,
                          bg="white", relief="ridge", borderwidth=2)
# Cambiamos de pack() a place(), ajustando x e y
frame_palabras.place(x=10, y=100)

# Título para el cuadro
titulo_palabras = tk.Label(frame_palabras, text="Palabras ganadas", font=(
    "Arial", 14), bg="white", fg="red")
titulo_palabras.pack(pady=(10, 5))

# Canvas para manejar el scroll de las palabras ganadas
canvas_palabras = tk.Canvas(
    frame_palabras, bg="white", width=180, height=300, highlightthickness=0)
canvas_palabras.pack(side="top", fill="both", expand=True)

# Scrollbar vertical para las palabras ganadas
scrollbar_palabras = tk.Scrollbar(
    frame_palabras, orient="vertical", command=canvas_palabras.yview)
scrollbar_palabras.pack(side="right", fill="y")

# Frame interno para contener las palabras ganadas
frame_interno_palabras = tk.Frame(canvas_palabras, bg="white")
canvas_palabras.create_window(
    (0, 0), window=frame_interno_palabras, anchor="nw")

# Configurar el canvas con el scroll
canvas_palabras.configure(yscrollcommand=scrollbar_palabras.set)

# Ajustar el scroll según el contenido


def ajustar_scroll(event=None):
    canvas_palabras.configure(scrollregion=canvas_palabras.bbox("all"))


frame_interno_palabras.bind("<Configure>", ajustar_scroll)

# Lista de widgets para las palabras ganadas
widgets_palabras = []

# Función para actualizar la lista de palabras ganadas


def actualizar_palabras_ganadas():
    global widgets_palabras

    # Limpiar widgets previos
    for widget in widgets_palabras:
        widget.destroy()
    widgets_palabras.clear()

    # Agregar cada palabra como un ítem en la lista
    for palabra in palabras_ganadas:
        palabra_item = tk.Label(frame_interno_palabras, text=f"- {palabra}", font=(
            "Arial", 12), bg="white", fg="blue", anchor="w", justify="left", wraplength=150)
        palabra_item.pack(anchor="w", padx=5, pady=2)
        widgets_palabras.append(palabra_item)

    ajustar_scroll()  # Ajustar el scroll por si se desborda


# Etiqueta para mostrar los puntos
puntos_label = tk.Label(frame_palabras, text="Puntos totales: 0", font=(
    "Arial", 12), bg="white", fg="red")
puntos_label.pack(pady=5)


palabra_label = tk.Label(root, text=" ".join(
    letras_adivinadas), font=("Arial", 24), bg="blue", fg="white")
palabra_label.pack(pady=10)

errores_label = tk.Label(root, text="Letras incorrectas: ", font=(
    "Arial", 14), bg="blue", fg="white")
errores_label.pack()

entry_letra = tk.Entry(root, font=("Arial", 18))
entry_letra.pack(pady=5)

boton_adivinar = tk.Button(root, text="Adivinar", font=(
    "Arial", 14), bg="red", fg="white", command=adivinar_letra)
boton_adivinar.pack(pady=5)

boton_gracias = tk.Button(root, text="Gracias", font=("Arial", 14), bg="red", fg="white", command=lambda: tk.messagebox.showinfo(
    "Gracias", "Tu colaboración me ayuda a seguir \nmejorando mis proyectos. Incluso 500 $ ayudan. \nAlias: davidask611"))
boton_gracias.pack(pady=5)

resultado_label = tk.Label(root, text="", font=(
    "Arial", 18), bg="blue", fg="white")
resultado_label.pack(pady=10)

temporizador_label = tk.Label(
    root, text="Tiempo restante: 05:00", font=("Arial", 16), bg="blue", fg="white")
temporizador_label.pack(pady=5)

menu_bar = tk.Menu(root)
tema_menu = tk.Menu(menu_bar, tearoff=0)
for tema in temas_palabras.keys():
    tema_menu.add_command(
        label=tema, command=lambda t=tema: seleccionar_tema(t))
menu_bar.add_cascade(label="Temas", menu=tema_menu)
menu_bar.add_command(label="Reiniciar", command=reiniciar_juego)
root.config(menu=menu_bar)

actualizar_interfaz()
actualizar_temporizador()

root.mainloop()
