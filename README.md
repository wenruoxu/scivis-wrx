# Scivis_wrx - 科学可视化颜色管理工具

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-green)

Scivis_wrx 是为科学可视化设计的颜色管理工具套件，帮助研究人员和数据科学家创建专业、一致的色彩方案，提升数据可视化效果。该工具专注于颜色提取、管理和生成，支持各种专业的配色方案。

## 主要特性

- **智能颜色提取**：从图像中提取主要颜色并保存到颜色库
- **专业色板生成**：支持多种色彩理论生成配色方案（互补色、三元色、单色等）
- **ID-based 颜色管理**：颜色ID反映色彩特性，便于相似颜色查找
- **智能命名系统**：根据颜色特性自动生成描述性名称
- **色彩可视化工具**：直观展示颜色库和色板效果

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/scivis_wrx.git
cd scivis_wrx

# 安装依赖
pip install -e .
```

依赖项:
- matplotlib
- numpy
- Pillow
- scipy (可选)

## 快速入门

### 从图像提取颜色

```bash
# 从单个图像提取颜色
python example/image_color_extraction.py path/to/image.jpg

# 从目录中提取颜色
python example/image_color_extraction.py path/to/image_directory

# 显示详细信息
python example/image_color_extraction.py path/to/image.jpg -v
```

### 生成色板

```bash
# 生成互补色色板
python example/color_palette_generator.py --type complementary --num 2 --show

# 生成蓝色系列的单色色板
python example/color_palette_generator.py --family blue --type monochromatic --num 5 --show

# 生成三元色配色，并显示使用示例
python example/color_palette_generator.py --type triadic --examples --show
```

### 显示所有颜色

```bash
# 显示颜色库中所有颜色
python example/show_all_colors.py --sort hue

# 按亮度排序
python example/show_all_colors.py --sort brightness
```

## 详细功能

### 颜色提取与管理

Scivis_wrx 的核心是基于ID的颜色管理系统，每个颜色都有一个唯一的ID，反映其RGB值和HSV特性。这使得系统能够:

- 准确存储和检索颜色
- 智能查找相似颜色
- 根据色彩理论生成配色方案

提取的颜色自动保存在颜色库中，可以跨项目复用。

### 色板类型

支持多种专业的色板类型:

- **complementary**: 互补色（色环上相对的颜色）
- **brightness**: 从深到浅的颜色渐变
- **similar**: 相似色（饱和度变化）
- **triadic**: 三元色（色环上等距的三种颜色）
- **tetradic**: 四方配色（两对互补色）
- **analogous**: 相邻色（色环上相邻的颜色）
- **monochromatic**: 单色配色（相同色相，不同饱和度和亮度）
- **split-complementary**: 分割互补色（一个基础色和两个互补色两侧的颜色）

每种色板类型都遵循专业的色彩理论，适用于不同的设计和数据可视化场景。

### 色彩可视化

工具提供了多种可视化方式:

- 图像颜色提取可视化
- 相似颜色对比
- 互补色展示
- 从深到浅的色板展示
- 全库颜色网格展示
- 配色方案的实际应用示例

## 编程接口

### 颜色管理

```python
from scivis_wrx import generate_color_id, load_colors, save_colors, rgb_to_hsv

# 生成颜色ID
color = (0.2, 0.5, 0.8)  # RGB格式 (0-1)
color_id = generate_color_id(color)  # 返回唯一的颜色ID

# 加载颜色库
colors = load_colors("outputs/image_colors.json", include_meta=True, use_id_as_key=True)

# 保存颜色到库
save_colors(colors, "outputs/image_colors.json")

# RGB转HSV
h, s, v = rgb_to_hsv(color)
```

### 颜色提取

```python
from scivis_wrx import extract_dominant_colors, add_colors_from_image

# 从图像提取主要颜色
dominant_colors = extract_dominant_colors(
    "path/to/image.jpg", 
    n_colors=5, 
    exclude_white=True
)

# 将颜色添加到颜色库
color_names = add_colors_from_image(
    "path/to/image.jpg",
    "outputs/image_colors.json",
    n_colors=5
)
```

### 查找相关颜色

```python
from scivis_wrx import find_similar_colors, find_complementary_colors, find_similar_colors_by_brightness

# 查找相似颜色
similar_colors = find_similar_colors(color, "outputs/image_colors.json", max_results=5)

# 查找互补色
complementary_colors = find_complementary_colors(color, "outputs/image_colors.json", max_results=2)

# 查找按亮度排序的相似色
similar_by_brightness = find_similar_colors_by_brightness(color, "outputs/image_colors.json", max_results=5)
```

## 配置选项

所有示例程序都支持多种命令行选项，使用 `-h` 或 `--help` 参数查看帮助信息:

```bash
python example/color_palette_generator.py --help
python example/image_color_extraction.py --help
python example/show_all_colors.py --help
```

## 应用场景

- **科学研究**: 为学术论文和报告创建专业、一致的配色方案
- **数据可视化**: 为图表和可视化选择最佳配色
- **UI/UX设计**: 从图片中提取颜色创建协调的用户界面
- **品牌设计**: 基于品牌图像创建配色系统
- **可访问性设计**: 创建考虑色盲人士的高对比度配色方案

## 最佳实践

- 对于科学论文，推荐使用互补色或三元色配色方案
- 对于数据可视化，推荐使用单色或相邻色方案表示连续数据
- 对于分类数据，推荐使用三元色或四方配色方案
- 始终考虑色彩可访问性，避免仅依赖颜色传达信息

## 贡献

欢迎贡献和改进建议！请通过 GitHub issues 或 pull requests 提交。

## 许可

本项目采用 MIT 许可证。

## 联系方式

有问题或建议请联系:
- Email: your.email@example.com
- GitHub: https://github.com/yourusername/scivis_wrx