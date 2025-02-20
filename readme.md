# 图片转PDF工具集 

📦 四阶段演进式工具集 | 从基础WebP处理到批量ZIP转换全覆盖

---

## 🗂 文件清单
| 版本 | 文件名 | 核心功能 |
|------|--------|----------|
| 基础版 | `webp_images_to_pdf.py` | 单目录WebP转PDF |
| 增强版 | `images_to_PDF.py` | 多格式图片转PDF |
| 扩展版 | `one_zip_to_PDF.py` | 单ZIP文件转PDF |
| 终极版 | `all_zip_to_PDF.py` | 批量ZIP转PDF |

---

## 🚀 功能叠加示意图

基础版 → 增强版 → 扩展版 → 终极版
[基础版] → [+多格式] → [+ZIP支持] → [+批量处理]

### 各版本适用场景
| 版本   | 最佳使用场景     | 示例                        |
| ------ | ---------------- | --------------------------- |
| 基础版 | 快速转换WebP截图 | 手机相册导出的.webp文件     |
| 增强版 | 混合格式图片整理 | 扫描件（部分JPG+部分PNG）   |
| 扩展版 | 接收压缩包素材   | 设计师提供的图片压缩包      |
| 终极版 | 批量处理多个项目 | 按日期分类的多个ZIP备份文件 |

---

## 📜 版本特性对比

| 功能特性                | 基础版 | 增强版 | 扩展版 | 终极版 |
|------------------------|-------|-------|-------|-------|
| WebP格式支持           | ✅    | ✅    | ✅    | ✅    |
| 多图片格式支持         | ❌    | ✅    | ✅    | ✅    |
| 自然排序               | ✅    | ✅    | ✅    | ✅    |
| 透明背景处理           | ✅    | ✅    | ✅    | ✅    |
| EXIF方向校正           | ✅    | ✅    | ✅    | ✅    |
| ZIP文件支持            | ❌    | ❌    | ✅    | ✅    |
| 批量ZIP处理            | ❌    | ❌    | ❌    | ✅    |
| 子目录图片搜索         | ❌    | ❌    | ✅    | ✅    |
| 自动清理临时文件       | ❌    | ❌    | ✅    | ✅    |
| 错误隔离机制           | 基础  | 基础  | 增强  | 增强  |

---


## 🛠 环境配置

### 基础要求

```python
# 安装Python依赖
pip install pillow natsort
```

### 系统支持

| 系统    | 安装命令                       |
| :------ | :----------------------------- |
| Windows | 无需额外操作                   |
| Ubuntu  | `sudo apt install libwebp-dev` |
| macOS   | `brew install webp jpeg-turbo` |

------

## 🧭 使用指南

### 基础版：WebP转PDF

```python
# 将webp图片放入当前目录
python webp_images_to_pdf.py
# 生成 output_年月日_时分秒.pdf
```

### 增强版：多格式转PDF

```python
# 支持jpg/png/webp等格式
python images_to_PDF.py
```

### 扩展版：单ZIP转PDF

```python
# 需准备1.zip文件
python one_zip_to_PDF.py
# 生成带时间戳的PDF
```

### 终极版：批量ZIP转PDF

```python
# 自动处理所有zip文件
python all_zip_to_PDF.py
# 每个zip生成独立PDF（文件名_合并结果_时间戳.pdf）
```

---

## ⚙️ 高级配置

### 统一图片尺寸

```python
# 在任意版本中取消注释以下代码
# base_size = images[0].size
# images = [img.resize(base_size)...]
```

### 扩展支持格式

```python
# 增强版/扩展版/终极版修改：
extensions = ["jpg", "png", "bmp", "tiff"]  # 添加新格式
```

### 设置输出DPI

```python
# 在.save()方法中添加参数（仅扩展版）
images[0].save(pdf_name, ..., resolution=300)  # 默认300dpi
```

------

## 🧠 智能处理逻辑

### 文件排序策略

1. 自然排序数字编号（img1 < img2 < img10）
2. 混合格式时按扩展名字典序排列（jpg → png → webp）
3. ZIP版本优先保留压缩包内目录结构

### 错误隔离机制

- 单文件处理失败不影响整体流程
- 损坏ZIP文件自动跳过并报错
- 内存保护：强制关闭所有图片句柄

### 格式优先级

同名文件按扩展名排序：
`img.A.jpg` → `img.B.png` → `img.C.webp`

------

## 🚨 常见问题排查

| 现象             | 解决方案                           |
| :--------------- | :--------------------------------- |
| "无有效图片"警告 | 检查文件扩展名是否在支持列表       |
| ZIP文件处理失败  | 确认压缩包未加密且包含图片文件     |
| 生成PDF方向错误  | 更新Pillow库：`pip upgrade pillow` |
| 内存不足         | 分批次处理（建议单次≤500张图片）   |
| 临时文件残留     | 手动删除`/tmp/zip_extract_*`目录   |

---

## 📊 性能优化建议

1. **大文件预处理**
   建议对超过10MB的图片进行压缩：

   ```python
   img = img.resize((1920, 1080))  # 添加到convert_image函数
   ```

2. **并行处理模式**
   终极版可添加多线程加速：

   ```python
   from concurrent.futures import ThreadPoolExecutor
   ```

3. **缓存机制**
   重复处理相同文件时可添加缓存逻辑：

   ```python
   from functools import lru_cache
   @lru_cache(maxsize=100)
   ```

------

📌 **最佳实践**：推荐使用终极版`all_zip_to_PDF.py`，支持最全面的功能和最佳错误处理机制。对于简单场景可使用增强版`images_to_PDF.py`保持轻量化。

