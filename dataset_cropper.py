import os
import cv2
import numpy as np
import re




# Пути к папкам
marked_dir = "разм"  # Папка с размеченными изображениями
clean_dir = "чист"   # Папка с чистыми изображениями
output_dir = "crop"   # Папка для сохранения вырезанных областей

# Создаем папку для результатов, если ее нет
os.makedirs(output_dir, exist_ok=True)

# Параметры для определения красного контура
red_min = np.array([0, 0, 220], dtype=np.uint8)
red_max = np.array([40, 40, 255], dtype=np.uint8)

# Минимальная площадь контура (0.1% от площади изображения)
min_contour_area_percent = 0.001

# Функция для обработки изображений
def process_images():
    # Получаем список файлов в папке с размеченными изображениями
    marked_files = [f for f in os.listdir(marked_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    for marked_file in marked_files:
        # Загружаем размеченное изображение
        marked_path = os.path.join(marked_dir, marked_file)
        marked_img = cv2.imread(marked_path)
        
        if marked_img is None:
            print(f"Не удалось загрузить изображение: {marked_path}")
            continue
        
        # Получаем высоту и ширину изображения
        height, width = marked_img.shape[:2]
        image_area = height * width
        min_contour_area = image_area * min_contour_area_percent
        
        # Создаем маску для красного цвета
        red_mask = cv2.inRange(marked_img, red_min, red_max)
        
        # Находим контуры на маске
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(marked_img, contours, -1, (0,255,0), 4)
        cv2.imshow("img", marked_img)
        cv2.waitKey(0)
        
        # Фильтруем контуры по площади
        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= min_contour_area]
        #print(f"largest contour area is {large_contours}")
        
        if not large_contours:
            print(f"Не найдено подходящих контуров в {marked_file}")
            continue
        
        # Находим соответствующий чистый файл
        # Ищем файл, который начинается с того же числа (предполагаем формат "число_...")
        file_prefix = marked_file.split('_')[0]
        file_prefix = re.match(r"\d+", marked_file).group()
        clean_files = [f for f in os.listdir(clean_dir) if f.startswith(file_prefix) and f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not clean_files:
            print(f"Не найден соответствующий чистый файл для {marked_file} \
                  (поиск по префиксу {file_prefix})")
            continue
        
        # Берем первый подходящий файл
        clean_file = clean_files[0]
        clean_path = os.path.join(clean_dir, clean_file)
        clean_img = cv2.imread(clean_path)
        
        if clean_img is None:
            print(f"Не удалось загрузить чистое изображение: {clean_path}")
            continue

        
        # Обрабатываем каждый контур
        for i, contour in enumerate(large_contours):
            # Получаем ограничивающий прямоугольник
            x, y, w, h = cv2.boundingRect(contour)
            
            # Вырезаем область из чистого изображения
            cropped = clean_img[y:y+h, x:x+w]
            
            # Сохраняем вырезанную область
            output_filename = f"{os.path.splitext(marked_file)[0]}_crop_{i}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            cv2.imwrite(output_path, cropped)
            
            print(f"Сохранено: {output_path}")

if __name__ == "__main__":
    process_images()
    print("Обработка завершена!")