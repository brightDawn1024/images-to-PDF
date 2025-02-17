# 3.将文件夹下的一个压缩包里的图片转换成pdf文件
from PIL import Image, ImageOps
import glob
from natsort import natsorted
import time
import zipfile
import os
import tempfile


def convert_image(img_path):
    """处理单张图片：修正方向、转换颜色模式、处理透明度"""
    try:
        img = Image.open(img_path)
        # 处理旋转（根据EXIF信息自动修正方向）
        img = ImageOps.exif_transpose(img)
        # 处理透明度（RGBA转RGB白底）
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert('RGB')  # 确保统一为RGB模式
        return img
    except Exception as e:
        print(f"处理文件失败 {os.path.basename(img_path)}: {str(e)}")
        return None


def extract_zip_to_temp(zip_path):
    """解压ZIP文件到临时目录，返回解压目录路径"""
    # 创建临时目录（自动清理）
    temp_dir = tempfile.mkdtemp(prefix="zip_images_")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 过滤非图片文件（按扩展名）
            image_exts = ('.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP')
            file_list = [f for f in zip_ref.namelist() if f.lower().endswith(image_exts)]

            if not file_list:
                raise ValueError("压缩包中未找到支持的图片文件")

            # 解压文件并保持目录结构
            for file in file_list:
                zip_ref.extract(file, temp_dir)

            return temp_dir
    except zipfile.BadZipFile:
        raise ValueError("无效的ZIP文件")
    except Exception as e:
        # 清理临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise RuntimeError(f"解压失败: {str(e)}")


def process_images_from_zip(zip_path):
    """主处理流程：解压ZIP → 处理图片 → 生成PDF"""
    # 解压到临时目录
    temp_dir = extract_zip_to_temp(zip_path)

    try:
        # 递归匹配所有子目录中的图片
        extensions = ["jpg", "jpeg", "png", "webp"]
        patterns = []
        for ext in extensions:
            patterns.append(f"**/*.{ext.lower()}")  # 匹配子目录
            patterns.append(f"**/*.{ext.upper()}")  # 匹配大写扩展名

        # 合并并去重文件路径
        seen = set()
        all_images = []
        for pattern in patterns:
            # 注意：recursive=True 允许匹配子目录
            for f in glob.glob(os.path.join(temp_dir, pattern), recursive=True):
                if f not in seen and os.path.isfile(f):  # 过滤目录
                    seen.add(f)
                    all_images.append(f)

        # 自然排序（保持数字顺序）
        sorted_files = natsorted(all_images, key=lambda x: x.lower())  # 统一小写排序

        # 转换图片并过滤失败项
        images = []
        for f in sorted_files:
            converted = convert_image(f)
            if converted:
                images.append(converted)

        if not images:
            raise RuntimeError("没有成功转换的图片")

        # 统一尺寸（以第一张图片为基准）
        # if images:
        #     base_size = images[0].size
        #     images = [img.resize(base_size) if img.size != base_size else img for img in images]

        # 生成PDF文件名（带时间戳）
        pdf_name = f"output_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
        images[0].save(
            pdf_name,
            save_all=True,
            append_images=images[1:],
            resolution=300,  # 设置DPI（默认72可能不够清晰）
            quality=95  # 压缩质量（1-95）
        )

        print(f"PDF生成成功: {os.path.abspath(pdf_name)}")

    finally:
        # 清理临时目录
        import shutil
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    import os

    # 动态获取压缩包路径（脚本所在目录下的 images.zip）
    script_dir = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录
    zip_name = "1.zip"  # 你的压缩包文件名
    zip_path = os.path.join(script_dir, zip_name)  # 拼接完整路径

    if not os.path.exists(zip_path):
        print(f"错误：压缩包 {zip_path} 不存在")
        exit(1)

    try:
        process_images_from_zip(zip_path)
    except Exception as e:
        print(f"处理失败: {str(e)}")