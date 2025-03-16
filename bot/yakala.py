import cv2
import numpy as np
import pyautogui
import time
from pynput import keyboard
import matplotlib.pyplot as plt

# Çemberin merkezi ve yarıçapı
center = (238, 223)  # Merkez koordinatları (X, Y)
radius = 67.6  # Yarıçap (piksel cinsinden)

# Balık görüntü dosyalarının yolları
fish_image_paths = [
    r'C:\bot\fiss.jpg',
    r'C:\bot\fiss1.jpg',
    r'C:\bot\fiss2.jpg',
    r'C:\bot\fiss3.jpg'
]

# Referans resminin dosya yolu
reference_image_path = r'C:\bot\ref3.png'

# Balık resimlerini yükle
fish_images = [cv2.imread(path) for path in fish_image_paths]

# Kontrol et: Tüm balık resimleri yüklendi mi?
for path in fish_image_paths:
    if path is None:
        raise FileNotFoundError(f"{path} dosyası bulunamadı.")

reference_image = cv2.imread(reference_image_path)
if reference_image is None:
    raise FileNotFoundError(f"{reference_image_path} dosyası bulunamadı.")

# Çıkış durumu için değişken
exit_program = False

def on_press(key):
    global exit_program
    if key == keyboard.Key.esc:
        exit_program = True

# Renk tabanlı maskeleme fonksiyonu
def color_mask(image):
    # Renk aralıklarını tanımlayın
    lower_fish_color = np.array([30, 70, 100])  # Balık için alt sınır (BGR)
    upper_fish_color = np.array([70, 130, 160])  # Balık için üst sınır (BGR)
    lower_water_color = np.array([20, 80, 80])  # Su için alt sınır (BGR)
    upper_water_color = np.array([60, 150, 150])  # Su için üst sınır (BGR)

    # Balık maskesi oluştur
    fish_mask = cv2.inRange(image, lower_fish_color, upper_fish_color)
    # Su maskesi oluştur
    water_mask = cv2.inRange(image, lower_water_color, upper_water_color)

    # Balık ve su maskelerini birleştir
    combined_mask = cv2.bitwise_and(fish_mask, cv2.bitwise_not(water_mask))
    return combined_mask

# Görüntü ön işleme fonksiyonu
def preprocess_image(image):
    # Gri tonlama
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Gaussian bulanıklığı
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Kenar algılama
    edges = cv2.Canny(blurred, 100, 200)
    return edges

# Ekranı sürekli kontrol eden ana döngü
while not exit_program:
    # Ekran görüntüsü al
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Referans resmini kontrol et
    reference_result = cv2.matchTemplate(screenshot, reference_image, cv2.TM_CCOEFF_NORMED)
    reference_threshold = 0.8  # Eşleşme eşiği
    ref_loc = np.where(reference_result >= reference_threshold)

    # Eğer referans resmi bulunursa balığı aramaya başla
    if ref_loc[0].size > 0:
        print("Referans resmi bulundu, balık aranmaya başlanıyor...")

        # Ekran görüntüsünü renk tabanlı maskele
        fish_mask = color_mask(screenshot)

        # Maske ile ekran görüntüsünü birleştir
        masked_image = cv2.bitwise_and(screenshot, screenshot, mask=fish_mask)

        # Ekran görüntüsünü ön işleme tabi tut
        edges = preprocess_image(masked_image)

        for fish_image in fish_images:
            # Balığın ekran üzerindeki konumunu bul
            fish_result = cv2.matchTemplate(edges, cv2.cvtColor(fish_image, cv2.COLOR_BGR2GRAY), cv2.TM_CCOEFF_NORMED)
            fish_threshold = 0.8  # Eşleşme eşiği
            fish_loc = np.where(fish_result >= fish_threshold)

            for pt in zip(*fish_loc[::-1]):  # Eşleşme noktalarını döngü ile gez
                fish_center = (pt[0] + fish_image.shape[1] // 2, pt[1] + fish_image.shape[0] // 2)

                # Merkez ile balık merkezi arasındaki mesafeyi hesapla
                distance = np.sqrt((fish_center[0] - center[0])**2 + (fish_center[1] - center[1])**2)

                # Eğer balık çemberin içindeyse tıkla
                if distance <= radius:
                    pyautogui.click(fish_center[0], fish_center[1])  # Balığın ortasına tıkla
                    print(f"Tıklama yapıldı: {fish_center}")
                    time.sleep(1)  # Tıklama sonrası 1 saniye bekle (hızlı tıklamayı önlemek için)

        # Matplotlib ile görüntüleri göster
        plt.subplot(131)
        plt.imshow(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        plt.title('Ekran Görüntüsü')
        plt.axis('off')

        plt.subplot(132)
        plt.imshow(fish_mask, cmap='gray')
        plt.title('Balık Maskesi')
        plt.axis('off')

        plt.subplot(133)
        plt.imshow(cv2.cvtColor(masked_image, cv2.COLOR_BGR2RGB))
        plt.title('Masked Image')
        plt.axis('off')

        plt.show(block=False)  # Görüntüleri engellemeyen şekilde göster
        plt.pause(0.001)  # Görüntüleri güncellemek için kısa bir bekleme süresi

    else:
        print("Referans resmi bulunamadı.")

    time.sleep(0.1)  # Her döngü arasında 0.1 saniye bekle

listener.stop()  # Dinleyiciyi durdur
print("Program sona erdi.")
