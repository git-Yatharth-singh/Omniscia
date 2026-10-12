
import ollama


def analyze_image(image_path):
    response = ollama.chat(
        model="gemma4:e2b",
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze this image for a document question-answering "
                    "system. Describe its content accurately. If it is a "
                    "chart or graph, identify the title, axes, labels, "
                    "visible values, and trends. If it is a diagram, "
                    "explain its components and relationships. Do not "
                    "invent information that is not visible."
                ),
                "images": [image_path],
            }
        ],
    )

    return response.message.content
