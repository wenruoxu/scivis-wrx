"""
显示库中所有颜色 - 以可视化方式显示颜色库中的所有颜色

用法:
    python show_all_colors.py
    python show_all_colors.py --output all_colors.png
    python show_all_colors.py --sort hue
"""

import os
import sys
import argparse
from pathlib import Path
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scivis_wrx import (
    load_colors,
    rgb_to_hsv,
    BASIC_COLOR_NAMES,
    generate_color_id
)

# 设置输出目录
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
colors_file = output_dir / "image_colors.json"

def load_all_colors():
    """加载所有颜色"""
    # 加载颜色文件中的颜色
    file_colors = {}
    if Path(colors_file).exists():
        try:
            file_colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
            print(f"从 {colors_file} 加载了 {len(file_colors)} 种颜色")
        except Exception as e:
            print(f"加载颜色文件时出错: {e}")
    
    # 如果颜色文件不存在或为空，加载默认颜色
    if not file_colors:
        print("使用默认颜色库")
        for name, color in BASIC_COLOR_NAMES.items():
            color_id = generate_color_id(color)
            file_colors[color_id] = {
                "color": color,
                "name": name
            }
    
    # 转换为列表，便于处理
    colors_list = []
    for color_id, info in file_colors.items():
        name = info["name"]
        color = info["color"]
        h, s, v = rgb_to_hsv(color[:3])
        rgb_values = [int(c * 255) for c in color[:3]]
        hex_code = '#{:02x}{:02x}{:02x}'.format(*rgb_values)
        
        colors_list.append({
            "name": name,
            "color": color,
            "id": color_id,
            "rgb": rgb_values,
            "hex": hex_code,
            "hsv": (h, s, v)
        })
    
    return colors_list

def sort_colors(colors, sort_by="name"):
    """对颜色进行排序"""
    if sort_by == "name":
        return sorted(colors, key=lambda x: x["name"])
    elif sort_by == "rgb":
        return sorted(colors, key=lambda x: sum(x["rgb"]))
    elif sort_by == "hue":
        return sorted(colors, key=lambda x: x["hsv"][0])
    elif sort_by == "saturation":
        return sorted(colors, key=lambda x: x["hsv"][1], reverse=True)
    elif sort_by == "brightness":
        return sorted(colors, key=lambda x: x["hsv"][2], reverse=True)
    else:
        return colors

def display_colors_grid(colors, title="颜色库中的所有颜色"):
    """以网格形式显示所有颜色"""
    n_colors = len(colors)
    if n_colors == 0:
        print("没有颜色可显示")
        return None
    
    # 计算网格尺寸
    cols = min(8, n_colors)  # 最多8列
    rows = (n_colors + cols - 1) // cols
    
    # 创建图形
    fig_width = 3 * cols
    fig_height = 2 * rows
    fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
    fig.suptitle(title, fontsize=16)
    
    # 如果只有一行或一列，确保axes是二维的
    if rows == 1:
        axes = np.array([axes])
    if cols == 1:
        axes = axes.reshape(-1, 1)
    
    # 填充网格
    for i, color_info in enumerate(colors):
        row = i // cols
        col = i % cols
        
        ax = axes[row, col]
        color = color_info["color"]
        
        # 绘制颜色方块
        rect = patches.Rectangle((0, 0.3), 1, 0.7, color=color)
        ax.add_patch(rect)
        
        # 确定文本颜色
        text_color = 'white' if sum(color[:3]) < 1.5 else 'black'
        
        # 在方块上显示颜色信息
        name_text = color_info["name"]
        if len(name_text) > 20:
            name_text = name_text[:17] + "..."
        rgb_text = f"RGB: {color_info['rgb']}"
        hex_text = color_info["hex"]
        
        ax.text(0.5, 0.65, name_text, 
                ha='center', va='center', color=text_color,
                fontsize=8, fontweight='bold')
        ax.text(0.5, 0.5, rgb_text, 
                ha='center', va='center', color=text_color,
                fontsize=7)
        ax.text(0.5, 0.35, hex_text, 
                ha='center', va='center', color=text_color,
                fontsize=7)
        
        # 在底部显示其他信息
        hsv_info = color_info["hsv"]
        hsv_text = f"H: {hsv_info[0]:.0f}° S: {hsv_info[1]*100:.0f}% V: {hsv_info[2]*100:.0f}%"
        ax.text(0.5, 0.15, hsv_text, ha='center', va='center', fontsize=6)
        
        # 设置坐标轴
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    # 处理空白格子
    for i in range(n_colors, rows * cols):
        row = i // cols
        col = i % cols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    return fig

def main():
    parser = argparse.ArgumentParser(description="显示库中所有颜色")
    parser.add_argument("--output", help="输出文件名 (默认: outputs/all_colors.png)")
    parser.add_argument("--sort", choices=["name", "rgb", "hue", "saturation", "brightness"],
                        default="hue", help="颜色排序方式 (默认: hue)")
    parser.add_argument("--show", action="store_true", help="显示颜色窗口")
    
    args = parser.parse_args()
    
    try:
        # 加载所有颜色
        all_colors = load_all_colors()
        print(f"共加载了 {len(all_colors)} 种颜色")
        
        # 排序颜色
        sorted_colors = sort_colors(all_colors, args.sort)
        title = f"颜色库中的所有颜色 (按{args.sort}排序)"
        
        # 显示颜色
        fig = display_colors_grid(sorted_colors, title)
        
        if fig:
            # 保存图像
            if args.output:
                output_path = args.output
                if not output_path.endswith(('.png', '.jpg', '.pdf')):
                    output_path += '.png'
            else:
                output_path = output_dir / f"all_colors_{args.sort}.png"
            
            fig.savefig(output_path, dpi=150)
            print(f"颜色图像已保存至: {output_path}")
            
            # 显示窗口
            if args.show:
                plt.show()
            else:
                plt.close(fig)
        
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 