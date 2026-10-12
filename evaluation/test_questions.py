from retrieval.retriever import retrieve
from reranking.reranker import rerank
from generation.generator import generate_answer
test_questions = [
    {
        "question": "What was the company's revenue in 2024?",
        "expected": ["$42 million", "42 million USD", "42 million"],
        "answerable": True
    },
    {
        "question": "How many employees did the company have at the end of 2024?",
        "expected": "not available",
        "answerable": False
    },
    
    {
        "question": "How much did the company invest in research and development in 2024?",
        "expected": "not available",
        "answerable": False
    },

    
    
    {
        "question": "What was Asterion Technologies' revenue in 2023?",
        "expected": "30",
        "answerable": True
    },
    {
        "question": "What trend does the revenue chart show from 2022 to 2025?",
        "expected": ["increasing", "upward trend", "rises steadily"],
        "answerable": True
    },
    {
        "question": "What is the capital of Japan?",
        "expected": "not available",
        "answerable": False
    }
]

retrieval_hits = 0
answerable_questions = 0
answer_correct = 0
grounding_supported = 0

abstention_correct = 0
unanswerable_questions = 0

for test in test_questions:
    question = test["question"]
    expected = test["expected"]
    is_answerable = test["answerable"]

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    # 1. Retrieve relevant chunks from ChromaDB
    results = retrieve(
        question,
        top_k=5,
        document_name="omniscIa_chart_test.pdf"
    )

    # 2. Rerank the retrieved chunks
    results = rerank(question, results, top_n=3)

    # 3. Generate an answer using the selected chunks
    answer = generate_answer(question, results)

    print("\nEXPECTED:", expected)
    print("ANSWER:", answer)

    # Combine the retrieved chunks into one string
    retrieved_text = " ".join(
        chunk["text"] for chunk in results
    )

    print("\nRETRIEVED CONTEXT:")
    print(retrieved_text)

    
    # Convert expected answer into a list of phrases
    if isinstance(expected, str):
        expected_phrases = [expected]
    else:
        expected_phrases = expected

    # Check retrieved context
    retrieval_pass = any(
        phrase.lower() in retrieved_text.lower()
        for phrase in expected_phrases
    )

    # Check generated answer
    answer_pass = any(
        phrase.lower() in answer.lower()
        for phrase in expected_phrases
    )


    if is_answerable:
        answerable_questions += 1

        if retrieval_pass:
            retrieval_hits += 1
            print("\nRETRIEVAL: PASS")
        else:
            print("\nRETRIEVAL: FAIL")

        if answer_pass:
            answer_correct += 1
            print("ANSWER MATCH: PASS")
        else:
            print("ANSWER MATCH: FAIL")

        if retrieval_pass and answer_pass:
            grounding_supported += 1
            print("GROUNDING PROXY: PASS")
        else:
            print("GROUNDING PROXY: FAIL")

    else:
        unanswerable_questions += 1

        # This checks only for the phrase used by your prompt
        if "not available" in answer.lower():
            abstention_correct += 1
            print("\nABSTENTION: PASS")
        else:
            print("\nABSTENTION: FAIL")


# Calculate metrics safely
def calculate_rate(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator


retrieval_rate = calculate_rate(
    retrieval_hits, answerable_questions
)

answer_rate = calculate_rate(
    answer_correct, answerable_questions
)

grounding_rate = calculate_rate(
    grounding_supported, answerable_questions
)

abstention_rate = calculate_rate(
    abstention_correct, unanswerable_questions
)


# Print the final evaluation report
print("\n" + "=" * 60)
print("OMNISCIA EVALUATION REPORT")
print("=" * 60)

print(
    f"Retrieval Hit Rate: {retrieval_hits}/"
    f"{answerable_questions} "
    f"({retrieval_rate:.2%})"
    if retrieval_rate is not None
    else "Retrieval Hit Rate: N/A"
)

print(
    f"Answer Match Rate: {answer_correct}/"
    f"{answerable_questions} "
    f"({answer_rate:.2%})"
    if answer_rate is not None
    else "Answer Match Rate: N/A"
)

print(
    f"Grounding Proxy: {grounding_supported}/"
    f"{answerable_questions} "
    f"({grounding_rate:.2%})"
    if grounding_rate is not None
    else "Grounding Proxy: N/A"
)

print(
    f"Abstention Accuracy: {abstention_correct}/"
    f"{unanswerable_questions} "
    f"({abstention_rate:.2%})"
    if abstention_rate is not None
    else "Abstention Accuracy: N/A"
)
