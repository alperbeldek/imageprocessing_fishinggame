import tkinter as tk
import subprocess
import random

# Global değişkenler
fishing_process = None

# Daktilo efekti için global değişkenler
footer_text = ""
footer_index = 0
footer_display = ""
is_deleting = False

def start_fishing():
    global fishing_process
    if fishing_process is None:
        fishing_process = subprocess.Popen(['pythonw.exe', 'C:\\bot\\balikc.py'], creationflags=subprocess.CREATE_NO_WINDOW)

def stop_fishing():
    global fishing_process
    if fishing_process:
        fishing_process.terminate()
        fishing_process = None

def toggle_fishing():
    if fishing_btn['bg'] == 'lime':
        fishing_btn['bg'] = 'red'
        fishing_btn['text'] = 'Fishing: OFF'
        stop_fishing()
    else:
        fishing_btn['bg'] = 'lime'
        fishing_btn['text'] = 'Fishing: ON'
        start_fishing()

def on_closing():
    stop_fishing()
    root.destroy()

# Matrix animasyonu
def matrix_animation():
    canvas.delete("all")
    for i in range(20):  # 20 sütun
        x = i * 10
        if random.random() > 0.95:  # %5 olasılıkla bir karakter oluştur
            char = random.choice("01")
            canvas.create_text(x, random.randint(0, 200), text=char, fill="lime", font=("Courier", 8))
    canvas.after(100, matrix_animation)

# Daktilo efekti
def type_effect():
    global footer_display, footer_index, is_deleting
    target_text = "make money don't worry"
    
    if not is_deleting:
        if footer_index < len(target_text):
            footer_display += target_text[footer_index]
            footer_index += 1
        else:
            is_deleting = True
    else:
        if footer_index > 0:
            footer_display = footer_display[:-1]
            footer_index -= 1
        else:
            is_deleting = False
    
    footer_label.config(text=footer_display)
    root.after(150, type_effect)  # Her 150 ms'de bir güncelle

# GUI Oluşturma
root = tk.Tk()
root.title("$")
root.geometry("200x200")  # Pencere boyutu
root.configure(bg="black")

# Matrix arka planı
canvas = tk.Canvas(root, width=200, height=200, bg="black")
canvas.pack()

# Matrix animasyonunu başlat
matrix_animation()

# Özel tasarım butonları
button_style = {
    'bg': 'red',
    'fg': 'white',
    'font': ('Courier', 8),
    'width': 12,
    'activebackground': 'lime',
}

# Butonu tam ortada konumlandır
fishing_btn = tk.Button(root, text="Fishing: OFF", command=toggle_fishing, **button_style)
fishing_btn.place(relx=0.5, rely=0.5, anchor='center')  # Ekranın tam ortasında konumlandır

# Metin ekleme
footer_label = tk.Label(root, text="", font=("Courier New", 10, "italic"), bg="black", fg="lime")
footer_label.place(relx=0.5, rely=0.85, anchor='center')  # Metni yukarıda konumlandır

# Daktilo efekti başlatma
type_effect()

# X tuşuna basıldığında durdurma
root.protocol("WM_DELETE_WINDOW", on_closing)

# Uygulamayı başlat
root.mainloop()
