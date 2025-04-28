"""
色板生成器 - 从颜色库中选择颜色组成色板，包括相对色和从深到浅的相近色

用法:
    python color_palette_generator.py --num 5 --type complementary
    python color_palette_generator.py --family red --num 8 --type brightness
    python color_palette_generator.py --output my_palette.png
"""

import os
import sys
import json
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scivis_wrx import (
    get_color,
    load_colors,
    save_colors,
    generate_color_id,
    rgb_to_hsv,
    Color,
    BASIC_COLOR_NAMES
)

# 设置输出目录
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
colors_file = output_dir / "image_colors.json"

def get_colors_from_library(family=None, num_colors=5, palette_type="complementary"):
    """从颜色库中获取颜色"""
    # 加载所有颜色
    if Path(colors_file).exists():
        all_colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    else:
        # 如果颜色文件不存在，使用默认颜色
        all_colors = {}
        for name, color in BASIC_COLOR_NAMES.items():
            color_id = generate_color_id(color)
            all_colors[color_id] = {
                "color": color,
                "name": name
            }
    
    # 如果没有颜色，返回空列表
    if not all_colors:
        print("警告: 颜色库为空")
        return [], "空色板"
    
    # 转换为列表，便于处理
    color_list = [(info["name"], info["color"], color_id) for color_id, info in all_colors.items()]
    
    # 如果指定了颜色系列，筛选出相关颜色
    filtered_colors = color_list
    if family:
        family = family.lower()
        filtered_colors = [(name, color, color_id) for name, color, color_id in color_list
                          if family in name.lower() or 
                             (family in BASIC_COLOR_NAMES and 
                              any(abs(c1 - c2) < 0.3 for c1, c2 in zip(color[:3], BASIC_COLOR_NAMES[family])))]
        
        if not filtered_colors:
            print(f"警告: 没有找到'{family}'系列的颜色，使用所有颜色")
            filtered_colors = color_list
    
    # 辅助函数
    def find_closest_color_by_hue(colors_list, target_h):
        """找到色相最接近目标值的颜色"""
        closest_color = None
        min_diff = 1.0
        
        for color_info in colors_list:
            h = color_info[2]  # 色相值
            diff = min(abs(h - target_h), 1.0 - abs(h - target_h))
            if diff < min_diff:
                min_diff = diff
                closest_color = color_info
                
        return closest_color
    
    # 将颜色转换为带HSV的格式，便于处理
    colors_with_hsv = []
    for name, color, color_id in filtered_colors:
        h, s, v = rgb_to_hsv(color[:3])
        # 将HSV标准化到0-1范围
        h = h / 360.0  # 将色相从0-360度转换为0-1
        colors_with_hsv.append((name, color, h, s, v, color_id))
    
    # 根据请求的类型排序颜色
    selected_colors = []
    
    if palette_type == "complementary":
        # 改进版本的互补色算法
        if num_colors == 2:
            # 真正的互补色（相差180°）
            base_color = None
            for name, color, h, s, v, color_id in colors_with_hsv:
                if base_color is None or "primary" in name.lower():
                    base_color = (name, color, h, s, v, color_id)
                    break
            
            if base_color is None and colors_with_hsv:
                # 找不到主色，选择第一个饱和度高的颜色
                sorted_by_sat = sorted(colors_with_hsv, key=lambda x: x[3], reverse=True)
                base_color = sorted_by_sat[0]
            
            if base_color:
                name, color, h, s, v, color_id = base_color
                # 寻找接近互补色的颜色（色相差约180°）
                complement_h = (h + 0.5) % 1.0
                best_complement = None
                min_diff = 0.2  # 最大可接受差异
                
                for n, c, ch, cs, cv, cid in colors_with_hsv:
                    if (n, c, ch, cs, cv, cid) == base_color:
                        continue  # 跳过基础颜色自身
                    
                    diff = min(abs(ch - complement_h), 1.0 - abs(ch - complement_h))
                    if diff < min_diff:
                        min_diff = diff
                        best_complement = (n, c, ch, cs, cv, cid)
                
                if best_complement:
                    # 提取基础信息
                    b_name, b_color, _, _, _, b_id = base_color
                    c_name, c_color, _, _, _, c_id = best_complement
                    
                    selected_colors = [(b_name, b_color, b_id), (c_name, c_color, c_id)]
                    title = "互补色配色"
        
        elif num_colors == 3:
            # 分割互补色（Split Complementary）
            # 一个基础颜色和两个与其互补色相邻的颜色（互补色两侧各30°）
            if colors_with_hsv:
                # 选择饱和度和亮度适中的颜色作为基础色
                sorted_by_sv = sorted(colors_with_hsv, key=lambda x: abs(x[3]-0.7) + abs(x[4]-0.7))
                base_color = sorted_by_sv[0]
                base_h = base_color[2]
                
                # 计算分割互补色的理想色相（互补色两侧各30°）
                complement_h = (base_h + 0.5) % 1.0
                split1_h = (complement_h - 0.08) % 1.0  # 约30°
                split2_h = (complement_h + 0.08) % 1.0  # 约30°
                
                # 寻找最接近这些色相的颜色
                color1 = find_closest_color_by_hue(colors_with_hsv, split1_h)
                color2 = find_closest_color_by_hue(colors_with_hsv, split2_h)
                
                if color1 and color2:
                    # 提取基础信息
                    b_name, b_color, _, _, _, b_id = base_color
                    c1_name, c1_color, _, _, _, c1_id = color1
                    c2_name, c2_color, _, _, _, c2_id = color2
                    
                    selected_colors = [(b_name, b_color, b_id), (c1_name, c1_color, c1_id), (c2_name, c2_color, c2_id)]
                    title = "分割互补色配色"
        
        # 如果上面的特定配色方案没有生效，使用原来的均匀分布方法
        if not selected_colors:
            # 原有的均匀分布逻辑
            # 按色相排序
            sorted_colors = sorted(colors_with_hsv, key=lambda x: x[2])
            
            # 尝试选择色相均匀分布的颜色
            if len(sorted_colors) >= num_colors:
                step = len(sorted_colors) / num_colors
                selected_colors = []
                for i in range(num_colors):
                    idx = int(i * step)
                    name, color, _, _, _, color_id = sorted_colors[idx]
                    selected_colors.append((name, color, color_id))
            else:
                # 如果颜色不够，就全部选择
                selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in sorted_colors]
            
            title = "相对色色板 (色相均匀分布)"
    
    elif palette_type == "brightness":
        # 按亮度排序（从深到浅）
        sorted_colors = sorted(colors_with_hsv, key=lambda x: x[4])  # 按V值排序
        
        # 选择指定数量的颜色
        if len(sorted_colors) >= num_colors:
            step = len(sorted_colors) / num_colors
            selected_colors = []
            for i in range(num_colors):
                idx = int(i * step)
                name, color, _, _, _, color_id = sorted_colors[idx]
                selected_colors.append((name, color, color_id))
        else:
            # 如果颜色不够，就全部选择
            selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in sorted_colors]
        
        title = "从深到浅的颜色色板"
    
    elif palette_type == "similar":
        # 按照饱和度选择相似色
        sorted_colors = sorted(colors_with_hsv, key=lambda x: x[3], reverse=True)  # 按S值排序
        
        # 选择指定数量的颜色
        if len(sorted_colors) >= num_colors:
            step = len(sorted_colors) / num_colors
            selected_colors = []
            for i in range(num_colors):
                idx = int(i * step)
                name, color, _, _, _, color_id = sorted_colors[idx]
                selected_colors.append((name, color, color_id))
        else:
            # 如果颜色不够，就全部选择
            selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in sorted_colors]
        
        title = "相似色色板 (饱和度变化)"
    
    elif palette_type == "triadic":
        # 三元配色（色环上相距120°的三种颜色）
        base_colors = []
        if colors_with_hsv:
            # 找出饱和度和明度适中的颜色作为基础色
            sorted_by_sv = sorted(colors_with_hsv, key=lambda x: abs(x[3]-0.7) + abs(x[4]-0.7))
            base_color = sorted_by_sv[0]
            base_h = base_color[2]
            
            # 计算另外两个三元色的理想色相
            h1 = (base_h + 1/3) % 1.0
            h2 = (base_h + 2/3) % 1.0
            
            # 寻找最接近这些色相的颜色
            color1 = find_closest_color_by_hue(colors_with_hsv, h1)
            color2 = find_closest_color_by_hue(colors_with_hsv, h2)
            
            if color1 and color2:
                base_colors = [base_color, color1, color2]
        
        # 提取需要的信息
        if base_colors:
            selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in base_colors]
            title = "三元配色"
        else:
            # 如果找不到三元色，退回到均匀分布
            sorted_colors = sorted(colors_with_hsv, key=lambda x: x[2])
            if len(sorted_colors) >= 3:
                step = len(sorted_colors) / 3
                selected_colors = []
                for i in range(3):
                    idx = int(i * step)
                    name, color, _, _, _, color_id = sorted_colors[idx]
                    selected_colors.append((name, color, color_id))
            else:
                selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in sorted_colors]
            title = "三元配色 (近似)"
    
    elif palette_type == "tetradic":
        # 四色配色（两对互补色，成矩形）
        base_colors = []
        if colors_with_hsv:
            # 选择基础色
            sorted_by_sv = sorted(colors_with_hsv, key=lambda x: abs(x[3]-0.7) + abs(x[4]-0.7))
            base_color = sorted_by_sv[0]
            base_h = base_color[2]
            
            # 计算其他三个角的色相
            h1 = (base_h + 0.25) % 1.0  # 90°
            h2 = (base_h + 0.5) % 1.0   # 180°
            h3 = (base_h + 0.75) % 1.0  # 270°
            
            # 寻找最接近这些色相的颜色
            color1 = find_closest_color_by_hue(colors_with_hsv, h1)
            color2 = find_closest_color_by_hue(colors_with_hsv, h2)
            color3 = find_closest_color_by_hue(colors_with_hsv, h3)
            
            if color1 and color2 and color3:
                base_colors = [base_color, color1, color2, color3]
        
        # 提取需要的信息
        if base_colors:
            selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in base_colors]
            title = "四方配色"
        else:
            # 退回到均匀分布
            sorted_colors = sorted(colors_with_hsv, key=lambda x: x[2])
            if len(sorted_colors) >= 4:
                step = len(sorted_colors) / 4
                selected_colors = []
                for i in range(4):
                    idx = int(i * step)
                    name, color, _, _, _, color_id = sorted_colors[idx]
                    selected_colors.append((name, color, color_id))
            else:
                selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in sorted_colors]
            title = "四方配色 (近似)"
    
    elif palette_type == "analogous":
        # 相邻色配色（色环上相邻的颜色）
        if colors_with_hsv:
            # 选择基础色
            sorted_by_sv = sorted(colors_with_hsv, key=lambda x: abs(x[3]-0.7) + abs(x[4]-0.7))
            base_color = sorted_by_sv[0]
            base_h = base_color[2]
            
            # 相邻色通常在色相环上相距30°左右
            analogous_colors = [base_color]
            
            # 计算基础色两侧的色相
            for i in range(1, (num_colors + 1) // 2):
                offset = i * 0.08  # 约30°
                h1 = (base_h - offset) % 1.0
                h2 = (base_h + offset) % 1.0
                
                color1 = find_closest_color_by_hue(colors_with_hsv, h1)
                color2 = find_closest_color_by_hue(colors_with_hsv, h2)
                
                if color1:
                    analogous_colors.append(color1)
                if color2 and len(analogous_colors) < num_colors:
                    analogous_colors.append(color2)
            
            selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in analogous_colors[:num_colors]]
            title = "相邻色配色"
        else:
            title = "相邻色配色 (近似)"
    
    elif palette_type == "monochromatic":
        # 单色配色（相同色相，不同饱和度和亮度）
        if colors_with_hsv:
            # 选择基础色
            sorted_by_s = sorted(colors_with_hsv, key=lambda x: x[3], reverse=True)
            base_color = sorted_by_s[0]
            base_h = base_color[2]
            
            # 寻找色相相似的颜色
            similar_hue_colors = []
            for color_info in colors_with_hsv:
                h = color_info[2]
                diff = min(abs(h - base_h), 1.0 - abs(h - base_h))
                if diff < 0.05:  # 色相差异在18°内
                    similar_hue_colors.append(color_info)
            
            # 按亮度排序
            similar_hue_colors.sort(key=lambda x: x[4])
            
            # 选择num_colors个分布均匀的颜色
            if similar_hue_colors:
                if len(similar_hue_colors) >= num_colors:
                    step = len(similar_hue_colors) / num_colors
                    monochromatic_colors = []
                    for i in range(num_colors):
                        idx = int(i * step)
                        monochromatic_colors.append(similar_hue_colors[idx])
                else:
                    monochromatic_colors = similar_hue_colors
                
                selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in monochromatic_colors]
                title = "单色配色"
            else:
                title = "单色配色 (近似)"
    
    elif palette_type == "split-complementary":
        # 分割互补色（一个基础色和两个互补色两侧的颜色）
        if num_colors >= 3 and colors_with_hsv:
            # 本质上与三色配色相同，但基于互补色原理
            # 选择基础色
            sorted_by_sv = sorted(colors_with_hsv, key=lambda x: abs(x[3]-0.7) + abs(x[4]-0.7))
            base_color = sorted_by_sv[0]
            base_h = base_color[2]
            
            # 计算互补色
            complement_h = (base_h + 0.5) % 1.0
            
            # 计算互补色两侧的色相（通常相距30°）
            split1_h = (complement_h - 0.08) % 1.0  # 约30°
            split2_h = (complement_h + 0.08) % 1.0  # 约30°
            
            # 寻找最接近这些色相的颜色
            color1 = find_closest_color_by_hue(colors_with_hsv, split1_h)
            color2 = find_closest_color_by_hue(colors_with_hsv, split2_h)
            
            if color1 and color2:
                selected_colors = [
                    (base_color[0], base_color[1], base_color[5]),
                    (color1[0], color1[1], color1[5]),
                    (color2[0], color2[1], color2[5])
                ]
                title = "分割互补色配色"
            else:
                title = "分割互补色配色 (近似)"
    
    # 如果没有选出颜色，使用默认均匀分布
    if not selected_colors:
        # 按色相排序
        sorted_colors = sorted(colors_with_hsv, key=lambda x: x[2])
        
        # 尝试选择色相均匀分布的颜色
        if len(sorted_colors) >= num_colors:
            step = len(sorted_colors) / num_colors
            selected_colors = []
            for i in range(num_colors):
                idx = int(i * step)
                name, color, _, _, _, color_id = sorted_colors[idx]
                selected_colors.append((name, color, color_id))
        else:
            # 如果颜色不够，就全部选择
            selected_colors = [(name, color, color_id) for name, color, _, _, _, color_id in sorted_colors]
        
        # 如果title还没有设置，添加一个默认标题
        if 'title' not in locals():
            title = f"{palette_type}色板 (近似)"
    
    return selected_colors, title

def display_color_palette(colors, title="色板", show_usage_examples=True):
    """显示色板"""
    if not colors:
        print("警告: 没有颜色可显示")
        fig, ax = plt.subplots(figsize=(12, 2))
        ax.text(0.5, 0.5, "没有找到颜色", ha='center', va='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title)
        ax.axis('off')
        plt.tight_layout()
        return fig
    
    # 计算图表高度 - 如果需要显示用例示例且有足够的颜色，添加额外空间
    has_examples = show_usage_examples and len(colors) >= 2
    height_ratio = 3 if has_examples else 1
    fig_height = 6 if has_examples else 4
    
    if has_examples:
        fig, axs = plt.subplots(height_ratio, 1, figsize=(12, fig_height), 
                              gridspec_kw={'height_ratios': [2, 1, 1]})
        ax_palette = axs[0]
    else:
        fig, ax_palette = plt.subplots(figsize=(12, fig_height))
        axs = [ax_palette]
    
    # 显示色板颜色
    n_colors = len(colors)
    height = 1.0 / n_colors
    
    # 显示色板颜色
    for i, (name, color, color_id) in enumerate(colors):
        y = i * height
        rect = patches.Rectangle((0, y), 1, height, color=color)
        ax_palette.add_patch(rect)
        
        # 计算文本颜色（深色背景用白色文本，浅色背景用黑色文本）
        text_color = 'white' if sum(color[:3]) < 1.5 else 'black'
        
        # 显示颜色信息
        rgb_values = [int(c * 255) for c in color[:3]]
        rgb_hex = '#{:02x}{:02x}{:02x}'.format(*rgb_values)
        
        h, s, v = rgb_to_hsv(color[:3])
        hsv_values = f"H:{h:.0f}° S:{s*100:.0f}% V:{v*100:.0f}%"
        
        label = f"{name}\nRGB: {rgb_values}\nHEX: {rgb_hex}\nHSV: {hsv_values}"
        ax_palette.text(0.5, y + height/2, label, 
                ha='center', va='center', color=text_color,
                fontsize=10)
    
    ax_palette.set_xlim(0, 1)
    ax_palette.set_ylim(0, 1)
    ax_palette.set_title(title)
    ax_palette.axis('off')
    
    # 添加使用示例
    if has_examples:
        # 示例1: 展示文本与背景配色
        ax1 = axs[1]
        ax1.set_title("文本与背景配色示例", fontsize=12)
        ax1.axis('off')
        
        n_examples = min(len(colors), 4)  # 最多显示4个示例
        width = 1.0 / n_examples
        
        for i in range(n_examples):
            # 选择颜色
            bg_color = colors[i][1]
            
            # 找出对比色作为文本颜色
            contrasting_idx = (i + len(colors) // 2) % len(colors)
            text_color = colors[contrasting_idx][1]
            
            # 绘制背景矩形
            rect = patches.Rectangle((i * width, 0), width, 1, color=bg_color)
            ax1.add_patch(rect)
            
            # 显示示例文本
            rgb_hex = '#{:02x}{:02x}{:02x}'.format(*[int(c * 255) for c in bg_color[:3]])
            ax1.text(i * width + width/2, 0.5, 
                    f"示例文本\n{rgb_hex}", 
                    ha='center', va='center', 
                    color=text_color, fontsize=10)
        
        # 示例2: 展示渐变或图表配色
        ax2 = axs[2]
        ax2.set_title("图表配色示例", fontsize=12)
        
        # 创建简单条形图
        x = np.arange(len(colors))
        heights = np.linspace(0.3, 1.0, len(colors))  # 渐变高度
        bar_colors = [c[1] for c in colors]
        
        ax2.bar(x, heights, color=bar_colors, width=0.7)
        ax2.set_xticks(x)
        ax2.set_xticklabels([f"数据{i+1}" for i in range(len(colors))], fontsize=8)
        ax2.set_ylim(0, 1.1)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig

def print_available_colors():
    """打印可用的颜色"""
    # 加载所有颜色
    if Path(colors_file).exists():
        all_colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    else:
        # 如果颜色文件不存在，使用默认颜色
        all_colors = {}
        for name, color in BASIC_COLOR_NAMES.items():
            color_id = generate_color_id(color)
            all_colors[color_id] = {
                "color": color,
                "name": name
            }
    
    # 打印默认颜色信息
    print("\n=== 基础颜色 ===")
    for name in sorted(BASIC_COLOR_NAMES.keys()):
        color = BASIC_COLOR_NAMES[name]
        rgb = [int(c * 255) for c in color[:3]]
        print(f"{name:<15}: RGB={rgb}")
    
    # 对颜色进行分组
    color_families = {}
    for color_id, info in all_colors.items():
        name = info["name"]
        color = info["color"]
        
        # 找到基础颜色名称
        base_name = name.split("_")[0] if "_" in name else name
        
        if base_name not in color_families:
            color_families[base_name] = []
        
        color_families[base_name].append((name, color, color_id))
    
    # 如果找到了额外的颜色
    if len(color_families) > len(BASIC_COLOR_NAMES):
        print("\n=== 颜色库中的其他颜色系列 ===")
        for family, colors in sorted(color_families.items()):
            if family not in BASIC_COLOR_NAMES:
                print(f"{family}: {len(colors)} 种变体")
    
    print("\n使用方法示例:")
    print("  python color_palette_generator.py --family blue --type brightness --num 6")
    print("  python color_palette_generator.py --type complementary --num 8")
    print("  python color_palette_generator.py --family red --output my_red_palette.png")

def main():
    parser = argparse.ArgumentParser(description="颜色色板生成器 - 从现有颜色库中选择颜色")
    parser.add_argument("--family", help="颜色系列名称 (例如: red, blue, green)")
    parser.add_argument("--num", type=int, default=5, help="色板中要包含的颜色数量 (默认: 5)")
    parser.add_argument("--type", choices=["complementary", "brightness", "similar", 
                         "triadic", "tetradic", "analogous", "monochromatic", "split-complementary"], 
                         default="complementary", 
                         help="色板类型: 互补色(complementary), 明暗(brightness), 相似色(similar), 三元色(triadic)...")
    parser.add_argument("--output", help="输出文件名 (默认: 根据色板类型自动生成)")
    parser.add_argument("--show", action="store_true", help="显示色板窗口")
    parser.add_argument("--list", action="store_true", help="列出所有可用的颜色系列")
    parser.add_argument("--examples", action="store_true", help="显示色板使用示例")
    
    args = parser.parse_args()
    
    # 如果指定了--list参数，只显示颜色列表
    if args.list:
        print_available_colors()
        return 0
    
    try:
        # 从颜色库中获取颜色
        selected_colors, title = get_colors_from_library(
            family=args.family,
            num_colors=args.num,
            palette_type=args.type
        )
        
        # 显示色板
        fig = display_color_palette(selected_colors, title, show_usage_examples=args.examples)
        
        # 保存色板
        if args.output:
            output_path = args.output
            if not output_path.endswith(('.png', '.jpg', '.pdf')):
                output_path += '.png'
        else:
            family_tag = args.family or "all"
            output_path = output_dir / f"palette_{args.type}_{family_tag}.png"
        
        fig.savefig(output_path)
        print(f"色板已保存至: {output_path}")
        
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
    # 如果没有参数，显示帮助信息
    if len(sys.argv) == 1:
        print("\n色板生成器 - 从颜色库中选择颜色组成色板")
        print("\n支持的色板类型:")
        print("  - complementary:       互补色（色环上相对的颜色）")
        print("  - brightness:          从深到浅的颜色")
        print("  - similar:             相似色（饱和度变化）")
        print("  - triadic:             三元色（色环上等距的三种颜色）")
        print("  - tetradic:            四方配色（两对互补色）")
        print("  - analogous:           相邻色（色环上相邻的颜色）")
        print("  - monochromatic:       单色配色（相同色相，不同饱和度和亮度）")
        print("  - split-complementary: 分割互补色（一个基础色和两个互补色两侧的颜色）")
        print("\n用法示例:")
        print("  python color_palette_generator.py --type triadic --num 3")
        print("  python color_palette_generator.py --family blue --type monochromatic --num 5")
        print("  python color_palette_generator.py --type tetradic --examples --show")
        print("\n使用 --list 参数查看所有可用的颜色")
        print("使用 --examples 参数显示色板使用示例")
        print("使用 -h 或 --help 参数查看完整帮助信息\n")
    
    sys.exit(main()) 