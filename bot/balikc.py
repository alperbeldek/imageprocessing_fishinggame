import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
from pynput.keyboard import Key, Controller, Listener
import os
import pydirectinput
import math
from windowcapture import WindowCapture
from hsvfilter import HsvFilter
import constants
from PIL import ImageGrab
from threading import Thread

# Çıkış durumu için değişken tanımlanıyor
exit_program = False

# PyAutoGUI güvenlik özelliğini devre dışı bırak
pyautogui.FAILSAFE = False

keyboard_controller = Controller()

window_title = "Metin2"
try:
    window = gw.getWindowsWithTitle(window_title)[0]
    window.activate()
    time.sleep(1)

    # Pencereyi tam ekran yap
    window.maximize()
    
except IndexError:
    exit()

# Referans görüntülerinin bulunduğu dizin
reference_dir = r'C:\bot\refler'
reference_images = []

# Dizin içindeki tüm resimleri yükle
for filename in os.listdir(reference_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(reference_dir, filename)
        img = cv2.imread(image_path)
        if img is not None:
            reference_images.append((filename, img))

# Hedef görüntü dosyası
target_image_path = r"C:\bot\tuttu.png"
target_image = cv2.imread(target_image_path)

# Ref3 görüntüsü
reference_image3_path = r'C:\bot\ref3.png'
reference_image3 = cv2.imread(reference_image3_path)

def on_press(key):
    global exit_program
    if hasattr(key, 'char') and key.char == 'k':
        exit_program = True  # K tuşuna basıldığında çıkış yap

listener = Listener(on_press=on_press)
listener.start()

# Eşleşme fonksiyonu
def find_image_on_screen(image):
    screen = ImageGrab.grab()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(result >= threshold)
    return loc

import time  # time modülünü ekleyelim

import time  # time modülünü ekleyelim

import time  # time modülünü ekleyelim

def reference_clicking_loop():
    ref3_missing_start_time = None  # ref3'ün kaybolmaya başladığı zamanı başta None olarak tanımlıyoruz
    ref3_was_missing = False  # ref3'ün kaybolup kaybolmadığını kontrol edeceğiz

    while True:  # Sonsuz döngü
        x, y, width, height = window.left, window.top, window.width, window.height  # Ekran alanı tanımlaması
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))  # Ekran görüntüsünü alıyoruz
        except Exception as e:
            print(f"Hata oluştu: {e}")  # Hata mesajını yazdırıyoruz
            continue  # Eğer ekran görüntüsü alınamazsa döngü devam eder

        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)  # BGR formatına çeviriyoruz
        processed_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Gri tonlamaya çeviriyoruz

        found_reference = False  # Referans bulunmadı
        for filename, reference_image in reference_images:  # Referans görselleri üzerinde döngü
            reference_image_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)  # Gri tonlamaya çeviriyoruz
            result = cv2.matchTemplate(processed_screenshot, reference_image_gray, cv2.TM_CCOEFF_NORMED)  # Görüntüleri karşılaştırıyoruz
            loc = np.where(result >= 0.85)  # Eşleşme arıyoruz (0.95 eşik değeri)

            if len(loc[0]) > 0:  # Eğer eşleşme varsa
                found_reference = True
                time.sleep(7)
                break  # Döngüyü sonlandırıyoruz

        # Eğer referans bulunmazsa
        if not found_reference:
            reference_image3_gray = cv2.cvtColor(reference_image3, cv2.COLOR_BGR2GRAY)  # Alternatif bir referans
            result3 = cv2.matchTemplate(processed_screenshot, reference_image3_gray, cv2.TM_CCOEFF_NORMED)
            loc3 = np.where(result3 >= 0.7)  # Daha düşük eşik değeri ile eşleşme arıyoruz

            if len(loc3[0]) > 0:  # Eğer bu alternatif referansla eşleşme varsa
                time.sleep(0.1)
                keyboard_controller.press(Key.esc)
                time.sleep(0.1)
                keyboard_controller.release(Key.esc)
                time.sleep(0.1)

                for _ in range(2):
                    time.sleep(0.1)
                    keyboard_controller.press('g')
                    time.sleep(0.1)
                    keyboard_controller.release('g')
                    time.sleep(0.1)

                time.sleep(0.4)
                keyboard_controller.press('3')
                time.sleep(0.1)
                keyboard_controller.release('3')
                time.sleep(0.1)

                time.sleep(0.4)

                keyboard_controller.press('4')
                time.sleep(0.1)
                keyboard_controller.release('4')
                time.sleep(0.1)


        locations = find_image_on_screen(target_image)
        if locations[0].size > 0:
            time.sleep(6)

            for _ in range(2):
                    keyboard_controller.press('g')
                    time.sleep(0.1)
                    keyboard_controller.release('g')
                    time.sleep(0.1)

            time.sleep(0.4)
            keyboard_controller.press('3')
            time.sleep(0.1)
            keyboard_controller.release('3')
            time.sleep(0.1)

            time.sleep(0.4)

            keyboard_controller.press('4')
            time.sleep(0.1)
            keyboard_controller.release('4')
            time.sleep(0.1)





          # ref3 bulunmadıysa ve kaybolmasından 6 saniye geçtiyse
        if len(loc3[0]) == 0:  # Eğer ref3 bulunmazsa
            if not ref3_was_missing:
                ref3_missing_start_time = time.time()  # ref3 kaybolmaya başladığı zamanı başlatıyoruz
                ref3_was_missing = True  # ref3'ün kaybolduğunu işaretliyoruz

            # Eğer 6 saniye geçtiyse ve ref3 hala yoksa
            if (time.time() - ref3_missing_start_time) >= 6.5:
                print("ref3 6 saniye boyunca bulunamadı. Tekrar '4' tuşuna basılıyor.")
               
                keyboard_controller.press('3')
                time.sleep(0.1)
                keyboard_controller.release('3')
                time.sleep(0.1)

                time.sleep(0.4)
 
                keyboard_controller.press('4')
                time.sleep(0.1)
                keyboard_controller.release('4')
                time.sleep(0.1)
                # ref3 kaybolduğunda zaman başlatmayı sıfırlıyoruz
                ref3_missing_start_time = None  # Zamanı sıfırlıyoruz
                ref3_was_missing = False  # ref3'ün kaybolma durumunu sıfırlıyoruz

        # Eğer ref3 tekrar ekranda varsa, zamanı sıfırlıyoruz
        else:
            ref3_missing_start_time = None  # ref3 tekrar bulunduğunda zamanı sıfırlıyoruz
            ref3_was_missing = False  # ref3'ün kaybolma durumunu sıfırlıyoruz


            
       # Balık yakalama
class FishingBot:
    def __init__(self):
        self.fish_pos_x = None
        self.fish_pos_y = None
        self.fish_last_time = None

        self.FISH_RANGE = 74
        self.FISH_VELO_PREDICT = 30
        self.FISH_WINDOW_SIZE = (281, 251)
        self.FISH_WINDOW_POSITION = (100, 54)

        self.wincap = WindowCapture(constants.GAME_NAME)
        self.hsv_filter = HsvFilter(49, 0, 58, 134, 189, 189, 0, 0, 0, 0)

        self.needle_img = cv2.imread('images/fiss.jpg', cv2.IMREAD_UNCHANGED)
        self.loop_time = time.time()
        self.timer_mouse = time.time()

    def detect(self, haystack_img):
        result = cv2.matchTemplate(haystack_img, self.needle_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        needle_w = self.needle_img.shape[1]
        needle_h = self.needle_img.shape[0]

        if max_val > 0.5:
            pos_x = max_loc[0] + needle_w / 2
            pos_y = max_loc[1] + needle_h / 2

            if self.fish_last_time:
                dist = math.sqrt((pos_x - self.fish_pos_x) ** 2 + (self.fish_pos_y - pos_y) ** 2)
                velo = dist / (time.time() - self.fish_last_time)

                if velo >= 150:
                    pro = self.FISH_VELO_PREDICT / dist
                    destiny_x = int(pos_x + (pos_x - self.fish_pos_x) * pro)
                    destiny_y = int(pos_y + (pos_y - self.fish_pos_y) * pro)
                    return (destiny_x, destiny_y)

            self.fish_pos_x = pos_x
            self.fish_pos_y = pos_y
            self.fish_last_time = time.time()

            return (pos_x, pos_y)

        return None

    def run(self):
        while not exit_program:
            screenshot = self.wincap.get_screenshot()
            crop_img = screenshot[self.FISH_WINDOW_POSITION[1]:self.FISH_WINDOW_POSITION[1] + self.FISH_WINDOW_SIZE[1],
                                  self.FISH_WINDOW_POSITION[0]:self.FISH_WINDOW_POSITION[0] + self.FISH_WINDOW_SIZE[0]]

            crop_img = self.hsv_filter.apply_hsv_filter(crop_img)

            square_pos = self.detect(crop_img)

            if square_pos:
                pos_x = square_pos[0]
                pos_y = square_pos[1]

                center_x = self.FISH_WINDOW_SIZE[0] / 2
                center_y = self.FISH_WINDOW_SIZE[1] / 2

                d = self.FISH_RANGE ** 2 - ((center_x - pos_x) ** 2 + (center_y - pos_y) ** 2)

                if d > 0 and (time.time() - self.timer_mouse) > 0.3:
                    mouse_x = int(pos_x + self.FISH_WINDOW_POSITION[0] + self.wincap.offset_x)
                    mouse_y = int(pos_y + self.FISH_WINDOW_POSITION[1] + self.wincap.offset_y)
                    pydirectinput.click(x=mouse_x, y=mouse_y)
                    self.timer_mouse = time.time()



# NewFunctionality Sınıfı
class NewFunctionality:
    def __init__(self):
        self.target_image = "C:\\bot\\bitti1.png"
        self.yem_image = "C:\\bot\\sonyem.png"
        self.click_coordinates = [
            (717, 581),  # Envanter
            (691, 232),  # 2. Envanter
            (398, 584),  # Yem ceb
            (784,209),  # x
            (785,22),   #x
            (749, 198),   #uzay
            (416, 23)    #uzay      
        ]
        self.yem_coordinates = [
            (648, 261), (679, 259), (712, 260), (744, 259), (777, 262),
            (652, 292), (684, 292), (712, 292), (745, 290), (780, 295),
            (650, 324), (680, 321), (714, 322), (744, 322), (778, 324),
            (650, 359), (679, 355), (714, 356), (743, 356), (776, 359),
            (653, 389), (684, 385), (715, 391), (747, 387), (777, 390),
            (650, 419), (683, 416), (712, 419), (744, 419), (778, 420),
            (650, 452), (682, 451), (715, 451), (745, 454), (777, 455),
            (649, 485), (679, 479), (717, 482), (744, 486), (773, 482),
            (645, 518), (685, 514), (714, 514), (746, 516), (778, 517),
        ]
        self.current_yem_index = 0

    def find_image_on_screen(self, target_image):
        try:
            screen = ImageGrab.grab()
            screen_np = np.array(screen)
            screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

            template = cv2.imread(target_image, cv2.IMREAD_GRAYSCALE)
            result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)

            threshold = 0.95
            yloc, xloc = np.where(result >= threshold)
            return len(xloc) > 0
        except Exception as e:
            return False

    def click_coordinates_sequence(self, coordinates):
        for x, y in coordinates:
            pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)

    def run(self):
        while not exit_program:
            if self.find_image_on_screen(self.target_image):
                self.click_coordinates_sequence(self.click_coordinates[:2])
                
                if self.current_yem_index < len(self.yem_coordinates):
                    pyautogui.moveTo(self.yem_coordinates[self.current_yem_index], duration=0.3)
                    pyautogui.click()
                    time.sleep(0.7)
                    self.current_yem_index += 1
                
                self.click_coordinates_sequence(self.click_coordinates[2:])

                if self.current_yem_index >= len(self.yem_coordinates):
                    self.current_yem_index = 0
                
                keyboard_controller.press('3')
                time.sleep(0.1)
                keyboard_controller.release('3')
                time.sleep(0.1)
                keyboard_controller.press('4')
                time.sleep(0.1)
                keyboard_controller.release('4')

                
            elif self.find_image_on_screen(self.yem_image):
                time.sleep(9)
            else:
                time.sleep(1)

# Ana fonksiyon
def main():
    fishing_bot = FishingBot()
    new_functionality = NewFunctionality()
    
    # Thread oluşturarak her üç fonksiyonu aynı anda çalıştırıyoruz
    Thread(target=fishing_bot.run).start()
    Thread(target=new_functionality.run).start()

        # Referans görüntü kontrolü
    reference_clicking_loop()

if __name__ == "__main__":
    main()
