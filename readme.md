# 图片转PDF工具集 

📦 包含两个版本的图片转PDF工具：基础版（WebP专用）和增强版（多格式支持），一键合并图片为PDF

---

## 📥 获取代码
- **基础版**：`webp_images_to_pdf.py`（仅支持WebP格式）
- **增强版**：`images_to_PDF.py`（支持JPG/PNG/WebP等格式）

------

## 🆚 版本对比

| 功能特性       | 基础版        | 增强版                   |
| :------------- | :------------ | :----------------------- |
| 支持格式       | 仅 .webp      | .jpg/.jpeg/.png/.webp 等 |
| 文件名匹配     | 严格大小写    | 兼容大小写（自动匹配）   |
| 文件排序       | 简单字典序    | 自然排序（智能编号识别） |
| 重复文件处理   | 无            | 自动去重                 |
| 透明背景转换   | ✅             | ✅                        |
| EXIF方向校正   | ✅             | ✅                        |
| 多格式混合处理 | ❌             | ✅                        |
| 统一尺寸功能   | ✅（手动启用） | ✅（手动启用）            |

------

## 🚀 快速开始

### 基础版（WebP专用）

```bash
# 1. 将webp图片放入当前目录
# 2. 运行命令
python webp_images_to_pdf.py
# 生成 output_20250216_153045.pdf
```

### 增强版（推荐）

```bash
# 1. 将图片（JPG/PNG/WEBP）放入当前目录
# 2. 运行命令
python images_to_PDF.py
# 生成带时间戳的PDF文件，自动合并所有图片
```

------

## 🛠️ 环境配置

### 基础要求

- Python 3.6+

- 安装依赖库：

  ```bash
  pip install pillow natsort
  ```

### 系统支持

| 系统    | 安装命令                       |
| :------ | :----------------------------- |
| Windows | 无需额外操作                   |
| Ubuntu  | `sudo apt install libwebp-dev` |
| macOS   | `brew install webp jpeg-turbo` |

------

## ⚙️ 高级功能

### 启用统一尺寸

```python
# 在两个版本中取消以下注释：
# base_size = images[0].size
# images = [img.resize(base_size)...]
```

### 扩展支持格式（增强版）

```python
# 修改 extensions 列表：
extensions = ["jpg", "png", "webp", "bmp"]  # 添加新格式
```

### 自定义输出路径

```python
# 修改两个版本中的 pdf_name：
pdf_name = "/自定义路径/output.pdf"  # 确保目录存在
```

------

## 📝 使用规范

### 文件命名建议

- 使用连续数字编号：`img_01.webp`, `img_02.jpg`
- 避免特殊字符：`!@#$%^&*`

### 格式优先级

同名文件按扩展名排序：
`img.A.jpg` → `img.B.png` → `img.C.webp`

------

## 🐞 常见问题

### 找不到图片文件

1. 检查文件扩展名是否在支持列表
2. 确认文件位于脚本同级目录
3. 尝试使用绝对路径：`/home/user/images/*.webp`

### 图片方向错误

```bash
pip install --upgrade pillow  # 更新到最新版本
```

### 透明背景失效

- 确保输出模式为RGB（代码已自动处理）
- 检查Alpha通道是否正常

------

## 📜 版本更新日志

### v2.0（增强版）

- 新增多格式混合支持
- 支持大小写不敏感匹配
- 优化文件去重逻辑
- 增强错误处理机制

### v1.0（基础版）

- 实现WebP转PDF基础功能
- 支持EXIF方向校正
- 透明背景自动转换

------

> 📌 建议优先使用增强版

