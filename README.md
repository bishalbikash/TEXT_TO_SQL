GenAI Data Analyst — Natural Language to SQL

An AI-powered data analytics application that allows users to query a MySQL database using natural language. The application converts questions into SQL queries using Large Language Models (LLMs), executes the queries, and presents the results through a web-based chat interface.

🚀 Features

Natural Language to SQL: Convert plain-English questions into SQL queries.

LLM Integration: Uses Google Gemini with Groq as a fallback model.

MySQL Integration: Connects to a MySQL database and retrieves data dynamically.

Interactive Web Interface: Ask questions and view query results through a chat interface.

SQL Generation and Execution: Generates and executes read-only SELECT queries.

SQL Evaluation: Compares generated query results against reference SQL results.

RAGAS Evaluation: Evaluates the system using Context Precision and domain-specific rubric scoring.

SQL Caching: Caches generated SQL queries to reduce repeated LLM calls during evaluation.

🛠️ Tech Stack

Language: Python

Backend: Flask

Frontend: HTML, CSS, JavaScript

Database: MySQL

LLMs: Google Gemini, Groq

AI Framework: LangChain

Evaluation: RAGAS

Other Tools: SQLAlchemy, python-dotenv

🏗️ How It Works

The user enters a natural-language question in the web interface.

The backend retrieves database schema information.

The LLM generates an SQL query based on the question and schema.

The application validates that the generated query is a SELECT query.

The SQL query executes against the MySQL database.

The application returns the generated SQL and query results to the interface.

An evaluation script measures execution accuracy and runs RAGAS evaluation metrics.

📂 Project Structure

genai-data-analyst/
├── backend/
│   ├── database.py
│   ├── llm.py
│   ├── sql_agent.py
│   ├── rag.py
│   ├── evaluation.py
│   └── test_cases.py
├── documents/
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── app.py
├── run_evaluation.py
├── sql_cache.json
├── requirements.txt
├── .env
├── .gitignore
└── README.md

⚙️ Installation and Setup

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/genai-data-analyst.git
cd genai-data-analyst

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root:

DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_database_name

GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key

Replace the example values with your own database credentials and API keys. Never commit your .env file to GitHub.

5. Start the application

python app.py

Open the local URL printed by Flask in your browser, typically:

http://127.0.0.1:5000

📊 Evaluation

The project includes a test suite with predefined natural-language questions and reference SQL queries.

Results from the current test run:

Metric

Result

SQL execution accuracy

100% on the current test set

RAGAS Context Precision

1.00

RAGAS domain-specific rubric score

5.00

Note: These are results from the current test run, not a guarantee of performance on unseen questions. Some RAGAS requests encountered API rate limits, so evaluation reliability should be verified with a successful rerun.

Run the evaluation script:

python run_evaluation.py

🔒 Security Notes

Keep API keys and database credentials in environment variables.

Do not commit .env or other files containing secrets.

Use a database account with read-only permissions where possible.

Validate generated SQL and restrict database access appropriately before deployment.

🎯 Project Objective

The goal of this project is to make database analytics more accessible by allowing users to retrieve insights using natural language instead of manually writing SQL queries.

It demonstrates practical skills in Python, SQL, LLM integration, backend development, database connectivity, and AI evaluation.

👨‍💻 Author

Your Name

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://www.linkedin.com/in/YOUR_LINKEDIN_PROFILE/
