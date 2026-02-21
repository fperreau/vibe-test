import tkinter as tk

def on_click(button_text):
    """
    Gère les clics sur les boutons de la calculatrice.

    Args:
        button_text (str): Le texte du bouton cliqué.
    """
    current_text = entry.get()
    if button_text == "=":
        try:
            result = eval(current_text)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Erreur")
    elif button_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, button_text)

def on_resize(event):
    """
    Gère le redimensionnement de la fenêtre pour ajuster la taille de la police.

    Args:
        event: L'événement de redimensionnement.
    """
    # Calculer la nouvelle taille de la police en fonction de la taille de la fenêtre
    new_font_size = max(12, int(event.width / 30))
    new_font = ('Arial', new_font_size)
    entry.config(font=new_font)
    for button in buttons:
        button.config(font=new_font)

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Calculatrice")

# Configuration de la grille pour qu'elle s'étende
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Champ de saisie
entry = tk.Entry(root, width=20, font=('Arial', 16))
entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

# Boutons de la calculatrice
buttons = []
button_texts = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

row_val = 1
col_val = 0

for button_text in button_texts:
    button = tk.Button(root, text=button_text, width=5, height=2, font=('Arial', 16),
                       command=lambda b=button_text: on_click(b))
    button.grid(row=row_val, column=col_val, sticky="nsew")
    buttons.append(button)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Lier l'événement de redimensionnement à la fonction on_resize
root.bind("<Configure>", on_resize)

# Lancer la boucle principale de l'application
root.mainloop()