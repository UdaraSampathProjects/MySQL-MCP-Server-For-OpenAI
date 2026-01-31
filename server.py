# import os
# import mysql.connector
# from mcp.server.fastmcp import FastMCP
# from dotenv import load_dotenv

# load_dotenv()

# mcp = FastMCP("MySQL-Server")

# def get_db_connection():
#     return mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST_KAYVE"),
#         user=os.getenv("MYSQL_USER_KAYVE"),
#         password=os.getenv("MYSQL_PASSWORD_KAYVE"),
#         database=os.getenv("MYSQL_DATABASE_KAYVE")
#     )

# @mcp.tool()
# def list_tables() -> str:
#     """List all tables available in the current database."""
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SHOW TABLES")
#         tables = [row[0] for row in cursor.fetchall()]
#         conn.close()
#         return f"Tables: {', '.join(tables)}"
#     except Exception as e:
#         return f"Error: {e}"

# @mcp.tool()
# def run_query(sql: str) -> str:
#     """Execute a read-only SELECT query."""
#     if not sql.lower().strip().startswith(("select", "show", "describe")):
#         return "Error: Only read-only queries are permitted."
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(sql)
#         results = cursor.fetchmany(size=50) # Limit results for safety
#         conn.close()
#         return str(results) if results else "No rows returned."
#     except Exception as e:
#         return f"Database Error: {str(e)}"

# if __name__ == "__main__":
#     mcp.run()

import os
import mysql.connector
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("MySQL-Server")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST_KAYVE"),
        user=os.getenv("MYSQL_USER_KAYVE"),
        password=os.getenv("MYSQL_PASSWORD_KAYVE"),
        database=os.getenv("MYSQL_DATABASE_KAYVE"),
        port=int(os.getenv("MYSQL_PORT_KAYVE", 3306))
    )

@mcp.tool()
def list_tables() -> str:
    """Lists all tables available in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return f"Tables: {', '.join(tables)}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def run_query(sql: str) -> str:
    """Execute a custom read-only SELECT query."""
    # Safety check to ensure only SELECT queries are run
    if not sql.lower().strip().startswith("select"):
        return "Error: Only SELECT queries are permitted."
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return str(results) if results else "No data found for this query."
    except Exception as e:
        return f"Database Error: {e}"

if __name__ == "__main__":
    mcp.run()