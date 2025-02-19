# 4.将文件夹下所有压缩包里的图片转换成pdf文件
from PIL import Image, ImageOps
import glob
from natsort import natsorted
import time
import zipfile
import os
import tempfile
import shutil


def convert_image(img_path):
    """处理单张图片：修正方向、转换颜色模式、处理透明度"""
    try:
        img = Image.open(img_path)
        img = ImageOps.exif_transpose(img)  # 修正方向
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert('RGB')
        return img
    except Exception as e:
        print(f"处理失败 {os.path.basename(img_path)}: {str(e)}")
        return None


def extract_zip_to_temp(zip_path):
    """解压ZIP到临时目录"""
    temp_dir = tempfile.mkdtemp(prefix="zip_extract_")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            image_exts = ('.jpg', '.jpeg', '.png', '.webp')
            files = [f for f in zip_ref.namelist() if os.path.splitext(f)[1].lower() in image_exts]
            if not files:
                raise ValueError("无图片文件")
            for f in files:
                zip_ref.extract(f, temp_dir)
        return temp_dir
    except zipfile.BadZipFile:
        shutil.rmtree(temp_dir)
        raise ValueError("ZIP文件损坏")


def process_images_from_zip(zip_path):
    """处理单个ZIP文件"""
    temp_dir = extract_zip_to_temp(zip_path)
    try:
        # 匹配所有子目录中的图片
        extensions = ["jpg", "jpeg", "png", "webp"]
        patterns = [f"**/*.{ext}" for ext in extensions] + [f"**/*.{ext.upper()}" for ext in extensions]

        seen = set()
        all_images = []
        for pattern in patterns:
            for f in glob.glob(os.path.join(temp_dir, pattern), recursive=True):
                if f not in seen and os.path.isfile(f):
                    seen.add(f)
                    all_images.append(f)

        sorted_files = natsorted(all_images, key=lambda x: x.lower())
        images = [img for img in (convert_image(f) for f in sorted_files) if img]

        if not images:
            raise RuntimeError("无有效图片")

        # # 统一尺寸（可选）
        # base_size = images[0].size
        # images = [img.resize(base_size) if img.size != base_size else img for img in images]

        # 生成带ZIP文件名的PDF
        base_name = os.path.splitext(os.path.basename(zip_path))[0]
        pdf_name = f"{base_name}_合并结果_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
        images[0].save(pdf_name, save_all=True, append_images=images[1:], quality=95)
        print(f"生成成功: {pdf_name}")

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    # 获取当前目录所有ZIP文件
    zip_files = glob.glob("*.zip")
    if not zip_files:
        print("错误：目录下无ZIP文件")
        exit(1)

    # 逐个处理
    for zip_path in zip_files:
        try:
            print(f"\n处理中: {os.path.basename(zip_path)}")
            process_images_from_zip(zip_path)
        except Exception as e:
            print(f"处理失败: {str(e)}")