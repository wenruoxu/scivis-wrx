"""
Example of extracting colors from an image and generating color IDs.
"""

import os
import sys
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scivis_wrx import (
    save_colors,
    load_colors,
    extract_dominant_colors,
    add_colors_from_image,
    generate_color_id,
    get_color_by_id,
    find_similar_colors,
    find_complementary_colors,
    find_similar_colors_by_brightness
)

# Set up directories
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
colors_file = output_dir / "image_colors.json"

def display_image_with_colors(image_path, colors, color_ids=None, title="Extracted Colors"):
    """Display the image alongside the extracted colors."""
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Display the image
    img = plt.imread(image_path)
    ax1.imshow(img)
    ax1.set_title("Source Image")
    ax1.axis('off')
    
    # Display the extracted colors
    height = 1.0 / len(colors)
    for i, (color, count) in enumerate(colors):
        y = 1.0 - (i + 1) * height
        rect = patches.Rectangle((0, y), 1, height, color=color)
        ax2.add_patch(rect)
        
        # Calculate text color (white for dark backgrounds, black for light backgrounds)
        text_color = 'white' if sum(color[:3]) < 1.5 else 'black'
        
        # Display color info
        color_id = color_ids[i] if color_ids and i < len(color_ids) else generate_color_id(color)
        rgb_values = [int(c * 255) for c in color[:3]]
        
        label = f"RGB: {rgb_values}\nID: {color_id[:6]}...\nCount: {count}"
        ax2.text(0.5, y + height/2, label, 
                ha='center', va='center', color=text_color,
                fontsize=10)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title(title)
    ax2.axis('off')
    
    plt.tight_layout()
    return fig

def display_similar_colors(color, similar_colors, color_id=None, title="Similar Colors"):
    """Display a color and its similar colors."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Number of colors to display
    n_colors = len(similar_colors) + 1
    
    # Display the reference color
    rect = patches.Rectangle((0, 0), 1, 1/n_colors, color=color)
    ax.add_patch(rect)
    
    # Calculate text color
    text_color = 'white' if sum(color[:3]) < 1.5 else 'black'
    
    # Display color info
    if not color_id:
        color_id = generate_color_id(color)
    rgb_values = [int(c * 255) for c in color[:3]]
    label = f"Reference\nRGB: {rgb_values}\nID: {color_id}"
    ax.text(0.5, 1/(2*n_colors), label, 
            ha='center', va='center', color=text_color,
            fontsize=10)
    
    # Display similar colors
    for i, (name, similar_color, similarity, similar_id) in enumerate(similar_colors):
        y = (i + 1) / n_colors
        rect = patches.Rectangle((0, y), 1, 1/n_colors, color=similar_color)
        ax.add_patch(rect)
        
        # Calculate text color
        text_color = 'white' if sum(similar_color[:3]) < 1.5 else 'black'
        
        # Display color info
        rgb_values = [int(c * 255) for c in similar_color[:3]]
        similarity_pct = similarity * 100
        label = f"{name}\nRGB: {rgb_values}\nID: {similar_id[:6]}...\nSimilarity: {similarity_pct:.1f}%"
        ax.text(0.5, y + 1/(2*n_colors), label, 
                ha='center', va='center', color=text_color,
                fontsize=10)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def display_complementary_colors(color, complementary_colors, color_id=None, title="Complementary Colors"):
    """Display a color and its complementary colors."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Number of colors to display
    n_colors = len(complementary_colors) + 1
    
    # Display the reference color
    rect = patches.Rectangle((0, 0), 1, 1/n_colors, color=color)
    ax.add_patch(rect)
    
    # Calculate text color
    text_color = 'white' if sum(color[:3]) < 1.5 else 'black'
    
    # Display color info
    if not color_id:
        color_id = generate_color_id(color)
    rgb_values = [int(c * 255) for c in color[:3]]
    label = f"Reference\nRGB: {rgb_values}\nID: {color_id}"
    ax.text(0.5, 1/(2*n_colors), label, 
            ha='center', va='center', color=text_color,
            fontsize=10)
    
    # Display complementary colors
    for i, (name, comp_color, comp_score, comp_id) in enumerate(complementary_colors):
        y = (i + 1) / n_colors
        rect = patches.Rectangle((0, y), 1, 1/n_colors, color=comp_color)
        ax.add_patch(rect)
        
        # Calculate text color
        text_color = 'white' if sum(comp_color[:3]) < 1.5 else 'black'
        
        # Display color info
        rgb_values = [int(c * 255) for c in comp_color[:3]]
        comp_score_pct = comp_score * 100
        label = f"{name}\nRGB: {rgb_values}\nID: {comp_id[:6]}...\nComp. Score: {comp_score_pct:.1f}%"
        ax.text(0.5, y + 1/(2*n_colors), label, 
                ha='center', va='center', color=text_color,
                fontsize=10)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def display_colors_by_brightness(color, similar_colors, color_id=None, title="Similar Colors (Dark to Light)"):
    """Display similar colors sorted by brightness from dark to light."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Number of colors to display
    n_colors = len(similar_colors) + 1
    
    # Display the reference color
    rect = patches.Rectangle((0, 0), 1, 1/n_colors, color=color)
    ax.add_patch(rect)
    
    # Calculate text color
    text_color = 'white' if sum(color[:3]) < 1.5 else 'black'
    
    # Display color info
    if not color_id:
        color_id = generate_color_id(color)
    rgb_values = [int(c * 255) for c in color[:3]]
    label = f"Reference\nRGB: {rgb_values}\nID: {color_id}"
    ax.text(0.5, 1/(2*n_colors), label, 
            ha='center', va='center', color=text_color,
            fontsize=10)
    
    # Display similar colors by brightness
    for i, (name, similar_color, similarity, similar_id) in enumerate(similar_colors):
        y = (i + 1) / n_colors
        rect = patches.Rectangle((0, y), 1, 1/n_colors, color=similar_color)
        ax.add_patch(rect)
        
        # Calculate text color
        text_color = 'white' if sum(similar_color[:3]) < 1.5 else 'black'
        
        # Display color info
        rgb_values = [int(c * 255) for c in similar_color[:3]]
        similarity_pct = similarity * 100
        label = f"{name}\nRGB: {rgb_values}\nID: {similar_id[:6]}...\nSimilarity: {similarity_pct:.1f}%"
        ax.text(0.5, y + 1/(2*n_colors), label, 
                ha='center', va='center', color=text_color,
                fontsize=10)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def is_image_file(file_path):
    """Check if a file is an image based on its extension."""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    return file_path.suffix.lower() in image_extensions

def process_image(image_path, colors_file, n_colors=5, show_plots=False):
    """Process a single image and extract colors."""
    try:
        print(f"Processing image: {image_path}")
        
        # Extract dominant colors from the image
        dominant_colors = extract_dominant_colors(
            image_path, 
            n_colors=n_colors, 
            exclude_white=True
        )
        
        if not dominant_colors:
            print(f"  Warning: No dominant colors found in {image_path}")
            return None
        
        # Display the extracted colors with their IDs
        print(f"  Extracted {len(dominant_colors)} colors:")
        for i, (color, count) in enumerate(dominant_colors):
            color_id = generate_color_id(color)
            rgb = [int(c * 255) for c in color[:3]]
            print(f"    Color {i+1}: RGB={rgb}, ID={color_id}, Count={count}")
        
        # Save the colors to the colors file and get their IDs
        color_names = add_colors_from_image(
            image_path,
            colors_file,
            n_colors=n_colors
        )
        
        # Get ordered list of color IDs to match dominant_colors order
        ordered_color_ids = []
        for i, (color, _) in enumerate(dominant_colors):
            color_id = generate_color_id(color)
            if color_id in color_names:
                ordered_color_ids.append(color_id)
        
        # Create output directory based on parent folder structure
        rel_path = Path(image_path).relative_to(Path.cwd()) if Path(image_path).is_absolute() else Path(image_path)
        parent_dir = rel_path.parent
        image_output_dir = output_dir / parent_dir
        image_output_dir.mkdir(exist_ok=True, parents=True)
        
        # Display the image with extracted colors
        fig1 = display_image_with_colors(
            image_path, 
            dominant_colors,
            ordered_color_ids,
            title=f"Dominant Colors: {Path(image_path).name}"
        )
        
        output_img = image_output_dir / f"{Path(image_path).stem}_colors.png"
        fig1.savefig(output_img)
        print(f"  Saved color visualization to {output_img}")
        
        # Display similar colors for the most dominant color
        if dominant_colors:
            most_dominant_color = dominant_colors[0][0]
            most_dominant_id = ordered_color_ids[0] if ordered_color_ids else generate_color_id(most_dominant_color)
            
            # Get similar colors with their IDs
            similar_colors_info = find_similar_colors(
                most_dominant_color,
                colors_file,
                max_results=5
            )
            
            # Display similar colors
            fig2 = display_similar_colors(
                most_dominant_color,
                similar_colors_info,
                most_dominant_id,
                title=f"Similar Colors: {Path(image_path).name}"
            )
            
            output_similar = image_output_dir / f"{Path(image_path).stem}_similar.png"
            fig2.savefig(output_similar)
            print(f"  Saved similar colors visualization to {output_similar}")
            
            # Get complementary colors
            complementary_colors_info = find_complementary_colors(
                most_dominant_color,
                colors_file,
                max_results=5
            )
            
            # Display complementary colors
            fig3 = display_complementary_colors(
                most_dominant_color,
                complementary_colors_info,
                most_dominant_id,
                title=f"Complementary Colors: {Path(image_path).name}"
            )
            
            output_complementary = image_output_dir / f"{Path(image_path).stem}_complementary.png"
            fig3.savefig(output_complementary)
            print(f"  Saved complementary colors visualization to {output_complementary}")
            
            # Get similar colors by brightness
            similar_by_brightness = find_similar_colors_by_brightness(
                most_dominant_color,
                colors_file,
                max_results=5
            )
            
            # Display similar colors by brightness
            fig4 = display_colors_by_brightness(
                most_dominant_color,
                similar_by_brightness,
                most_dominant_id,
                title=f"Similar Colors (Dark to Light): {Path(image_path).name}"
            )
            
            output_brightness = image_output_dir / f"{Path(image_path).stem}_brightness.png"
            fig4.savefig(output_brightness)
            print(f"  Saved dark-to-light colors visualization to {output_brightness}")
        
        if show_plots:
            plt.show()
        else:
            plt.close('all')
            
        return color_names
        
    except Exception as e:
        print(f"  Error processing image {image_path}: {e}")
        return None

def find_image_files(directory):
    """Recursively find all image files in a directory."""
    image_files = []
    
    try:
        for item in Path(directory).glob('**/*'):
            if item.is_file() and is_image_file(item):
                image_files.append(item)
    except Exception as e:
        print(f"Error scanning directory {directory}: {e}")
    
    return image_files

def process_directory(directory, colors_file, n_colors=5, show_plots=False):
    """Process all images in a directory and its subdirectories."""
    image_files = find_image_files(directory)
    
    if not image_files:
        print(f"No image files found in {directory}")
        return
    
    print(f"Found {len(image_files)} image files in {directory}")
    
    results = {}
    for i, img_path in enumerate(image_files):
        print(f"\nProcessing image {i+1}/{len(image_files)}")
        color_ids = process_image(img_path, colors_file, n_colors, show_plots)
        if color_ids:
            results[str(img_path)] = color_ids
    
    # Create summary report
    print(f"\nProcessed {len(results)} images successfully")
    print(f"All extracted colors are stored in {colors_file}")
    
    # Save a summary report
    summary_file = output_dir / "color_extraction_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Summary report saved to {summary_file}")
    
    # Load all colors to display statistics
    all_colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
    print(f"Total unique colors in database: {len(all_colors)}")
    
    # Display statistics about the most frequently used color families
    color_families = {}
    for color_id, info in all_colors.items():
        # Use first 6 characters of ID (RGB hex part) to identify color family
        family_id = color_id[:6]
        if family_id not in color_families:
            color_families[family_id] = []
        color_families[family_id].append(info["name"])
    
    print(f"Number of color families: {len(color_families)}")
    print("Top 5 color families by number of variations:")
    sorted_families = sorted(color_families.items(), key=lambda x: len(x[1]), reverse=True)
    for i, (family_id, color_names) in enumerate(sorted_families[:5]):
        # Get a representative color for visualization
        rep_id = None
        for color_id in all_colors:
            if color_id.startswith(family_id):
                rep_id = color_id
                break
                
        if rep_id:
            rep_color = all_colors[rep_id]["color"]
            rgb = [int(c * 255) for c in rep_color[:3]]
            print(f"  Family {i+1}: ID prefix={family_id}, Colors={len(color_names)}, Example: {all_colors[rep_id]['name']} RGB={rgb}")
    
    return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract dominant colors from images in a directory")
    parser.add_argument("path", help="Path to an image file or directory")
    parser.add_argument("-n", "--num-colors", type=int, default=5, help="Number of colors to extract from each image (default: 5)")
    parser.add_argument("-s", "--show", action="store_true", help="Show plots for each image (warning: this can open many windows)")
    parser.add_argument("-o", "--output", help="Output JSON file for colors (default: outputs/image_colors.json)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed color information")
    parser.add_argument("-c", "--convert", action="store_true", help="Convert existing color file to ID-based format")
    
    args = parser.parse_args()
    
    # Set custom output file if specified
    global colors_file
    if args.output:
        colors_file = Path(args.output)
        colors_file.parent.mkdir(exist_ok=True, parents=True)
    
    # Convert existing file to new format if requested
    if args.convert and os.path.exists(colors_file):
        try:
            # Load existing data
            with open(colors_file, 'r') as f:
                old_data = json.load(f)
            
            # Check if conversion is needed
            needs_conversion = False
            if old_data:
                first_key = next(iter(old_data))
                first_value = old_data[first_key]
                
                # Check if the key is likely an ID (all hex digits, right length)
                if not (len(first_key) >= 12 and all(c in "0123456789abcdef" for c in first_key)):
                    needs_conversion = True
                
                # Check if the structure is name -> {color, id} instead of id -> {color, name}
                if isinstance(first_value, dict) and "id" in first_value and "name" not in first_value:
                    needs_conversion = True
            
            if needs_conversion:
                print(f"Converting {colors_file} to ID-based format...")
                backup_file = colors_file.with_suffix('.json.bak')
                # Create backup
                with open(backup_file, 'w') as f:
                    json.dump(old_data, f, indent=2)
                print(f"Backup created: {backup_file}")
                
                # Convert to new format
                new_data = {}
                for key, value in old_data.items():
                    if isinstance(value, list):
                        # Simple [r,g,b] format
                        color = tuple(value)
                        color_id = generate_color_id(color)
                        new_data[color_id] = {
                            "color": value,
                            "name": key
                        }
                    elif isinstance(value, dict) and "color" in value:
                        if "id" in value:
                            # Name->{"color":..., "id":...} format
                            color_id = value["id"]
                            new_data[color_id] = {
                                "color": value["color"],
                                "name": key
                            }
                
                # Save converted file
                with open(colors_file, 'w') as f:
                    json.dump(new_data, f, indent=2)
                
                print(f"Converted {len(new_data)} colors to ID-based format")
        except Exception as e:
            print(f"Error converting file: {e}")
    
    path = Path(args.path)
    
    if not path.exists():
        print(f"Error: Path not found: {path}")
        return 1
    
    if path.is_file():
        if is_image_file(path):
            process_image(path, colors_file, args.num_colors, args.show)
            
            # If verbose mode, print the full color database
            if args.verbose:
                all_colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
                print("\nFull color database:")
                for color_id, info in all_colors.items():
                    rgb = [int(c * 255) for c in info["color"][:3]]
                    print(f"  {info['name']}: RGB={rgb}, ID={color_id[:10]}...")
        else:
            print(f"Error: Not an image file: {path}")
            return 1
    elif path.is_dir():
        results = process_directory(path, colors_file, args.num_colors, args.show)
        
        # If verbose mode, print details of the processed images and their colors
        if args.verbose and results:
            print("\nDetailed results:")
            for img_path, color_ids in results.items():
                print(f"  {img_path}:")
                all_colors = load_colors(colors_file, include_meta=True, use_id_as_key=True)
                for color_id, name in color_ids.items():
                    if color_id in all_colors:
                        rgb = [int(c * 255) for c in all_colors[color_id]["color"][:3]]
                        print(f"    {name}: RGB={rgb}, ID={color_id[:10]}...")
    else:
        print(f"Error: Path is neither a file nor a directory: {path}")
        return 1
    
    print("Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())