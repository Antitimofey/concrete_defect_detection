from shlex import join
import cv2
import numpy as np
import random
import sys
import os

def compare_images(img1: cv2.typing.MatLike, img2: cv2.typing.MatLike, sample_pixels=1000):

    # Проверяем, что изображения загружены
    if img1 is None or img2 is None:
        raise ValueError("Не удалось загрузить одно из изображений")
    
    # Проверяем, что размеры изображений совпадают
    if img1.shape != img2.shape:
        return -1
        #raise ValueError("Размеры изображений не совпадают")
    
    # Получаем размеры изображения
    height, width, _ = img1.shape
    
    # Генерируем случайные индексы пикселей
    random_indices = [
        (random.randint(0, height - 1), 
        (random.randint(0, width - 1))) 
        for _ in range(sample_pixels)
    ]
    
    matching_pixels = 0
    
    for y, x in random_indices:
        # Получаем значения пикселей
        pixel1 = img1[y, x]
        pixel2 = img2[y, x]
        
        # Сравниваем все 3 канала (BGR)
        if np.array_equal(pixel1, pixel2):
            matching_pixels += 1
    
    # Вычисляем процент совпадения
    match_percentage = (matching_pixels / sample_pixels) * 100
    
    return match_percentage





marked_dir = "разм"  # Папка с размеченными изображениями
clean_dir = "чист"   # Папка с чистыми изображениями

def main():
    working_dir = sys.argv[1]

    full_marked_dir = os.path.join(working_dir, marked_dir)
    full_clean_dir = os.path.join(working_dir, clean_dir)

    for img_name in [f for f in os.listdir(full_marked_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]:
        full_marked_img_name = os.path.join(full_marked_dir, img_name)
        marked_img = cv2.imread(full_marked_img_name)
        
        cv2.imshow("marked_img", marked_img)
        cv2.waitKey(0)

        for clean_img_name in [f for f in os.listdir(full_clean_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]:
            full_clean_img_name = os.path.join(full_clean_dir, clean_img_name)
            clean_img = cv2.imread(full_clean_img_name)
 
            cor = compare_images(marked_img, clean_img)
            if cor > -1:
                print(img_name, clean_img_name, "corr is", cor)

            if cor > 0.6:
                cv2.imshow("clean_img", clean_img)
                cv2.waitKey(0)

    print(full_marked_dir)

    #for img_name in [os.listdir()]












# Пример использования
if __name__ == "__main__":
    main()


