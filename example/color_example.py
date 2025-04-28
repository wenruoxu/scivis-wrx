"""
Example of using scivis_wrx color utilities.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scivis_wrx import (
    save_colors, 
    load_colors, 
    get_color, 
    add_color, 
    DEFAULT_COLORS
)

# Define the colors file path
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
colors_file = output_dir / "custom_colors.json"

def display_colors(colors_dict, title="Colors"):
    """Display a grid of colors with their names."""
    fig, axes = plt.subplots(
        nrows=len(colors_dict) // 4 + (1 if len(colors_dict) % 4 else 0),
        ncols=4,
        figsize=(10, len(colors_dict) // 4 * 2 + 2)
    )
    axes = axes.flatten()
    
    for i, (name, color) in enumerate(colors_dict.items()):
        if i < len(axes):
            axes[i].add_patch(
                plt.Rectangle((0, 0), 1, 1, color=color)
            )
            axes[i].text(
                0.5, 0.5, name,
                ha='center', va='center',
                color='white' if sum(color[:3]) < 1.5 else 'black'
            )
            axes[i].set_xlim(0, 1)
            axes[i].set_ylim(0, 1)
            axes[i].set_xticks([])
            axes[i].set_yticks([])
    
    # Hide any unused subplots
    for i in range(len(colors_dict), len(axes)):
        fig.delaxes(axes[i])
    
    plt.suptitle(title)
    plt.tight_layout()
    return fig

def main():
    # Save default colors to a file
    print(f"Saving default colors to {colors_file}")
    save_colors(DEFAULT_COLORS, colors_file)
    
    # Load colors from the file
    loaded_colors = load_colors(colors_file)
    print(f"Loaded colors: {list(loaded_colors.keys())}")
    
    # Add some custom colors
    custom_colors = {
        "deep_blue": (0.0, 0.1, 0.5),
        "forest_green": (0.0, 0.4, 0.2),
        "hot_pink": (1.0, 0.1, 0.7),
        "gold": (1.0, 0.7, 0.0),
        "sky_blue": (0.4, 0.7, 1.0)
    }
    
    # Add each custom color to our colors file
    for name, color in custom_colors.items():
        print(f"Adding color: {name}")
        add_color(name, color, colors_file)
    
    # Load the updated colors
    updated_colors = load_colors(colors_file)
    print(f"Updated colors: {list(updated_colors.keys())}")
    
    # Use get_color to retrieve a specific color
    try:
        blue_color = get_color("blue", colors_file)
        print(f"Retrieved blue color: {blue_color}")
        
        hot_pink = get_color("hot_pink", colors_file)
        print(f"Retrieved hot_pink color: {hot_pink}")
        
        # This will fail
        not_a_color = get_color("not_a_real_color", colors_file)
    except KeyError as e:
        print(f"Error: {e}")
    
    # Display the colors
    fig = display_colors(updated_colors, "scivis_wrx Color Palette")
    plt.savefig(output_dir / "color_palette.png")
    plt.show()

if __name__ == "__main__":
    main() 