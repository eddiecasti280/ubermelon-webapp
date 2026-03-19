#!/usr/bin/env python3
"""
Sprite Parser for Foods.png
Extracts 16x16 sprites from the sprite sheet and saves them individually.
"""

from PIL import Image
import os

def parse_sprites(input_path, output_dir):
    """
    Parse the Foods.png sprite sheet and extract individual sprites.
    
    The sprite sheet is 128x96 pixels with 16x16 sprites.
    That gives us 8 columns and 6 rows.
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the sprite sheet
    sprite_sheet = Image.open(input_path)
    
    # Sprite dimensions
    sprite_width = 16
    sprite_height = 16
    
    # Calculate grid dimensions
    cols = sprite_sheet.width // sprite_width   # 8 columns
    rows = sprite_sheet.height // sprite_height  # 6 rows
    
    # Define sprite names row by row
    # None means skip this sprite
    sprite_names = [
        # Row 1: Apples
        ["red_apple", "granny_smith_apple", "golden_delicious_apple", 
         "ambrosia_apple", "honeycrisp_apple", "half_apple", None, None],
        # Row 2: Pears
        ["concorde_pear", "bartlett_pear", "bosk_pear", "chinese_white_pear",
         "forelle_pear", "seckel_pear", "conference_pear", None],
        # Row 3: Vegetables
        ["tomato", "yellow_tomato", "pumpkin", "carrot", 
         "pea_pod", "bell_pepper", "yellow_bell_pepper", "green_bell_pepper"],
        # Row 4: Breakfast/Fast food
        ["scrambled_egg", "bacon", "crispy_bacon", "cheese", 
         "pizza_slice", "hot_dog", None, None],
        # Row 5: Holiday treats
        ["candy_cane", "gingerbread_man", "gingerbread_man_base", None,
         "gingerbread_house", "glintwein", "eggnog", "glass_of_milk"],
        # Row 6: Thanksgiving
        ["mashed_potatoes", "gravy", "cranberry_sauce", None, 
         None, None, None, None],
    ]
    
    extracted_sprites = []
    
    for row in range(rows):
        for col in range(cols):
            # Get sprite name for this position
            if row < len(sprite_names) and col < len(sprite_names[row]):
                sprite_name = sprite_names[row][col]
            else:
                sprite_name = None
            
            # Skip if no name (either not used or empty cell)
            if sprite_name is None:
                continue
            
            # Calculate the bounding box for this sprite
            left = col * sprite_width
            upper = row * sprite_height
            right = left + sprite_width
            lower = upper + sprite_height
            
            # Extract the sprite
            sprite = sprite_sheet.crop((left, upper, right, lower))
            
            # Save the sprite
            output_path = os.path.join(output_dir, f"{sprite_name}.png")
            sprite.save(output_path)
            
            extracted_sprites.append(sprite_name)
            print(f"Extracted: {sprite_name}.png")
    
    return extracted_sprites


def main():
    """Main entry point for sprite parsing."""
    input_path = "static/img/Foods.png"
    output_dir = "static/img/sprites"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        print("Please place Foods.png in static/img/ directory.")
        return
    
    print("Parsing sprite sheet...")
    sprites = parse_sprites(input_path, output_dir)
    print(f"\nSuccessfully extracted {len(sprites)} sprites to {output_dir}/")


if __name__ == "__main__":
    main()