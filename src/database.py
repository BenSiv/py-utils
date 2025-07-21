from typing import Optional, Union
import pandas as pd
import sqlite3


def local_query(db_path: str, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Executes a SELECT query and returns the results as a pandas DataFrame.

    Args:
        db_path (str): Path to the SQLite database file.
        query (str): SQL SELECT query.
        params (tuple, optional): Parameters to safely pass with the query.

    Returns:
        pd.DataFrame: Query results as a DataFrame. Returns empty DataFrame on error.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query(query, conn, params=params)
    except sqlite3.Error as e:
        print(f"SQLite error during query: {e}")
        return pd.DataFrame()


def local_update(db_path: str, sql_statement: str) -> bool:
    """
    Executes a single SQL statement (INSERT, UPDATE, DELETE, or DDL) against the SQLite database.

    Args:
        db_path (str): Path to the SQLite database file.
        sql_statement (str): SQL statement to execute.

    Returns:
        bool: True if the operation succeeded, False otherwise.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(sql_statement)
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"SQLite error during update: {e}")
        return False


def load_dataframe(db_path: str, table_name: str, df: pd.DataFrame, if_exists: str = "replace", index: bool = False) -> bool:
    """
    Loads a pandas DataFrame into an SQLite table.

    Args:
        db_path (str): Path to the SQLite database.
        table_name (str): Table name to write into.
        df (pd.DataFrame): DataFrame to load.
        if_exists (str): What to do if table exists: 'replace', 'append', 'fail'.
        index (bool): Whether to write DataFrame index as a column.

    Returns:
        bool: True if write succeeded, False otherwise.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists=if_exists, index=index)
        return True
    except Exception as e:
        print(f"Failed to load DataFrame into table '{table_name}': {e}")
        return False
