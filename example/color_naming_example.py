"""
Example of using the improved color naming system.
"""

import os
import sys
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from scivis_wrx import (
    save_colors,
    load_colors,
    extract_dominant_colors,
    add_colors_from_image,
    generate_color_id,
    generate_color_name,
    rgb_to_hsv,
    BASIC_COLOR_NAMES
)

# Set up directories
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
colors_file = output_dir / "named_colors.json"

def display_color_grid(colors_dict, title="Color Grid", cols=5, use_id_as_key=True):
    """Display a grid of colors with their names and IDs."""
    # Calculate rows needed
    rows = len(colors_dict) // cols + (1 if len(colors_dict) % cols else 0)
    
    # Create figure
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 2))
    
    # Ensure axes is a 2D array even if we have only one row
    if rows == 1:
        axes = np.array([axes])
    if cols == 1:
        axes = axes.reshape(-1, 1)
    
    # Flatten axes for easy iteration
    axes = axes.flatten()
    
    # Plot each color
    for i, (key, value) in enumerate(colors_dict.items()):
        if i < len(axes):
            if use_id_as_key:
                # Key is the color ID
                color_id = key
                if isinstance(value, dict):
                    color = value["color"]
                    name = value.get("name", "unnamed")
                else:
                    color = value
                    name = f"color_{color_id[:6]}"
            else:
                # Key is the color name
                name = key
                if isinstance(value, dict):
                    color = value["color"]
                    color_id = value.get("id", generate_color_id(color))
                else:
                    color = value
                    color_id = generate_color_id(color)
                
            ax = axes[i]
            ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=color))
            
            # Calculate whether to use white or black text
            text_color = 'white' if sum(color[:3]) < 1.5 else 'black'
            
            # Get HSV values for display
            h, s, v = rgb_to_hsv(color)
            rgb_val = [int(c * 255) for c in color[:3]]
            
            # Display color name and information
            name_parts = name.split('_')
            if len(name_parts) > 2:
                # Format name for better display
                name_line1 = '_'.join(name_parts[:2])
                name_line2 = '_'.join(name_parts[2:])
                name_display = f"{name_line1}\n{name_line2}"
            else:
                name_display = name
                
            hsv_info = f"H:{h:.0f}° S:{s:.2f} V:{v:.2f}"
            rgb_info = f"RGB: {rgb_val}"
            id_info = f"ID: {color_id[:6]}..."
            
            label = f"{name_display}\n{hsv_info}\n{rgb_info}\n{id_info}"
            ax.text(0.5, 0.5, label, 
                    ha='center', va='center', color=text_color,
                    fontsize=8, fontweight='bold')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
    
    # Hide any unused subplots
    for i in range(len(colors_dict), len(axes)):
        fig.delaxes(axes[i])
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    return fig

def create_sample_colors():
    """Create a sample set of colors with descriptive names."""
    # Create a range of sample colors
    sample_colors = {}
    
    # Add a spectrum of hues with different saturations and values
    for h in range(0, 360, 30):  # 12 hues around the color wheel
        for s in [0.3, 0.7, 1.0]:  # 3 saturation levels
            for v in [0.3, 0.7, 1.0]:  # 3 value (brightness) levels
                # Convert HSV to RGB
                h_norm = h / 360
                c = v * s
                x = c * (1 - abs((h_norm * 6) % 2 - 1))
                m = v - c
                
                if h_norm < 1/6:
                    r, g, b = c, x, 0
                elif h_norm < 2/6:
                    r, g, b = x, c, 0
                elif h_norm < 3/6:
                    r, g, b = 0, c, x
                elif h_norm < 4/6:
                    r, g, b = 0, x, c
                elif h_norm < 5/6:
                    r, g, b = x, 0, c
                else:
                    r, g, b = c, 0, x
                
                r, g, b = r + m, g + m, b + m
                color = (r, g, b)
                
                # Generate a descriptive name
                name = generate_color_name(color)
                
                # Generate ID
                color_id = generate_color_id(color)
                
                # Add to sample colors with ID as key
                sample_colors[color_id] = {
                    "color": color,
                    "name": name
                }
    
    return sample_colors

def rename_existing_colors(colors_file):
    """Rename colors in an existing color file using the new naming system."""
    if not os.path.exists(colors_file):
        print(f"Color file not found: {colors_file}")
        return
    
    # Load existing colors
    colors = load_colors(colors_file, include_ids=True)
    
    # Create a new dictionary with better names
    renamed_colors = {}
    existing_names = set()
    
    for old_name, info in colors.items():
        color = info["color"]
        color_id = info["id"]
        
        # Extract context from the old name if possible
        context = ""
        parts = old_name.split('_')
        if len(parts) > 1:
            context = parts[-1]
        
        # Generate a better name
        base_name = generate_color_name(color, context)
        new_name = base_name
        
        # Make sure the name is unique
        counter = 1
        while new_name in existing_names:
            new_name = f"{base_name}_{counter}"
            counter += 1
        
        existing_names.add(new_name)
        
        # Add to renamed colors
        renamed_colors[color_id] = {
            "color": color,
            "name": new_name
        }
    
    # Save the renamed colors
    renamed_file = output_dir / "renamed_colors.json"
    save_colors(renamed_colors, renamed_file, use_id_as_key=True)
    
    return renamed_colors

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Demonstrate the color naming system")
    parser.add_argument("-r", "--rename", help="Path to a color file to rename")
    parser.add_argument("-i", "--image", help="Path to an image to extract colors from")
    parser.add_argument("-c", "--convert", help="Convert a color file to use ID as key")
    
    args = parser.parse_args()
    
    # Handle file format conversion if requested
    if args.convert:
        if not os.path.exists(args.convert):
            print(f"File not found: {args.convert}")
        else:
            print(f"Converting color file format: {args.convert}")
            try:
                # Load the colors in any format
                with open(args.convert, 'r') as f:
                    loaded_data = json.load(f)
                
                # Create output path
                convert_base = Path(args.convert).stem
                convert_dir = Path(args.convert).parent
                converted_file = convert_dir / f"{convert_base}_id_based.json"
                
                # Transform to ID-based format
                id_based_colors = {}
                
                for key, value in loaded_data.items():
                    if isinstance(value, list):
                        # Simple [r,g,b] format
                        color = tuple(value)
                        color_id = generate_color_id(color)
                        id_based_colors[color_id] = {
                            "color": value,
                            "name": key
                        }
                    elif isinstance(value, dict) and "color" in value:
                        if "id" in value:
                            # Name->{"color":..., "id":...} format
                            color_id = value["id"]
                            id_based_colors[color_id] = {
                                "color": value["color"],
                                "name": key
                            }
                        elif "name" in value:
                            # Already in ID->{"color":..., "name":...} format
                            id_based_colors[key] = value
                
                # Save converted file
                with open(converted_file, 'w') as f:
                    json.dump(id_based_colors, f, indent=2)
                
                print(f"Converted {len(id_based_colors)} colors to ID-based format")
                print(f"Saved to: {converted_file}")
            except Exception as e:
                print(f"Error converting file: {e}")
    
    # Create and display sample colors
    print("Creating sample colors...")
    sample_colors = create_sample_colors()
    
    # Save sample colors
    save_colors(sample_colors, colors_file, use_id_as_key=True)
    print(f"Saved {len(sample_colors)} sample colors to {colors_file}")
    
    # Display a subset of the sample colors
    subset = dict(list(sample_colors.items())[:20])
    fig1 = display_color_grid(subset, title="Sample Named Colors", cols=4, use_id_as_key=True)
    fig1.savefig(output_dir / "sample_colors.png")
    
    # Rename existing colors if requested
    if args.rename:
        print(f"Renaming colors in {args.rename}...")
        renamed_colors = rename_existing_colors(args.rename)
        if renamed_colors:
            print(f"Renamed {len(renamed_colors)} colors")
            
            # Display a subset of the renamed colors
            subset = dict(list(renamed_colors.items())[:20])
            fig2 = display_color_grid(subset, title="Renamed Colors", cols=4, use_id_as_key=True)
            fig2.savefig(output_dir / "renamed_colors.png")
            
            # Compare old and new names
            original_colors = load_colors(args.rename, include_ids=True)
            
            print("\nSample of renamed colors:")
            for i, ((old_name, old_info), (new_name, new_info)) in enumerate(
                zip(list(original_colors.items())[:10], list(renamed_colors.items())[:10])
            ):
                if old_info["id"] == new_info["id"]:
                    rgb = [int(c * 255) for c in old_info["color"][:3]]
                    print(f"  {i+1}. {old_name:30} -> {new_name:30} (RGB: {rgb})")
    
    # Extract colors from an image if requested
    if args.image:
        image_path = args.image
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
        else:
            print(f"\nExtracting colors from {image_path}...")
            
            # Extract colors with descriptive names
            color_ids = add_colors_from_image(image_path, colors_file, n_colors=10)
            
            if color_ids:
                # Load the colors to display them
                image_colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
                
                # Filter to just the ones extracted from this image
                extracted_colors = {color_id: info for color_id, info in image_colors.items() 
                                  if color_id in color_ids}
                
                print(f"Extracted {len(extracted_colors)} colors with descriptive names:")
                for color_id, info in extracted_colors.items():
                    name = info["name"]
                    color = info["color"]
                    rgb = [int(c * 255) for c in color[:3]]
                    print(f"  ID: {color_id[:10]}... -> {name:30} - RGB: {rgb}")
                
                # Display the extracted colors
                fig3 = display_color_grid(extracted_colors, 
                                         title=f"Colors from {Path(image_path).name}", 
                                         cols=3,
                                         use_id_as_key=True)
                fig3.savefig(output_dir / f"{Path(image_path).stem}_named_colors.png")
    
    plt.show()
    return 0

if __name__ == "__main__":
    sys.exit(main()) 