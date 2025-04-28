"""
Scientific Visualization Tools for Working with Color
"""

__version__ = "0.1.0"

from .colors import (
    get_color,
    load_colors,
    save_colors,
    add_color,
    DEFAULT_COLORS,
    Color,
    ColorRGB,
    ColorRGBA,
    ColorDict,
    generate_color_id,
    extract_dominant_colors,
    add_colors_from_image,
    get_color_by_id,
    find_similar_colors,
    find_complementary_colors,
    find_similar_colors_by_brightness,
    generate_color_name,
    rgb_to_hsv,
    find_nearest_basic_color,
    BASIC_COLOR_NAMES,
    COLOR_MODIFIERS
) 