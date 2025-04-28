"""
颜色配置模块 - 存储所有图表元素使用的颜色配置
"""
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.colors as mcolors
import os.path

# 网格样式颜色
GRID_COLORS = {
    'default': '#dddddd',
    'dashed': '#cccccc',
    'dotted': '#888888',
    'subtle': '#eeeeee',
}

# 通用颜色
COMMON_COLORS = {
    'white': 'white',
    'gray': 'gray',
    'black': 'black',
}

# 特殊颜色
SPECIAL_COLORS = {
    'info_background': '#e5f5fd',
    'info_border': '#a8d7fd',
}

# 从图片提取的颜色组
COLOR_PALETTES_FROM_IMAGES = {}

# 导出所有颜色配置，统一管理
def get_grid_color(style):
    """获取指定样式的网格颜色"""
    return GRID_COLORS.get(style, GRID_COLORS['default'])

def get_common_color(name):
    """获取通用颜色"""
    return COMMON_COLORS.get(name, COMMON_COLORS['white'])

def get_special_color(name):
    """获取特殊颜色"""
    return SPECIAL_COLORS.get(name, None)

def extract_colors_from_image(image_path, color_count=5, palette_name=None, exclude_white=True):
    """
    从图片中提取指定数量的主要颜色，并可选地将其保存为命名调色板
    
    参数:
        image_path: 图片文件路径
        color_count: 要提取的颜色数量，默认为5
        palette_name: 保存调色板的名称，如果为None则不保存
        exclude_white: 是否排除白色（和接近白色的颜色），默认为True
    
    返回:
        提取的颜色列表，格式为十六进制颜色代码
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件 '{image_path}' 不存在")
    
    # 读取图片
    img = Image.open(image_path)
    
    # 调整图片大小以加快处理速度
    img.thumbnail((200, 200))
    
    # 将图片转换为像素数组
    pixels = np.array(img.convert('RGB')).reshape(-1, 3)
    
    # 如果需要排除白色
    if exclude_white:
        # 计算像素亮度，排除亮度过高的像素（白色或接近白色）
        brightness = np.sqrt(0.299 * pixels[:, 0]**2 + 0.587 * pixels[:, 1]**2 + 0.114 * pixels[:, 2]**2)
        pixels = pixels[brightness < 240]  # 排除亮度过高的像素
    
    # 确保有足够的像素进行聚类
    if len(pixels) < color_count:
        raise ValueError("图片中没有足够的非白色像素来提取指定数量的颜色")
    
    # 使用K-means聚类算法提取主要颜色
    kmeans = KMeans(n_clusters=color_count, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # 获取聚类中心（主要颜色）
    colors = kmeans.cluster_centers_.astype(int)
    
    # 将RGB颜色转换为十六进制颜色代码
    hex_colors = []
    for color in colors:
        hex_color = mcolors.to_hex([color[0]/255, color[1]/255, color[2]/255])
        hex_colors.append(hex_color)
    
    # 如果指定了调色板名称，则保存调色板
    if palette_name:
        COLOR_PALETTES_FROM_IMAGES[palette_name] = hex_colors
    
    return hex_colors

def get_image_palette(name):
    """
    获取从图片提取的颜色调色板
    
    参数:
        name: 调色板名称
    
    返回:
        调色板颜色列表，如果调色板不存在则返回None
    """
    return COLOR_PALETTES_FROM_IMAGES.get(name, None)

def list_image_palettes():
    """
    列出所有从图片提取的调色板名称
    
    返回:
        调色板名称列表
    """
    return list(COLOR_PALETTES_FROM_IMAGES.keys()) 