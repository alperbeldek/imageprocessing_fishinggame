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
    (650, 290), (684, 290), (717, 293), (746, 292), (773, 290),
    (646, 320), (679, 320), (711, 323), (745, 323), (776, 323),
    (647, 353), (677, 354), (711, 354), (748, 353), (774, 355),
    (650, 386), (676, 383), (713, 383), (742, 386), (775, 386),
    (647, 418), (680, 420), (708, 418), (741, 416), (772, 416),
    (647, 449), (682, 449), (711, 449), (748, 450), (776, 450),
    (648, 482), (682, 484), (717, 484), (744, 483), (772, 481),
    (649, 516), (680, 516), (711, 513), (741, 516), (774, 513),
    (649, 547), (678, 545), (711, 545), (742, 546), (775, 546),
]

# Başlangıçta yem indeksini sıfırla
current_yem_index = 0

def find_image_on_screen(target_image):
    template = cv2.imread(target_image, cv2.IMREAD_GRAYSCALE)
    if template is None:
        return False  # Görsel bulunamazsa False döner

    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    yloc, xloc = np.where(result >= threshold)
    
    return len(xloc) > 0  # Eşleşme varsa True döner

def click_coordinates_sequence(coordinates):
    for x, y in coordinates:
        pyautogui.moveTo(x, y, duration=0.3)  # Koordinata git (daha hızlı)
        pyautogui.click()  # Tıklama yap
        time.sleep(0.2)  # Daha kısa bekleme süresi

def main():
    global current_yem_index
    while True:
        if keyboard.is_pressed('k'):
            break  # 'K' tuşuna basıldığında döngüyü kır

        if find_image_on_screen(target_image):
            click_coordinates_sequence(click_coordinates[:2])  # İlk iki temel koordinata tıkla
            
            if current_yem_index < len(yem_coordinates):
                pyautogui.moveTo(yem_coordinates[current_yem_index], duration=0.5)  # Yem koordinatına git
                pyautogui.click()  # Tıklama yap
                time.sleep(0.5)  # Yem tıklaması sonrası bekleme
                current_yem_index += 1  # Sonraki yem koordinatına geç
            
            click_coordinates_sequence(click_coordinates[2:])  # Kalan temel koordinatlara tıkla

            if current_yem_index >= len(yem_coordinates):
                current_yem_index = 0  # Tüm yemler kullanıldıysa başa dön
            
            # Her döngü tamamlandığında 3 ve 4 tuşlarına bas
            keyboard.press_and_release('3')
            keyboard.press_and_release('4')

        time.sleep(1)  # Eşleşme kontrolü için 1 saniye bekle

if __name__ == "__main__":
    main()
