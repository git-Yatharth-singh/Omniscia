import ollama
class LLMClient:
    def generate(self, prompt):
        try:
            response = ollama.chat(
        model="gemma4:e2b",
        messages=[
            {"role": "user", "content": prompt}
            ]
        )
            return response["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}") from e