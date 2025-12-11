import os
import sqlite3
import pandas as pd
import logging
import subprocess
import datetime
from typing import Optional, Union

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

def get_last_backup_timestamp(backup_dir: str) -> Optional[str]:
    """
    Gets the timestamp from the last backup file in a directory.
    Backup format: YYYY-MM-DD-HH-MM-SS.sql
    Returns timestamp string without extension or None.
    """
    try:
        backups = [f for f in os.listdir(backup_dir) if f not in ('.', '..')]
    except Exception:
        return None
        
    if not backups:
        return None
    
    # Filter for valid backup files
    valid_backups = []
    for f in backups:
        if f.endswith(".sql"):
            try:
                # Validate format roughly
                parts = f.replace(".sql", "").split("-")
                if len(parts) == 6:
                    valid_backups.append(f)
            except:
                pass
                
    if not valid_backups:
        return None
        
    valid_backups.sort()
    last_backup = valid_backups[-1]
    
    # Return filename without extension
    return last_backup.replace(".sql", "")

def backup_database(backup_dir: str, database_file: str) -> str:
    """Backs up the database to a SQL file."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    backup_file = os.path.join(backup_dir, f"{current_datetime}.sql")
    
    command = f"sqlite3 '{database_file}' .dump > '{backup_file}'"
    
    try:
        subprocess.check_call(command, shell=True)
        logging.info(f"Database backed up to {backup_file}")
        return "success"
    except subprocess.CalledProcessError as e:
        logging.error(f"Backup failed: {e}")
        return "failure"

def load_backup_into_db(backup_path: str, database_file: str) -> str:
    """Loads a SQL backup into a database file."""
    
    # Remove existing database file if it exists
    if os.path.exists(database_file):
        try:
            os.remove(database_file)
        except OSError as e:
            print(f"Failed to remove existing database: {e}")
            return "failure"
    
    # Load backup
    command = f"sqlite3 {database_file} < {backup_path}"
    
    try:
        subprocess.check_call(command, shell=True)
        return "success"
    except subprocess.CalledProcessError as e:
        print(f"Failed to load backup: {e}")
        return "failure"
