# 1.将多个后缀为webp的图片合并成一个PDF文件
from PIL import Image, ImageOps
import glob
from natsort import natsorted
import time

def convert_image(img_path):
    try:
        img = Image.open(img_path)
        # 处理旋转和透明度
        img = ImageOps.exif_transpose(img)  # 修正方向
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            return background
        else:
            return img.convert('RGB')
    except Exception as e:
        print(f"错误处理文件 {img_path}: {e}")
        return None

# 获取并排序文件
webp_files = natsorted(glob.glob("*.webp"))

# 转换图片并过滤失败项
images = [img for img in (convert_image(f) for f in webp_files) if img is not None]

if not images:
    print("没有找到可转换的图片！")
    exit()

# 统一尺寸（可选）
# base_size = images[0].size
# images = [img.resize(base_size) if img.size != base_size else img for img in images]

# 生成PDF
pdf_name = f"output_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
images[0].save(pdf_name, save_all=True, append_images=images[1:])

# 关闭所有图片释放内存
for img in images:
    img.close()

print(f"PDF已保存为 {pdf_name}")
