
from generation.llm_client import LLMClient

llm = LLMClient()

prompt = """
You are a document question-answering assistant.

Context:
Revenue was 20 million in 2022, 30 million in 2023,
42 million in 2024, and 55 million in 2025.

Question:
What trend does the revenue chart show from 2022 to 2025?

Answer in one or two sentences using only the context.
"""

answer = llm.generate(prompt)

print("\nMODEL RESPONSE:")
print(answer)
