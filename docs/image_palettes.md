# 图片调色板功能

本文档介绍如何使用图片提取颜色功能来创建自定义调色板。

## 概述

图片调色板功能允许您从任意图片中提取主要颜色，并将这些颜色用作数据可视化的调色板。这个功能非常适合：

- 创建与特定图像匹配的颜色主题
- 从真实世界的自然图像中获取和谐的颜色组合
- 保持品牌一致性，使用品牌图像中的颜色

## 基本用法

### 从图片中提取颜色

```python
from scivis_wrx.colors import colors

# 从图片中提取5种颜色并创建名为"my_image_palette"的调色板
extracted_colors = colors.create_palette_from_image(
    name="my_image_palette", 
    image_path="path/to/image.jpg", 
    color_count=5
)

# 打印提取的颜色
print(extracted_colors)
```

### 使用提取的颜色绘图

提取颜色后，可以直接使用这些颜色绘制图表：

```python
import matplotlib.pyplot as plt
import numpy as np

# 提取颜色后，直接使用palette_name获取调色板
my_palette = colors.get_palette("my_image_palette")

# 创建一个简单的柱状图
plt.figure(figsize=(10, 6))
x = np.arange(len(my_palette))
y = np.random.rand(len(my_palette)) * 10
plt.bar(x, y, color=my_palette)
plt.title("使用图片调色板的柱状图")
plt.show()
```

## 高级选项

### 排除白色

默认情况下，提取颜色时会排除白色和接近白色的颜色。如果需要包含白色，可以设置`exclude_white=False`：

```python
colors.create_palette_from_image(
    name="with_white_palette", 
    image_path="path/to/image.jpg", 
    exclude_white=False
)
```

### 自定义颜色数量

您可以指定要从图片中提取的颜色数量：

```python
# 提取10种颜色
colors.create_palette_from_image(
    name="ten_colors", 
    image_path="path/to/image.jpg", 
    color_count=10
)
```

### 查看可用的图片调色板

您可以列出所有已保存的图片调色板：

```python
available_palettes = colors.get_image_palettes()
print(available_palettes)
```

## 示例

完整示例演示了如何从图片中提取颜色并应用于不同类型的图表：

```python
from scivis_wrx.colors import colors
from scivis_wrx.elements import elements
import matplotlib.pyplot as plt
import numpy as np

# 从图片中提取颜色
image_path = "path/to/beautiful_image.jpg"
extracted_colors = colors.create_palette_from_image("image_palette", image_path)

# 创建图表
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("使用图片调色板的示例", fontsize=16)

# 显示原始图片
img = plt.imread(image_path)
axes[0, 0].imshow(img)
axes[0, 0].set_title("原始图片")
axes[0, 0].axis('off')

# 显示提取的颜色
for i, color in enumerate(extracted_colors):
    axes[0, 1].add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
axes[0, 1].set_xlim(0, len(extracted_colors))
axes[0, 1].set_ylim(0, 1)
axes[0, 1].set_title("提取的颜色")
axes[0, 1].set_xticks([])
axes[0, 1].set_yticks([])

# 柱状图示例
x = np.arange(len(extracted_colors))
y = np.random.rand(len(extracted_colors)) * 10
axes[1, 0].bar(x, y, color=extracted_colors)
axes[1, 0].set_title("柱状图示例")
elements.set_grid(axes[1, 0], style='subtle')

# 折线图示例
x = np.linspace(0, 10, 100)
for i, color in enumerate(extracted_colors):
    axes[1, 1].plot(x, np.sin(x + i*0.5) + i*0.5, color=color, label=f"系列{i+1}")
axes[1, 1].set_title("折线图示例")
elements.set_grid(axes[1, 1], style='dashed')
elements.set_legend(axes[1, 1])

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()
```

## 技术细节

图片颜色提取使用以下技术：

1. 将图片调整为较小尺寸以提高处理速度
2. 将像素转换为RGB颜色空间
3. 可选地排除白色和接近白色的像素
4. 使用K-means聚类算法提取主要颜色
5. 将RGB值转换为十六进制颜色代码 