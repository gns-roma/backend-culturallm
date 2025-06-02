import mariadb
from fastapi import HTTPException

def db_connection():
    """Return a connection to the database, and close it when done"""
    conn = mariadb.connect(
        host="culturallm-db",
        port=3306,
        user="user",
        password="userpassword",
        database="culturallm_db"
    )
    try:
        yield conn
    finally:
        conn.close()


def execute_query(connection: mariadb.Connection, query: str, params: tuple = (), fetch: bool = True):
    """Execute a query and return the results if there are"""
    try:
        cursor: mariadb.Cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall() if fetch else None
        connection.commit()
        cursor.close()
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Errore nell'esecuzione della query: {e}")
    return results

