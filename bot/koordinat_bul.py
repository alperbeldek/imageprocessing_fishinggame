import pyautogui
import keyboard
import time

# Log dosyasının yolu
log_file_path = "C:\\bot\\yem_koordinatlari.txt"

def log_coordinate():
    # Koordinatı al ve dosyaya yaz
    x, y = pyautogui.position()  # Mevcut mouse konumunu al
    with open(log_file_path, 'a') as file:
        file.write(f"{x},{y}\n")  # Koordinatları dosyaya yaz

if __name__ == "__main__":
    print("Koordinatları kaydetmek için mouse ile bir yere gidin ve 'Enter' tuşuna basın.")
    print("Çıkmak için 'q' tuşuna basın.")

    while True:
        if keyboard.is_pressed('Enter'):  # 'Enter' tuşuna basıldığında
            log_coordinate()
            print(f"Koordinat kaydedildi: {pyautogui.position()}")
            time.sleep(1)  # Çok hızlı kaydedilmesini önlemek için 1 saniye bekle

        if keyboard.is_pressed('q'):  # 'q' tuşuna basıldığında çık
            print("Programdan çıkılıyor.")
            break
