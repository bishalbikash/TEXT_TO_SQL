
# from backend.evaluation import (
#     run_execution_evaluation,
#     calculate_execution_accuracy,
# )
# from backend.test_cases import TEST_CASES


# def main():
#     print("\nStarting SQL evaluation...\n")

#     results = run_execution_evaluation(TEST_CASES)

#     for result in results:
#         print("-" * 60)
#         print("Question:", result["question"])
#         print("Generated SQL:", result["generated_sql"])
#         print("Reference SQL:", result["reference_sql"])
#         print(
#             "Correct:",
#             "Yes" if result["execution_accuracy"] else "No"
#         )

#     accuracy = calculate_execution_accuracy(results)

#     print("\n" + "=" * 60)
#     print(f"Execution Accuracy: {accuracy:.2%}")
#     print("=" * 60)


# if __name__ == "__main__":
#     main()


from backend.evaluation import (
    run_execution_evaluation,
    calculate_execution_accuracy,
    run_ragas_evaluation,
)
from backend.test_cases import TEST_CASES


def main():
    print("\nStarting SQL evaluation...\n")

    results = run_execution_evaluation(TEST_CASES)

    for result in results:
        print("-" * 60)
        print("Question:", result["question"])
        print("Generated SQL:", result["generated_sql"])
        print("Reference SQL:", result["reference_sql"])
        print(
            "Correct:",
            "Yes" if result["execution_accuracy"] else "No"
        )

    accuracy = calculate_execution_accuracy(results)

    print("\nExecution Accuracy:", f"{accuracy:.2%}")

    # Run RAGAS evaluation
    print("\nStarting RAGAS evaluation...\n")

    try:
        ragas_results = run_ragas_evaluation(TEST_CASES, results)
        print(ragas_results)
    except Exception as e:
        print(f"RAGAS evaluation failed: {e}")


if __name__ == "__main__":
    main()
