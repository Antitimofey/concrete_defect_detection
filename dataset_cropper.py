import os, sys
import cv2
import numpy as np
import re
from typing import List



# Пути к папкам
marked_dir = "разм"  # Папка с размеченными изображениями
#marked_dir = re.compile(r"(Р|р)азм")
clean_dir = "чист"   # Папка с чистыми изображениями
#clean_dir = re.compile(r"(Ч|ч)ист")
output_dir = "crop"   # Папка для сохранения вырезанных областей

# Параметры для определения красного контура
red_min = np.array([0, 0, 220], dtype=np.uint8)
red_max = np.array([40, 40, 255], dtype=np.uint8)

# Минимальная площадь контура (0.1% от площади изображения)
min_contour_area_percent = 0.001


'''
def process_images(marked_dir: str):
    """Ваша функция обработки изображений"""
    print(f"Processing images in: {marked_dir}")
    # Здесь должна быть ваша реализация обработки изображений
    # ...
'''



# Функция для обработки изображений
def process_images(defect_dir: str, output_dir: str = "crop", debug_on:bool = False):
    # Создаем папку для результатов, если ее нет
    output_dir = os.path.join(defect_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Получаем список файлов в папке с размеченными изображениями
    marked_files = [f for f in os.listdir(os.path.join(defect_dir, marked_dir)) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    for marked_file in marked_files:
        # Загружаем размеченное изображение
        marked_path = os.path.join(defect_dir, marked_dir, marked_file)
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

        if debug_on:
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
        # Ищем файл, который начинается с того же числа (предполагаем формат "число...")
        pattern = re.match(r"\d+", marked_file)
        if pattern is None: # если такого файла нет
            print(f"не выделить число из файла {marked_file}") 
            continue
        file_prefix = pattern.group()
        clean_files = [f for f in os.listdir(os.path.join(defect_dir, clean_dir)) if f.startswith(file_prefix) and f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not clean_files:
            print(f"Не найден соответствующий чистый файл для {marked_file} \
                  в папке {defect_dir} (поиск по префиксу {file_prefix})")
            continue
        
        # Берем первый подходящий файл
        clean_file = clean_files[0]
        clean_path = os.path.join(defect_dir, clean_dir, clean_file)
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
            
            try:
                cv2.imwrite(output_path, cropped)
                print(f"Сохранено: {output_path}")
            except Exception as e:
                print(f'error while saving image {output_path}, shape is {cropped.shape}')
                print(f'contour area is {cv2.contourArea(contour)}')


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    
    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} is not a valid directory")
        sys.exit(1)
    
    # Получаем список всех подпапок первого уровня
    subdirs: List[str] = []
    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path):
            subdirs.append(full_path)
    
    # Обрабатываем каждую подпапку
    for subdir in subdirs:
        process_images(subdir)

    print('Обработка завершена!')

def mono_main():
    process_images(sys.argv[1])

if __name__ == "__main__":
    main()
    #mono_main()