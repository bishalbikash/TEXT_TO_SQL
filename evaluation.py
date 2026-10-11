# import json
# import os

# from .sql_agent import generate_sql
# from .rag import execute_sql


# # --------------------------------------------------
# # Cache Configuration
# # --------------------------------------------------

# CACHE_FILE = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)),
#     "sql_cache.json"
# )


# # --------------------------------------------------
# # Load SQL Cache
# # --------------------------------------------------

# def load_cache():
#     """
#     Load previously generated SQL queries.
#     """

#     if not os.path.exists(CACHE_FILE):
#         return {}

#     try:
#         with open(CACHE_FILE, "r", encoding="utf-8") as file:
#             return json.load(file)

#     except (json.JSONDecodeError, OSError):
#         return {}


# # --------------------------------------------------
# # Save SQL Cache
# # --------------------------------------------------

# def save_cache(cache):
#     """
#     Save generated SQL queries.
#     """

#     with open(CACHE_FILE, "w", encoding="utf-8") as file:

#         json.dump(
#             cache,
#             file,
#             indent=4,
#             ensure_ascii=False
#         )


# # --------------------------------------------------
# # Generate SQL With Cache
# # --------------------------------------------------

# def generate_sql_with_cache(question):
#     """
#     Generate SQL only when it is not already cached.
#     """

#     cache = load_cache()

#     # Use cached SQL if available
#     if question in cache:
#         return cache[question]

#     # Generate new SQL
#     sql = generate_sql(question)

#     # Store it
#     cache[question] = sql

#     save_cache(cache)

#     return sql


# # --------------------------------------------------
# # Compare Query Results
# # --------------------------------------------------

# def compare_results(generated_sql, reference_sql):
#     """
#     Compare the actual database results of the
#     generated SQL and reference SQL.

#     This is more reliable than comparing SQL strings.
#     """

#     try:

#         generated_result = execute_sql(generated_sql)

#         reference_result = execute_sql(reference_sql)

#         generated_columns = generated_result["columns"]
#         reference_columns = reference_result["columns"]

#         generated_rows = generated_result["rows"]
#         reference_rows = reference_result["rows"]

#         return (
#             generated_columns == reference_columns
#             and generated_rows == reference_rows
#         )

#     except Exception as e:

#         print(f"Result comparison failed: {e}")

#         return False


# # --------------------------------------------------
# # Evaluate Single Question
# # --------------------------------------------------

# def evaluate_question(question, reference_sql):
#     """
#     Evaluate one question.
#     """

#     generated_sql = generate_sql_with_cache(question)

#     execution_accuracy = compare_results(
#         generated_sql,
#         reference_sql
#     )

#     return {
#         "question": question,
#         "generated_sql": generated_sql,
#         "reference_sql": reference_sql,
#         "execution_accuracy": execution_accuracy
#     }


# # --------------------------------------------------
# # Evaluate Multiple Questions
# # --------------------------------------------------

# def run_execution_evaluation(test_cases):
#     """
#     Evaluate a list of question/reference-SQL pairs.

#     Expected format:

#     [
#         {
#             "question": "...",
#             "reference_sql": "..."
#         }
#     ]
#     """

#     results = []

#     for test_case in test_cases:

#         result = evaluate_question(
#             question=test_case["question"],
#             reference_sql=test_case["reference_sql"]
#         )

#         results.append(result)

#     return results


# # --------------------------------------------------
# # Calculate Accuracy
# # --------------------------------------------------

# def calculate_execution_accuracy(results):
#     """
#     Calculate overall execution accuracy.
#     """

#     if not results:
#         return 0.0

#     correct = sum(
#         1
#         for result in results
#         if result["execution_accuracy"]
#     )

#     return correct / len(results)

# import json
# import os

# from datasets import Dataset
# from ragas import evaluate
# from ragas.metrics import ContextPrecision, RubricsScore

# from .sql_agent import generate_sql
# from .rag import execute_sql


# # ==================================================
# # SQL Cache
# # ==================================================

# CACHE_FILE = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)),
#     "sql_cache.json"
# )


# def load_cache():
#     if not os.path.exists(CACHE_FILE):
#         return {}

#     try:
#         with open(CACHE_FILE, "r", encoding="utf-8") as file:
#             return json.load(file)
#     except (json.JSONDecodeError, OSError):
#         return {}


# def save_cache(cache):
#     with open(CACHE_FILE, "w", encoding="utf-8") as file:
#         json.dump(cache, file, indent=4, ensure_ascii=False)


# def generate_sql_with_cache(question):
#     cache = load_cache()

#     if question in cache:
#         return cache[question]

#     sql = generate_sql(question)
#     cache[question] = sql
#     save_cache(cache)

#     return sql


# # ==================================================
# # Execution Accuracy
# # ==================================================

# def compare_results(generated_sql, reference_sql):
#     try:
#         generated_result = execute_sql(generated_sql)
#         reference_result = execute_sql(reference_sql)

#         return (
#             generated_result["columns"] == reference_result["columns"]
#             and generated_result["rows"] == reference_result["rows"]
#         )

#     except Exception as e:
#         print(f"Result comparison failed: {e}")
#         return False


# def evaluate_question(question, reference_sql):
#     generated_sql = generate_sql_with_cache(question)

#     accuracy = compare_results(generated_sql, reference_sql)

#     return {
#         "question": question,
#         "generated_sql": generated_sql,
#         "reference_sql": reference_sql,
#         "execution_accuracy": accuracy,
#     }


# def run_execution_evaluation(test_cases):
#     return [
#         evaluate_question(
#             question=case["question"],
#             reference_sql=case["reference_sql"],
#         )
#         for case in test_cases
#     ]


# def calculate_execution_accuracy(results):
#     if not results:
#         return 0.0

#     correct = sum(
#         1 for result in results
#         if result["execution_accuracy"]
#     )

#     return correct / len(results)


# # ==================================================
# # RAGAS Evaluation
# # ==================================================

# def run_ragas_evaluation(test_cases, execution_results):
#     """
#     Evaluate SQL generation with RAGAS.

#     Requires the test cases and execution results to have
#     matching order. The database schema is used as context.
#     """

#     from .sql_agent import get_schema

#     schema_context = get_schema()

#     questions = [case["question"] for case in test_cases]
#     generated_sql = [
#         result["generated_sql"] for result in execution_results
#     ]
#     reference_sql = [case["reference_sql"] for case in test_cases]

#     dataset = Dataset.from_dict({
#         "question": questions,
#         "contexts": [[schema_context] for _ in questions],
#         "answer": generated_sql,
#         "ground_truth": reference_sql,
#     })

#     metrics = [
#         ContextPrecision(),
#         RubricsScore(
#             # name="sql_quality",
#             # definition=(
#             #     "Assess whether the generated SQL answers the question "
#             #     "correctly, uses appropriate tables and columns, and "
#             #     "follows valid SQL logic."
#             # ),
#         ),
#     ]

#     return evaluate(dataset, metrics=metrics)



import json
import os

from .sql_agent import generate_sql, get_schema
from .rag import execute_sql


# ==================================================
# SQL Cache
# ==================================================

CACHE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "sql_cache.json"
)


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=4, ensure_ascii=False)


def generate_sql_with_cache(question):
    cache = load_cache()

    if question in cache:
        return cache[question]

    sql = generate_sql(question)
    cache[question] = sql
    save_cache(cache)

    return sql


# ==================================================
# Execution Accuracy
# ==================================================

def compare_results(generated_sql, reference_sql):
    try:
        generated_result = execute_sql(generated_sql)
        reference_result = execute_sql(reference_sql)

        return (
            generated_result["columns"] == reference_result["columns"]
            and generated_result["rows"] == reference_result["rows"]
        )

    except Exception as e:
        print(f"Result comparison failed: {e}")
        return False


def evaluate_question(question, reference_sql):
    generated_sql = generate_sql_with_cache(question)

    accuracy = compare_results(generated_sql, reference_sql)

    return {
        "question": question,
        "generated_sql": generated_sql,
        "reference_sql": reference_sql,
        "execution_accuracy": accuracy,
    }


def run_execution_evaluation(test_cases):
    return [
        evaluate_question(
            question=case["question"],
            reference_sql=case["reference_sql"],
        )
        for case in test_cases
    ]


def calculate_execution_accuracy(results):
    if not results:
        return 0.0

    correct = sum(
        1 for result in results
        if result["execution_accuracy"]
    )

    return correct / len(results)


# ==================================================
# RAGAS Evaluation
# ==================================================

def run_ragas_evaluation(test_cases, execution_results):
    """
    Run RAGAS using the existing Groq model.

    Execution accuracy remains independent of RAGAS.
    """

    try:
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import ContextPrecision, RubricsScore
        from .llm import groq_llm

        schema_context = get_schema()

        questions = [case["question"] for case in test_cases]
        generated_sql = [
            result["generated_sql"] for result in execution_results
        ]
        reference_sql = [
            case["reference_sql"] for case in test_cases
        ]

        dataset = Dataset.from_dict({
            "question": questions,
            "contexts": [[schema_context] for _ in questions],
            "answer": generated_sql,
            "ground_truth": reference_sql,
        })

        metrics = [
            ContextPrecision(llm=groq_llm),
            RubricsScore(llm=groq_llm),
        ]

        return evaluate(dataset, metrics=metrics)

    except Exception as e:
        raise RuntimeError(
            f"RAGAS evaluation failed: {e}"
        ) from e
