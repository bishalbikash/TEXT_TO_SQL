
# ==================================================
# SQL Evaluation Test Cases
# ==================================================

TEST_CASES = [
    {
        "question": "What was the budget of Product 12?",
        "reference_sql": "SELECT `2017_Budgets` FROM `2017_budgets` WHERE `Product_Name` = 'Product 12';"
    },
    {
        "question": "What are the names of all products in the products table.",
        "reference_sql": "SELECT Product_Name FROM products;"
    },
    {
        "question": "List all customer names from the customers table.",
        "reference_sql": "SELECT Customer_Names FROM customers;"
    },
    {
        "question": "Find the name and state of all regions in the regions table.",
        "reference_sql": "SELECT name, state FROM regions;"
    },
    {
        "question": "What is the name of the customer with Customer Index = 1.",
        "reference_sql": "SELECT Customer_Names FROM customers WHERE Customer_Index = 1;"
    },
    
    
]
