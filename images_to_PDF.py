# 2.将图片合并成一个PDF文件
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

# 获取所有图片并按文件名排序（支持多格式）
# webp_files = natsorted(glob.glob("*.jpg") + glob.glob("*.png") + glob.glob("*.webp"))

# 定义需要匹配的格式列表
extensions = ["jpg", "jpeg", "png", "webp"]

# 生成通配符模式，如 ["*.jpg", "*.png", "*.webp"]
# patterns = [f"*.{ext}" for ext in extensions]

# 生成大小写敏感的通配符模式（覆盖 .JPG 和 .jpg）
patterns = []
for ext in extensions:
    patterns.extend([f"*.{ext.lower()}", f"*.{ext.upper()}"])

# 合并所有匹配的文件
# all_images = []
# for pattern in patterns:
#     all_images.extend(glob.glob(pattern))
#
# webp_files = natsorted(all_images)

# 合并并去重文件路径（保持顺序）
seen = set()
all_images = []
for pattern in patterns:
    for f in glob.glob(pattern):
        if f not in seen:
            seen.add(f)
            all_images.append(f)

# 自然排序文件
sorted_files = natsorted(all_images)

# 转换图片并过滤失败项
images = [img for img in (convert_image(f) for f in sorted_files) if img is not None]

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