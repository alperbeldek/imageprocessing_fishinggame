import cv2
import numpy as np
import pyautogui
import time
import keyboard

# Eşleşme için aranan görselin yolu
target_image = "C:\\bot\\bitti1.png"

# Tıklanacak temel koordinatlar
click_coordinates = [
    (720, 610),  # Envanter
    (776, 261),  # 4. Envanter
    (401, 613),  # Yem ceb
    (783, 239),  # Yeni koordinat 1
    (785, 49),   # Yeni koordinat 2
    (731, 303)   # Yeni koordinat 3
]

# Yem koordinatları
yem_coordinates = [
    (650, 290),
    (684, 290),
    (717, 293),
    (746, 292),
    (773, 290),
    (646, 320),
    (679, 320),
    (711, 323),
    (745, 323),
    (776, 323),
    (647, 353),
    (677, 354),
    (711, 354),
    (748, 353),
    (774, 355),
    (650, 386),
    (676, 383),
    (713, 383),
    (742, 386),
    (775, 386),
    (647, 418),
    (680, 420),
    (708, 418),
    (741, 416),
    (772, 416),
    (647, 449),
    (682, 449),
    (711, 449),
    (748, 450),
    (776, 450),
    (648, 482),
    (682, 484),
    (717, 484),
    (744, 483),
    (772, 481),
    (649, 516),
    (680, 516),
    (711, 513),
    (741, 516),
    (774, 513),
    (649, 547),
    (678, 545),
    (711, 545),
    (742, 546),
    (775, 546),
]

# Başlangıçta yem indeksini sıfırla
current_yem_index = 0

def find_image_on_screen(target_image):
    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(target_image, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.95
    yloc, xloc = np.where(result >= threshold)
    
    return len(xloc) > 0  # Eşleşme varsa True döner

def click_coordinates_sequence(coordinates):
    for x, y in coordinates:
        print(f"Tıklanacak koordinatlar: ({x}, {y})")  # Hata ayıklama için
        pyautogui.moveTo(x, y, duration=0.5)  # Koordinata git
        pyautogui.click()  # Tıklama yap
        time.sleep(0.5)  # 0.5 saniye bekle

def main():
    print("Metin2 penceresine odaklanıldı.")
    
    global current_yem_index
    while True:
        if keyboard.is_pressed('k'):  # 'K' tuşuna basılıp basılmadığını kontrol et
            print("Program durduruluyor...")
            break

        if find_image_on_screen(target_image):
            # İlk iki temel koordinata tıkla
            click_coordinates_sequence(click_coordinates[:2])
            
            # Yem koordinatına tıklama
            if current_yem_index < len(yem_coordinates):
                print(f"Yem koordinatına tıklanıyor: {yem_coordinates[current_yem_index]}")
                pyautogui.moveTo(yem_coordinates[current_yem_index], duration=0.7)  # Koordinata git
                pyautogui.click()  # Tıklama yap
                time.sleep(0.7)  # Yem tıklaması sonrası bekleme
                current_yem_index += 1  # Sonraki yem koordinatına geç
            
            # Kalan temel koordinatlara tıklama
            click_coordinates_sequence(click_coordinates[2:])  # 3. koordinattan itibaren devam et

            if current_yem_index >= len(yem_coordinates):  # Eğer tüm yemler kullanıldıysa başa dön
                current_yem_index = 0
            
            # Her döngü tamamlandığında 3 ve 4 tuşlarına bas
            keyboard.press('3')
            time.sleep(0.1)  # 3 tuşuna bastıktan sonra kısa bir bekleme
            keyboard.release('3')  # 3 tuşunu bırak
            keyboard.press('4')
            time.sleep(0.1)  # 4 tuşuna bastıktan sonra kısa bir bekleme
            keyboard.release('4')  # 4 tuşunu bırak

        else:
            print("Görüntü bulunamadı, bekleniyor...")
        
        time.sleep(1)  # Eşleşme kontrolü için 1 saniye bekle

if __name__ == "__main__":
    main()
