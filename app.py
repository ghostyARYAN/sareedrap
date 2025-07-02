from PIL import Image
import os

# Paths to mask files (make sure these exist)
MASKS = {
    "pallu": "static/masks/pallu_mask.png",
    "blouse": "static/masks/blouse_mask.png",
    "body": "static/masks/body_mask.png"
}

def generate_saree_from_files(pallu_path, blouse_path, body_path):
    # Load user uploaded parts
    pallu = Image.open(pallu_path).convert('RGBA')
    blouse = Image.open(blouse_path).convert('RGBA')
    body = Image.open(body_path).convert('RGBA')

    # Load masks
    pallu_mask = Image.open(MASKS["pallu"]).convert('L')
    blouse_mask = Image.open(MASKS["blouse"]).convert('L')
    body_mask = Image.open(MASKS["body"]).convert('L')

    # Use pallu_mask size as the base size
    base_size = pallu_mask.size

    # Resize all images and masks to base_size
    pallu = pallu.resize(base_size)
    blouse = blouse.resize(base_size)
    body = body.resize(base_size)
    pallu_mask = pallu_mask.resize(base_size)
    blouse_mask = blouse_mask.resize(base_size)
    body_mask = body_mask.resize(base_size)

    # Apply masks (L mode is greyscale used for alpha masking)
    pallu.putalpha(pallu_mask)
    blouse.putalpha(blouse_mask)
    body.putalpha(body_mask)

    # Combine all on blank transparent canvas
    final_img = Image.new("RGBA", base_size, (255, 255, 255, 0))
    final_img = Image.alpha_composite(final_img, body)
    final_img = Image.alpha_composite(final_img, blouse)
    final_img = Image.alpha_composite(final_img, pallu)

    # Save result
    output_path = "output/final_preview.png"
    os.makedirs("output", exist_ok=True)
    final_img.save(output_path)
    print(f"Saved output to {output_path}")

if __name__ == "__main__":
    # Example usage: change these paths to your test images
    generate_saree_from_files(
        "input/pallu_mask.png",
        "input/blouse_mask.png",
        "input/body_mask.png"
    )
