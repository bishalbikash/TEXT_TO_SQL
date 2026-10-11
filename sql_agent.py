import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# from database import db
# from llm import sql_llm
from .database import db
from .llm import sql_llm


# --------------------------------------------------
# SQL Prompt
# --------------------------------------------------

template = """
Based on the table schema below, write a MySQL query
that would answer the user's question.

Rules:
1. Only provide the SQL query.
2. Do not provide explanations.
3. Do not use markdown.
4. Return the SQL query in a single line.
5. Only generate SELECT queries.

Table Schema:
{schema}

Question:
{question}

SQL Query:
"""


prompt = ChatPromptTemplate.from_template(template)


# --------------------------------------------------
# Get database schema
# --------------------------------------------------

def get_schema():
    """
    Get the current database schema.
    """

    return db.get_table_info()


# --------------------------------------------------
# SQL Chain
# --------------------------------------------------

sql_chain = (
    RunnablePassthrough.assign(
        schema=lambda _: get_schema()
    )
    | prompt
    | sql_llm
    | StrOutputParser()
)


# --------------------------------------------------
# Clean generated SQL
# --------------------------------------------------

def clean_sql(text):
    """
    Remove markdown SQL fences if the LLM returns them.
    """

    match = re.search(
        r"```sql\s*(.*?)\s*```",
        text,
        re.DOTALL | re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return (
        text
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )


# --------------------------------------------------
# Generate SQL
# --------------------------------------------------

def generate_sql(question):
    """
    Convert a natural-language question into SQL.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    response = sql_chain.invoke({
        "question": question.strip()
    })

    sql = clean_sql(response)

    # Basic safety check
    if not sql.lower().lstrip().startswith("select"):
        raise ValueError(
            "Generated query is not a SELECT statement."
        )

    return sql