
import ollama

image_path = input("Enter the path to an image: ").strip().strip('"')

response = ollama.chat(
    model="gemma4:e2b",
    messages=[
        {
            "role": "user",
            "content": (
                "Describe this image. If it is a chart, "
                "explain its title, axes, and visible trends."
            ),
            "images": [image_path],
        }
    ],
)

print("\nVISION MODEL RESPONSE:")
print(response.message.content)
