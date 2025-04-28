"""
颜色提取示例 - 从图片中提取颜色并创建调色板
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from scivis_wrx.colors import colors
from scivis_wrx.elements import elements

def plot_with_image_palette(image_path, palette_name='image_palette'):
    """
    使用从图片中提取的颜色绘制示例图表
    
    参数:
        image_path: 图片文件路径
        palette_name: 为调色板取的名称
    """
    # 显示原始图片
    fig = plt.figure(figsize=(12, 8))
    fig.suptitle(f"从图片中提取颜色示例: {os.path.basename(image_path)}", fontsize=14)
    
    # 添加原始图片子图
    ax_image = plt.subplot2grid((2, 3), (0, 0), colspan=1, rowspan=1)
    img = plt.imread(image_path)
    ax_image.imshow(img)
    ax_image.set_title("原始图片")
    ax_image.axis('off')
    
    # 从图片中提取颜色并创建调色板
    extracted_colors = colors.create_palette_from_image(palette_name, image_path, color_count=5)
    
    # 显示提取的颜色
    ax_palette = plt.subplot2grid((2, 3), (0, 1), colspan=2, rowspan=1)
    for i, color in enumerate(extracted_colors):
        ax_palette.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
    
    ax_palette.set_xlim(0, len(extracted_colors))
    ax_palette.set_ylim(0, 1)
    ax_palette.set_xticks([i + 0.5 for i in range(len(extracted_colors))])
    ax_palette.set_xticklabels([f"{color}" for color in extracted_colors])
    ax_palette.set_yticks([])
    ax_palette.set_title(f"提取的颜色 (共{len(extracted_colors)}种)")
    
    # 使用提取的颜色创建柱状图
    ax_bar = plt.subplot2grid((2, 3), (1, 0), colspan=1, rowspan=1)
    x = np.arange(len(extracted_colors))
    y = np.random.rand(len(extracted_colors)) * 10
    ax_bar.bar(x, y, color=extracted_colors)
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels([f"类别{i+1}" for i in range(len(extracted_colors))])
    ax_bar.set_title("柱状图示例")
    elements.set_grid(ax_bar, style='subtle')
    
    # 使用提取的颜色创建折线图
    ax_line = plt.subplot2grid((2, 3), (1, 1), colspan=1, rowspan=1)
    x = np.linspace(0, 10, 100)
    for i, color in enumerate(extracted_colors):
        ax_line.plot(x, np.sin(x + i*0.5) + i*0.5, color=color, label=f"系列{i+1}")
    
    ax_line.set_title("折线图示例")
    elements.set_grid(ax_line, style='dashed')
    elements.set_legend(ax_line, style='minimal')
    
    # 使用提取的颜色创建饼图
    ax_pie = plt.subplot2grid((2, 3), (1, 2), colspan=1, rowspan=1)
    ax_pie.pie(np.random.rand(len(extracted_colors)) + 1, colors=extracted_colors, 
               autopct='%1.1f%%', startangle=90)
    ax_pie.set_title("饼图示例")
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    return fig

def main():
    """主函数"""
    # 提供一些图片路径作为示例
    # 用户需要替换为实际的图片路径
    image_path = "示例图片.jpg"  # 替换为你的图片路径
    
    # 检查图片是否存在
    if not os.path.exists(image_path):
        print(f"图片 {image_path} 不存在！请修改图片路径。")
        return
    
    # 从图片中提取颜色并绘制示例图表
    fig = plot_with_image_palette(image_path)
    plt.show()

if __name__ == "__main__":
    main() 