
from vision.vision_analyzer import analyze_image

image_path = input("Enter image path: ").strip().strip('"')

description = analyze_image(image_path)

print("\nIMAGE DESCRIPTION:")
print(description)
