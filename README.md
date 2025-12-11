# py-utils

My python utilities library.

## Structure

The utilities are organized into independent modules in `src/`:

- `database.py`: SQLite database operations and backups.
- `files.py`: File I/O for Text, JSON, YAML, and Delimited files.
- `paths.py`: Path manipulation utilities.
- `log_utils.py`: Logging configuration.
- `common.py`: Common utilities.

## Usage

Add `src` to your PYTHONPATH.

```python
import files
import database

data = files.read_json("data.json")
df = database.local_query("db.sqlite", "SELECT * FROM table")
```
