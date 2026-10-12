
from retrieval.retriever import retrieve

def test_irrelevant_question():
    results = retrieve("What is the capital of Japan?")
    assert results == [], "Irrelevant results should be rejected."
    print("\nRetrieved results:")
    for result in results:
        print("Distance:", result["distance"])
        print("Text:", result["text"][:200])


def test_relevant_question():
    results = retrieve(
        "What was Asterion Technologies' revenue in 2024?"
    )
    assert len(results) > 0, "Relevant results should be retained."
    print("\nRelevant question results:")
    for result in results:
        print("Distance:", result["distance"])
        print("Text:", result["text"][:200])

    assert len(results) > 0
