from sqlalchemy import text

# from database import engine
# from sql_agent import generate_sql
from .database import engine
from .sql_agent import generate_sql


# --------------------------------------------------
# Validate SQL
# --------------------------------------------------

def is_safe_sql(sql):
    """
    Allow only SELECT queries.
    """

    if not sql:
        return False

    cleaned_sql = sql.strip().lower()

    return cleaned_sql.startswith("select")


# --------------------------------------------------
# Execute SQL
# --------------------------------------------------

def execute_sql(sql):
    """
    Execute a generated SELECT query
    and return columns and rows.
    """

    if not is_safe_sql(sql):
        raise ValueError("Only SELECT queries are allowed.")

    try:
        with engine.connect() as connection:

            result = connection.execute(text(sql))

            columns = list(result.keys())

            rows = [
                list(row)
                for row in result.fetchall()
            ]

        return {
            "columns": columns,
            "rows": rows
        }

    except Exception as e:
        raise RuntimeError(
            f"Database query failed: {str(e)}"
        )


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

def ask_question(question):
    """
    Complete chatbot pipeline:

    User question
        ↓
    Generate SQL
        ↓
    Execute SQL
        ↓
    Return result
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Generate SQL using Gemini/Groq
    sql = generate_sql(question)

    # Execute SQL against MySQL
    result = execute_sql(sql)

    return {
        "question": question,
        "sql": sql,
        "columns": result["columns"],
        "rows": result["rows"]
    }