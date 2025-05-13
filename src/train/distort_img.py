import os
import cv2
import numpy as np
import random
from PIL import Image, ImageEnhance


def add_gaussian_noise(img, mean=0, var=5):  # 减小噪声强度
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, img.shape).astype(np.float32)
    noisy = cv2.add(img.astype(np.float32), gauss)
    return np.clip(noisy, 0, 255).astype(np.uint8)


def apply_motion_blur(img, size=3):  # 减小模糊强度
    kernel = np.zeros((size, size))
    kernel[int((size - 1) / 2), :] = np.ones(size)
    kernel = kernel / size
    return cv2.filter2D(img, -1, kernel)


def apply_affine_shear(img, strength=0.02):
    rows, cols = img.shape[:2]
    shear_x = random.uniform(-strength, strength)
    shear_y = random.uniform(-strength, strength)
    M = np.float32([[1, shear_x, 0], [shear_y, 1, 0]])
    return cv2.warpAffine(img, M, (cols, rows), borderMode=cv2.BORDER_REFLECT)


def apply_rotation(img, angle=0.05):
    rows, cols = img.shape[:2]
    rand_angle = random.uniform(-angle, angle)
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rand_angle, 1)
    return cv2.warpAffine(img, M, (cols, rows), borderMode=cv2.BORDER_REFLECT)


def chop_random_region(img, chop_height=2):
    h, w = img.shape[:2]
    if h <= chop_height + 1:
        return img
    top = random.randint(0, h - chop_height - 1)
    return np.delete(img, slice(top, top + chop_height), axis=0)


def adjust_brightness_contrast(pil_img):
    contrast = random.uniform(0.9, 1.1)
    brightness = random.uniform(0.9, 1.1)
    pil_img = ImageEnhance.Contrast(pil_img).enhance(contrast)
    pil_img = ImageEnhance.Brightness(pil_img).enhance(brightness)
    return pil_img


def get_distortion_strength(height):
    if height > 4500:
        return 0.0
    elif height > 3500:
        return 0.25
    elif height > 2500:
        return 0.5
    else:
        return 1.0


def distort_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".png"):
            continue

        path = os.path.join(input_folder, filename)
        img = cv2.imread(path)
        if img is None:
            print(f"[跳过] 无法读取图像: {filename}")
            continue

        h, w = img.shape[:2]
        strength = get_distortion_strength(h)

        # 按图像长度比例调整扰动强度
        if strength > 0 and random.random() < 0.3 * strength:
            img = apply_affine_shear(img, strength=0.02 * strength)

        if strength > 0 and random.random() < 0.3 * strength:
            img = apply_rotation(img, angle=0.05 * strength)

        if strength > 0 and random.random() < 0.3 * strength:
            img = chop_random_region(img, chop_height=1)

        if random.random() < 0.4:  # 减小模糊的强度
            img = apply_motion_blur(img, size=3)

        if random.random() < 0.5:  # 减小噪声的强度
            img = add_gaussian_noise(img, var=5)

        if random.random() < 0.4:
            img = cv2.medianBlur(img, 3)

        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img_pil = adjust_brightness_contrast(img_pil)

        name, _ = os.path.splitext(filename)
        new_filename = f"{name}_distortion.png"
        output_path = os.path.join(output_folder, new_filename)
        img_pil.save(output_path, quality=90, optimize=True)

        print(f"已处理: {filename} → {new_filename}")


if __name__ == "__main__":
    distort_images(r"F:\Graduation Design\Dataset\new\images",
                   r"F:\Graduation Design\Dataset\new\images\output")
