"""
Color definitions and utilities for scientific visualization.
"""
import json
import os
import math
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional, Any
import numpy as np
from PIL import Image
from collections import Counter

# Type definition for colors
ColorRGB = Tuple[float, float, float]
ColorRGBA = Tuple[float, float, float, float]
Color = Union[ColorRGB, ColorRGBA]
ColorDict = Dict[str, Color]
ColorInfoDict = Dict[str, Dict[str, Any]]
ColorIdDict = Dict[str, Dict[str, Any]]  # ID -> {color, name}

# Predefined color names for color naming algorithm
# Contains common color names with their RGB values
BASIC_COLOR_NAMES = {
    "red": (1.0, 0.0, 0.0),
    "orange": (1.0, 0.5, 0.0),
    "yellow": (1.0, 1.0, 0.0),
    "chartreuse": (0.5, 1.0, 0.0),
    "green": (0.0, 1.0, 0.0),
    "spring_green": (0.0, 1.0, 0.5),
    "cyan": (0.0, 1.0, 1.0),
    "azure": (0.0, 0.5, 1.0),
    "blue": (0.0, 0.0, 1.0),
    "violet": (0.5, 0.0, 1.0),
    "magenta": (1.0, 0.0, 1.0),
    "rose": (1.0, 0.0, 0.5),
    "black": (0.0, 0.0, 0.0),
    "dark_gray": (0.25, 0.25, 0.25),
    "gray": (0.5, 0.5, 0.5),
    "light_gray": (0.75, 0.75, 0.75),
    "white": (1.0, 1.0, 1.0),
    "brown": (0.6, 0.3, 0.1),
    "olive": (0.5, 0.5, 0.0),
    "teal": (0.0, 0.5, 0.5),
    "navy": (0.0, 0.0, 0.5),
    "purple": (0.5, 0.0, 0.5),
    "maroon": (0.5, 0.0, 0.0),
    "gold": (1.0, 0.84, 0.0),
    "silver": (0.75, 0.75, 0.75),
    "pink": (1.0, 0.75, 0.8),
    "sky_blue": (0.53, 0.81, 0.92),
    "coral": (1.0, 0.5, 0.31),
    "turquoise": (0.25, 0.88, 0.82),
    "lavender": (0.9, 0.9, 0.98),
    "tan": (0.82, 0.71, 0.55),
    "beige": (0.96, 0.96, 0.86),
    "mint": (0.6, 1.0, 0.6),
    "indigo": (0.29, 0.0, 0.51),
    "salmon": (0.98, 0.5, 0.45),
}

# Modifiers for naming algorithm
COLOR_MODIFIERS = {
    # Intensity modifiers
    "very_light": 0.75,  # High brightness
    "light": 0.6,        # Above-medium brightness
    "medium": 0.45,      # Medium brightness
    "dark": 0.3,         # Below-medium brightness
    "very_dark": 0.15,   # Low brightness
    
    # Saturation modifiers
    "vivid": 0.85,      # High saturation
    "bright": 0.7,      # Above-medium saturation
    "muted": 0.4,       # Below-medium saturation
    "dull": 0.25,       # Low saturation
    "grayish": 0.1,     # Very low saturation
}

# Load default colors from file
def _load_default_colors() -> ColorDict:
    """Load default colors from the bundled JSON file."""
    # Find the path to the default_colors.json file
    current_dir = Path(__file__).parent
    default_colors_path = current_dir / "default_colors.json"
    
    try:
        with open(default_colors_path, 'r') as f:
            colors_data = json.load(f)
            
        # Convert the data format if needed
        if colors_data and isinstance(next(iter(colors_data.values())), list):
            # Old format: name -> [r, g, b]
            return {k: tuple(v) for k, v in colors_data.items()}
        else:
            # Format with IDs: could be name->{"color":[r,g,b], "id":...} or id->{"color":[r,g,b], "name":...}
            result = {}
            for key, value in colors_data.items():
                if "color" in value:
                    if isinstance(value["color"], list):
                        if "name" in value:
                            # ID is the key, name is in the value
                            name = value["name"]
                            color = tuple(value["color"])
                            result[name] = color
                        else:
                            # Name is the key, ID is in the value
                            result[key] = tuple(value["color"])
            return result
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to hardcoded default colors if file is not found
        return {k: v for k, v in BASIC_COLOR_NAMES.items() if k in [
            "blue", "red", "green", "yellow", "cyan", "magenta", 
            "white", "black", "gray", "orange", "purple", "brown"
        ]}

# Default colors loaded from file
DEFAULT_COLORS = _load_default_colors()


def save_colors(colors: Union[ColorDict, ColorInfoDict, ColorIdDict], filename: str, use_id_as_key: bool = True) -> None:
    """
    Save a dictionary of colors to a JSON file.
    
    Args:
        colors: Dictionary of colors (can be in various formats)
        filename: Path to save the colors file
        use_id_as_key: Whether to use color ID as the key in the output JSON
    """
    # Create directory if it doesn't exist
    file_path = Path(filename)
    os.makedirs(file_path.parent, exist_ok=True)
    
    # Convert to the format with IDs as keys
    serializable_colors = {}
    
    if use_id_as_key:
        # Output format: color_id -> {color: [r,g,b], name: "..."}
        for key, value in colors.items():
            if isinstance(value, tuple):
                # Simple color tuple with name as key
                color_tuple = value
                color_id = generate_color_id(color_tuple)
                serializable_colors[color_id] = {
                    "color": list(color_tuple),
                    "name": key
                }
            elif isinstance(value, dict):
                if "color" in value and "id" in value:
                    # Name is key, ID is in value
                    color_id = value["id"]
                    serializable_colors[color_id] = {
                        "color": list(value["color"]) if isinstance(value["color"], tuple) else value["color"],
                        "name": key
                    }
                elif "color" in value and "name" in value:
                    # ID is key, name is in value
                    serializable_colors[key] = {
                        "color": list(value["color"]) if isinstance(value["color"], tuple) else value["color"],
                        "name": value["name"]
                    }
    else:
        # Output format: color_name -> {color: [r,g,b], id: "..."}
        for key, value in colors.items():
            if isinstance(value, tuple):
                # Simple color tuple
                color_tuple = value
                color_id = generate_color_id(color_tuple)
                serializable_colors[key] = {
                    "color": list(color_tuple),
                    "id": color_id
                }
            elif isinstance(value, dict):
                if "color" in value and "name" in value:
                    # ID is key, name is in value
                    name = value["name"]
                    color_id = key
                    serializable_colors[name] = {
                        "color": list(value["color"]) if isinstance(value["color"], tuple) else value["color"],
                        "id": color_id
                    }
                elif "color" in value and "id" in value:
                    # Name is key, ID is in value
                    serializable_colors[key] = {
                        "color": list(value["color"]) if isinstance(value["color"], tuple) else value["color"],
                        "id": value["id"]
                    }
    
    with open(filename, 'w') as f:
        json.dump(serializable_colors, f, indent=2)


def load_colors(filename: str, include_meta: bool = False, use_id_as_key: bool = True) -> Union[ColorDict, ColorInfoDict, ColorIdDict]:
    """
    Load colors from a JSON file.
    
    Args:
        filename: Path to the colors file
        include_meta: Whether to include metadata (name/id) in the returned dictionary
        use_id_as_key: Whether to use color ID as the key in the returned dictionary
        
    Returns:
        Dictionary of colors in the requested format
    """
    try:
        with open(filename, 'r') as f:
            loaded_data = json.load(f)
        
        result = {}
        
        for key, value in loaded_data.items():
            # Determine if the key is an ID or a name
            is_key_id = len(key) >= 12 and all(c in "0123456789abcdef" for c in key)
            
            if isinstance(value, list):
                # Old format: name -> [r, g, b]
                color_tuple = tuple(value)
                color_id = generate_color_id(color_tuple)
                name = key
                
                if include_meta:
                    if use_id_as_key:
                        result[color_id] = {"color": color_tuple, "name": name}
                    else:
                        result[name] = {"color": color_tuple, "id": color_id}
                else:
                    if use_id_as_key:
                        # For simple color dict, we can't use ID as key without metadata
                        result[name] = color_tuple
                    else:
                        result[name] = color_tuple
                        
            elif isinstance(value, dict) and "color" in value:
                color_tuple = tuple(value["color"])
                
                if "id" in value and "name" not in value:
                    # Name is key, ID is in value
                    name = key
                    color_id = value["id"]
                elif "name" in value and "id" not in value:
                    # ID is key, name is in value
                    color_id = key
                    name = value["name"]
                elif is_key_id:
                    # Best guess: key is ID
                    color_id = key
                    name = value.get("name", f"color_{key[:6]}")
                else:
                    # Best guess: key is name
                    name = key
                    color_id = value.get("id", generate_color_id(color_tuple))
                
                if include_meta:
                    if use_id_as_key:
                        result[color_id] = {"color": color_tuple, "name": name}
                    else:
                        result[name] = {"color": color_tuple, "id": color_id}
                else:
                    if use_id_as_key:
                        # For simple color dict, we can't use ID as key without metadata
                        result[name] = color_tuple
                    else:
                        result[name] = color_tuple
        
        return result
        
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: Could not load colors from {filename}. Using default colors.")
        
        # Create result based on DEFAULT_COLORS
        result = {}
        
        for name, color in DEFAULT_COLORS.items():
            color_id = generate_color_id(color)
            
            if include_meta:
                if use_id_as_key:
                    result[color_id] = {"color": color, "name": name}
                else:
                    result[name] = {"color": color, "id": color_id}
            else:
                if use_id_as_key:
                    # For simple color dict, we can't use ID as key without metadata
                    result[name] = color
                else:
                    result[name] = color
        
        return result


def get_color(name_or_id: str, colors_file: Optional[str] = None) -> Color:
    """
    Get a color by name or ID from the colors file or default colors.
    
    Args:
        name_or_id: Name or ID of the color to retrieve
        colors_file: Optional path to a colors file
        
    Returns:
        The color as an RGB or RGBA tuple
        
    Raises:
        KeyError: If the color is not found
    """
    if colors_file:
        # Try loading with ID as key first (with metadata)
        colors_by_id = load_colors(colors_file, include_meta=True, use_id_as_key=True)
        
        # Check if it's a direct ID match
        if name_or_id in colors_by_id:
            return colors_by_id[name_or_id]["color"]
        
        # Try looking by name
        for color_id, info in colors_by_id.items():
            if info["name"] == name_or_id:
                return info["color"]
        
        # If still not found, try loading with name as key (for backwards compatibility)
        colors_by_name = load_colors(colors_file, include_meta=False, use_id_as_key=False)
        if name_or_id in colors_by_name:
            return colors_by_name[name_or_id]
    else:
        # Just check default colors
        if name_or_id in DEFAULT_COLORS:
            return DEFAULT_COLORS[name_or_id]
        
        # Try matching against IDs of default colors
        for name, color in DEFAULT_COLORS.items():
            if generate_color_id(color) == name_or_id:
                return color
    
    raise KeyError(f"Color '{name_or_id}' not found")


def add_color(name: str, color: Color, colors_file: str) -> str:
    """
    Add or update a color in the colors file.
    
    Args:
        name: Name of the color to add
        color: RGB or RGBA tuple for the color
        colors_file: Path to the colors file
        
    Returns:
        The ID of the added color
    """
    # Generate ID for the color
    color_id = generate_color_id(color)
    
    # Load existing colors with metadata
    colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    
    # Add or update the color
    colors[color_id] = {
        "color": color,
        "name": name
    }
    
    # Save updated colors
    save_colors(colors, colors_file, use_id_as_key=True)
    
    return color_id


def generate_color_id(color: Color) -> str:
    """
    Generate a unique ID for a color that reflects color similarity.
    
    The ID is constructed as a hexadecimal string:
    - First 6 characters: RGB hex code
    - Next 2 characters: Hue quantized to 256 values
    - Next 2 characters: Saturation quantized to 256 values
    - Next 2 characters: Value/Brightness quantized to 256 values
    
    Args:
        color: RGB or RGBA color tuple
        
    Returns:
        A string ID that reflects color properties
    """
    r, g, b = color[:3]
    
    # RGB hex part
    hex_part = f"{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    # Convert RGB to HSV
    r, g, b = [x * 255 for x in color[:3]]
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val
    
    # Hue calculation
    if delta == 0:
        h = 0
    elif max_val == r:
        h = ((g - b) / delta) % 6
    elif max_val == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4
    
    h = int((h * 60) % 360)
    
    # Saturation calculation
    s = 0 if max_val == 0 else delta / max_val
    
    # Value calculation
    v = max_val / 255
    
    # Quantize HSV to 256 values each (00-FF)
    h_hex = f"{int(h * 255 / 360):02x}"
    s_hex = f"{int(s * 255):02x}"
    v_hex = f"{int(v * 255):02x}"
    
    # Combine to form the ID
    color_id = f"{hex_part}{h_hex}{s_hex}{v_hex}"
    
    return color_id


def rgb_to_hsv(color: Color) -> Tuple[float, float, float]:
    """Convert RGB color to HSV color space."""
    r, g, b = color[:3]
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    delta = max_val - min_val
    
    # Value calculation
    v = max_val
    
    # Saturation calculation
    s = 0 if max_val == 0 else delta / max_val
    
    # Hue calculation
    if delta == 0:
        h = 0
    elif max_val == r:
        h = ((g - b) / delta) % 6
    elif max_val == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4
    
    h = (h * 60) % 360
    
    return h, s, v


def find_nearest_basic_color(color: Color) -> Tuple[str, float]:
    """
    Find the nearest basic color name for a given color.
    
    Args:
        color: RGB or RGBA tuple
        
    Returns:
        Tuple of (color_name, distance)
    """
    r, g, b = color[:3]
    
    min_distance = float('inf')
    nearest_name = None
    
    for name, (r2, g2, b2) in BASIC_COLOR_NAMES.items():
        # Calculate Euclidean distance in RGB space
        distance = math.sqrt((r - r2)**2 + (g - g2)**2 + (b - b2)**2)
        
        if distance < min_distance:
            min_distance = distance
            nearest_name = name
    
    return nearest_name, min_distance


def generate_color_name(color: Color, source_name: str = "", count: int = 0) -> str:
    """
    Generate a descriptive name for a color based on its properties.
    
    Args:
        color: RGB or RGBA color tuple
        source_name: Optional source name or file name for context
        count: Optional count for disambiguation
        
    Returns:
        A descriptive color name
    """
    # Convert to HSV for better color naming
    h, s, v = rgb_to_hsv(color)
    
    # Find the nearest basic color
    basic_name, distance = find_nearest_basic_color(color)
    
    # Determine modifiers based on HSV values
    intensity_modifier = ""
    saturation_modifier = ""
    
    # Intensity modifier based on V (brightness)
    if v > 0.85:
        intensity_modifier = "very_light"
    elif v > 0.65:
        intensity_modifier = "light"
    elif v < 0.15:
        intensity_modifier = "very_dark"
    elif v < 0.35:
        intensity_modifier = "dark"
    
    # Saturation modifier based on S
    if s > 0.85 and v > 0.5:
        saturation_modifier = "vivid"
    elif s > 0.65 and v > 0.4:
        saturation_modifier = "bright"
    elif s < 0.15:
        saturation_modifier = "grayish"
    elif s < 0.35:
        saturation_modifier = "muted"
    
    # Special cases
    if v < 0.15:  # Very dark colors tend to look black
        basic_name = "black"
        intensity_modifier = ""
        saturation_modifier = ""
    elif v > 0.95 and s < 0.05:  # Very light unsaturated colors look white
        basic_name = "white"
        intensity_modifier = ""
        saturation_modifier = ""
    elif s < 0.08:  # Very unsaturated colors look gray
        if v > 0.8:
            basic_name = "white"
            intensity_modifier = "off"
        elif v < 0.2:
            basic_name = "black"
            intensity_modifier = "off"
        else:
            basic_name = "gray"
            if v > 0.65:
                intensity_modifier = "light"
            elif v < 0.35:
                intensity_modifier = "dark"
            else:
                intensity_modifier = "medium"
        saturation_modifier = ""
    
    # Build the color name
    parts = []
    
    if intensity_modifier and saturation_modifier:
        # If we have both modifiers, only use the more significant one
        if s < 0.3 or s > 0.8:
            parts.append(saturation_modifier)
        else:
            parts.append(intensity_modifier)
    else:
        if intensity_modifier:
            parts.append(intensity_modifier)
        if saturation_modifier:
            parts.append(saturation_modifier)
    
    parts.append(basic_name)
    
    # Add context from source if available
    context = ""
    if source_name:
        # Extract meaningful context from the source name
        context_parts = source_name.split('-')
        if len(context_parts) > 1:
            context = context_parts[-1].lower()
            # Remove file extension if present
            context = context.split('.')[0]
            # Clean up the context
            context = ''.join(c for c in context if c.isalnum() or c == '_')
            if context and len(context) <= 15:  # Only use short contexts
                parts.append(f"from_{context}")
    
    # Join with underscores for a nice variable-friendly name
    name = "_".join(parts)
    
    # Add a number for disambiguation if needed
    if count > 0:
        name = f"{name}_{count}"
    
    return name


def extract_dominant_colors(image_path: str, n_colors: int = 5, exclude_white: bool = True, 
                           white_threshold: float = 0.9) -> List[Tuple[Color, int]]:
    """
    Extract the dominant colors from an image.
    
    Args:
        image_path: Path to the image file
        n_colors: Number of dominant colors to extract
        exclude_white: Whether to exclude white/near-white colors
        white_threshold: Threshold for considering a color as white (0-1)
        
    Returns:
        List of tuples containing (color, pixel_count)
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image to speed up processing if it's too large
        max_dimension = 300
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # Get pixel data
        pixels = np.array(img)
        pixels = pixels.reshape(-1, 3)
        
        # Convert to 0-1 range
        pixels = pixels / 255.0
        
        # Round colors to reduce the number of unique colors
        precision = 0.05  # Adjust this value to control color quantization
        pixels = np.round(pixels / precision) * precision
        
        # Convert pixels to tuples for counting
        pixel_tuples = [tuple(p) for p in pixels]
        
        # Count occurrences of each color
        color_counts = Counter(pixel_tuples)
        
        # Filter out white or near-white colors if requested
        if exclude_white:
            filtered_colors = []
            for color, count in color_counts.items():
                # Check if the color is white or near-white
                is_white = all(c >= white_threshold for c in color)
                if not is_white:
                    filtered_colors.append((color, count))
        else:
            filtered_colors = list(color_counts.items())
        
        # Sort by count (most frequent first) and take top n_colors
        dominant_colors = sorted(filtered_colors, key=lambda x: x[1], reverse=True)[:n_colors]
        
        return dominant_colors
    
    except Exception as e:
        print(f"Error extracting colors from image: {e}")
        return []


def add_colors_from_image(image_path: str, colors_file: str, n_colors: int = 5, 
                         prefix: str = "") -> Dict[str, str]:
    """
    Extract dominant colors from an image and add them to the colors file.
    
    Args:
        image_path: Path to the image file
        colors_file: Path to the colors file
        n_colors: Number of dominant colors to extract
        prefix: Optional prefix for the color names
        
    Returns:
        Dictionary mapping color names to their IDs
    """
    # Extract dominant colors
    dominant_colors = extract_dominant_colors(image_path, n_colors)
    
    if not dominant_colors:
        return {}
    
    # Extract source name from image path for context in color naming
    source_name = Path(image_path).stem
    
    # Load existing colors with metadata, using ID as key
    colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    
    # Add each dominant color with a unique name and ID
    color_names = {}  # Map of color IDs to names
    existing_names = set(info["name"] for info in colors.values())
    
    for i, (color, count) in enumerate(dominant_colors):
        # Generate a unique ID for the color
        color_id = generate_color_id(color)
        
        # Generate a descriptive name for the color
        base_name = generate_color_name(color, source_name)
        color_name = base_name
        
        # Ensure name is unique by adding numbers if needed
        counter = 1
        while color_name in existing_names:
            color_name = f"{base_name}_{counter}"
            counter += 1
        
        # Add prefix if provided
        if prefix:
            color_name = f"{prefix}_{color_name}"
            
        # Add to tracking sets
        existing_names.add(color_name)
        
        # Add to colors dictionary
        colors[color_id] = {
            "color": color,
            "name": color_name
        }
        
        # Store the name
        color_names[color_id] = color_name
    
    # Save updated colors
    save_colors(colors, colors_file, use_id_as_key=True)
    
    return color_names


def get_color_by_id(color_id: str, colors_file: str) -> Optional[Tuple[str, Color]]:
    """
    Find a color by its ID.
    
    Args:
        color_id: The color ID to search for
        colors_file: Path to the colors file
        
    Returns:
        Tuple of (color_name, color) if found, None otherwise
    """
    # Load colors with IDs as keys
    colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    
    # Look for exact match
    if color_id in colors:
        info = colors[color_id]
        return (info["name"], info["color"])
    
    # If no exact match, look for closest match by prefix (RGB part)
    rgb_prefix = color_id[:6]
    matches = []
    for id, info in colors.items():
        if id.startswith(rgb_prefix):
            matches.append((info["name"], info["color"]))
    
    if matches:
        return matches[0]
    
    return None


def find_similar_colors(color: Color, colors_file: str, max_results: int = 5) -> List[Tuple[str, Color, float, str]]:
    """
    Find colors similar to the given color.
    
    Args:
        color: The reference color
        colors_file: Path to the colors file
        max_results: Maximum number of results to return
        
    Returns:
        List of tuples (color_name, color, similarity_score, color_id)
        where similarity_score is between 0 and 1 (1 being identical)
    """
    # Load colors with IDs as keys
    colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    
    # Calculate color distance for each color
    color_distances = []
    for color_id, info in colors.items():
        color_name = info["name"]
        c = info["color"]
        
        # Ensure both colors have the same dimensions
        c1 = color[:3]  # Take only RGB part of reference color
        c2 = c[:3]      # Take only RGB part of comparison color
        
        # Euclidean distance in RGB space (simple but not perceptually uniform)
        # Could be replaced with a better color distance metric if needed
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
        
        # Convert distance to similarity score (1 = identical, 0 = maximally different)
        # Sqrt(3) is max possible distance in RGB space with values 0-1
        similarity = 1 - distance / math.sqrt(3)
        
        color_distances.append((color_name, c, similarity, color_id))
    
    # Sort by similarity (highest first) and return top max_results
    return sorted(color_distances, key=lambda x: x[2], reverse=True)[:max_results]


def find_complementary_colors(color: Color, colors_file: str, max_results: int = 5) -> List[Tuple[str, Color, float, str]]:
    """
    Find complementary colors (colors on the opposite side of the color wheel).
    
    Args:
        color: The reference color
        colors_file: Path to the colors file
        max_results: Maximum number of results to return
        
    Returns:
        List of tuples (color_name, color, complementary_score, color_id)
        where complementary_score measures how well the colors complement each other
    """
    # Load colors with IDs as keys
    colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    
    # Convert reference color to HSV
    h, s, v = rgb_to_hsv(color[:3])
    
    # Calculate complementary color's hue (opposite on color wheel)
    complementary_h = (h + 180) % 360
    
    # Find colors that are close to the complementary hue
    complementary_colors = []
    for color_id, info in colors.items():
        color_name = info["name"]
        c = info["color"]
        
        # Convert to HSV
        ch, cs, cv = rgb_to_hsv(c[:3])
        
        # Calculate hue distance (0-180, where 0 means perfectly complementary)
        hue_distance = min(abs(ch - complementary_h), 360 - abs(ch - complementary_h))
        
        # Convert to a score where 1 means perfectly complementary
        # and 0 means least complementary (same hue)
        complementary_score = 1 - (hue_distance / 180)
        
        complementary_colors.append((color_name, c, complementary_score, color_id))
    
    # Sort by complementary score (highest first) and return top max_results
    return sorted(complementary_colors, key=lambda x: x[2], reverse=True)[:max_results]


def find_similar_colors_by_brightness(color: Color, colors_file: str, max_results: int = 5) -> List[Tuple[str, Color, float, str]]:
    """
    Find colors similar to the given color and sort them from dark to light.
    
    Args:
        color: The reference color
        colors_file: Path to the colors file
        max_results: Maximum number of results to return
        
    Returns:
        List of tuples (color_name, color, similarity_score, color_id)
        sorted from darkest to lightest
    """
    # First find similar colors
    similar_colors = find_similar_colors(color, colors_file, max_results=max_results*2)
    
    # Calculate brightness for each color
    colors_with_brightness = []
    for name, color, similarity, color_id in similar_colors:
        _, _, v = rgb_to_hsv(color[:3])  # v represents brightness
        colors_with_brightness.append((name, color, similarity, color_id, v))
    
    # Sort by brightness (darkest first)
    sorted_colors = sorted(colors_with_brightness, key=lambda x: x[4])
    
    # Return the results without the brightness value in the tuple
    return [(name, color, similarity, color_id) for name, color, similarity, color_id, _ in sorted_colors[:max_results]] 