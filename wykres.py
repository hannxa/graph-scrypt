import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, PhotoImage
import matplotlib.pyplot as plt
from contourpy.util.data import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import random
import numpy as np
from numpy.ma.testutils import approx

plot_color = (0, 0, 1)  # domyślny kolor
x_label = 'X'
y_label = 'Y'
title_label = 'Title'
canvas = None
fig = None

def load_file():
    filename = filedialog.askopenfilename(filetypes=[("text files", "*.txt"), ("csv files", "*.csv")])
    if filename:
        entry_file.delete(0, tk.END)  # wyczysc pole tekstowe
        entry_file.insert(0, filename)  # wstaw ścieżkę pliku do pola tekstowego

def choose_color():
    global plot_color
    color = colorchooser.askcolor()[0]
    if color:
        plot_color = tuple(c / 255. for c in color)
        label_color.config(text=f"Chosen color: {plot_color}")  # etykieta z kolorem

def update_labels():
    global x_label, y_label, title_label
    x_label = entry_x_label.get()
    y_label = entry_y_label.get()
    title_label = entry_title.get()
    plot_data(show_approximation=False, standard_deviation=False)  # ponowne rysowanie

def save_plot():
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),("PDF files", "*.pdf")])
    if file_path:
        try:
            fig.savefig(file_path)
            messagebox.showinfo("Success", f"Plot saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save plot: {e}")

def plot_data(show_approximation,standard_deviation):
    global fig, canvas, x_values, y_values
    file_path = entry_file.get()

    if file_path == 'C:/Users/akabe/Desktop/poskProjekt4/special.txt':
        open_special_window()
        return
    if not file_path:
        messagebox.showwarning("Warning", "Please select a file")
        return

    try:
        # wczytanie danych
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # usunięcie pustych linii i zbieranie danych
        lines = [line.strip() for line in lines if line.strip()]
        x_values = []
        y_values = []
        current_column = None

        for line in lines:
            if line == 'X':
                current_column = 'X'
            elif line == 'Y':
                current_column = 'Y'
            else:
                if current_column == 'X':
                    x_values.append(float(line))
                elif current_column == 'Y':
                    y_values.append(float(line))

        # Sprawdź, czy mamy dane do obu kolumn
        if not x_values or not y_values:
            raise ValueError("There are no values for column X or Y")

        if len(x_values) != len(y_values):
            raise ValueError("Columns X and Y do not have the same length")

        # usunięcie poprzedniego wykresu
        for widget in frame_plot.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        # tworzenie wykresu
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, marker='o', color=plot_color)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title_label)
        ax.grid(True)
        if(show_approximation):
            a, b = np.polyfit(x_values, y_values, 1)
            approx_y_values = [a * x + b for x in x_values]
            ax.plot(x_values, approx_y_values, label=f'Approximation Line (y={a:.2f}x + {b:.2f})', color='red')
            ax.legend()
        if(standard_deviation):
            # odchylenie standardowe
            residuals = [y - approx_y for y, approx_y in zip(y_values, approx_y_values)]
            std_dev = np.std(residuals)
            ax.plot([], [], ' ', label=f'Standard Deviation: {std_dev:.2f}', color='green')
            ax.legend()

        # rysowanie wykresu w GUI
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)  # użyj grid w miejscu pack

        btn_save_plot.grid(row=8, column=1, pady=10)  # przyciski pojawią się po narysowaniu wykresu
        btn_line.grid(row=8,column=2,pady=10)
        btn_deviation.grid(row=9,column=2,pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

def open_special_window():
    global root_special, btn_10, btn_0, label_special
    root_special = tk.Toplevel(root)
    frame_special = tk.Frame(root_special)
    frame_special.grid(row=0, column=0, padx=10, pady=10)  # Zamiast pack, użyj grid

    # Przyciski do interakcji
    btn_10 = tk.Button(frame_special, text="10 pkt", command=special_success)
    btn_10.grid(row=1, column=0, padx=10, pady=10)

    btn_0 = tk.Button(frame_special, text="mniej niż 10", command=special_attack)
    btn_0.grid(row=1, column=1, padx=10, pady=10)

    # Dodanie nasłuchiwania na zdarzenie "Enter" (najechanie myszką)
    btn_0.bind("<Enter>", special_attack)  # Wywołanie special_attack po najechaniu na przycisk

    # Label, który będzie zmieniany
    label_special = tk.Label(root_special, text="Przyznane punkty za projekt", font=("Helvetica", 20))
    label_special.grid(row=2, column=0, columnspan=3, pady=10)

def special_attack(event = None):
    random_row = random.randint(0,3)
    random_col = random.randint(0,3)
    btn_0.grid(row=random_row, column=random_col, padx=5, pady=10)

def special_success():
    global gif_frames, gif_index, label_gif
    gif_index = 0
    gif_frames = []

    try:
        # Wczytanie GIF-a za pomocą PIL
        gif = Image.open("C:\\Users\\akabe\\Desktop\\cat-mochi.gif")

        # Iteracja przez klatki GIF-a
        for frame in range(0, gif.n_frames):
            gif.seek(frame)  # Ustawienie na konkretną klatkę
            # Konwersja klatki do formatu PhotoImage
            frame_image = ImageTk.PhotoImage(gif.copy())
            gif_frames.append(frame_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load GIF: {e}")
        return

    label_special.config(text="Dziękujemy")
    label_special.grid(row=3, column=0, columnspan=3, pady=10)

    label_gif = tk.Label(root_special)
    label_gif.grid(row=4, column=0, columnspan=3, pady=10)

            # Uruchom animację, jeśli klatki zostały wczytane
    if gif_frames:
        animate_gif()


def animate_gif():
    global gif_index
    if gif_frames:
        label_gif.config(image=gif_frames[gif_index])  # Ustaw klatkę jako obraz w etykiecie
        gif_index = (gif_index + 1) % len(gif_frames)  # Przejdź do następnej klatki z zapętleniem
        root_special.after(100, animate_gif)  # Wywołaj ponownie po 100 ms


            # tworzenie okna GUI
root = tk.Tk()
root.title("Graph Generator")

# pole do wpisania nazwy pliku
frame_input = tk.Frame(root)
frame_input.grid(row=0, column=0, pady=10)  # zmieniono pack na grid

tk.Label(frame_input, text="Data file: ").grid(row=0, column=0, padx=5)
entry_file = tk.Entry(frame_input, width=40)
entry_file.grid(row=0, column=1, padx=5)
tk.Button(frame_input, text="Load File", command=load_file).grid(row=0, column=2, padx=5)

btn_color = tk.Button(frame_input, text="Choose color", command=choose_color)
btn_color.grid(row=2, column=1, columnspan=1, pady=10)

label_color = tk.Label(frame_input, text=f"Chosen color: {plot_color}")
label_color.grid(row=2, column=2, columnspan=3, pady=5)

tk.Label(frame_input, text="Title: ").grid(row=4, column=1, padx=5)
entry_title = tk.Entry(frame_input, width=40)
entry_title.grid(row=5, column=1, padx=5)
entry_title.insert(0, title_label)

tk.Label(frame_input, text="X label: ").grid(row=6, column=1, padx=5)
entry_x_label = tk.Entry(frame_input, width=40)
entry_x_label.grid(row=7, column=1, padx=5)
entry_x_label.insert(0, x_label)

tk.Label(frame_input, text="Y label: ").grid(row=6, column=2, padx=5)
entry_y_label = tk.Entry(frame_input, width=40)
entry_y_label.grid(row=7, column=2, padx=5)
entry_y_label.insert(0, y_label)

btn_save_plot = tk.Button(frame_input, text="Save Plot", command=save_plot)

btn_update_plot = tk.Button(frame_input, text="Plot Data", command=update_labels)
btn_update_plot.grid(row=8, column=0, columnspan=3, pady=10)

btn_line = tk.Button(frame_input, text="Proximal line", command=lambda: plot_data(show_approximation=True, standard_deviation=False))
btn_deviation = tk.Button(frame_input, text="standard Deviation", command=lambda: plot_data(show_approximation=True, standard_deviation=True))


frame_plot = tk.Frame(root)
frame_plot.grid(row=1, column=0, pady=10)  # frame_plot teraz używa grid


# uruchomienie aplikacji
root.mainloop()
