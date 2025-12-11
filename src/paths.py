import os

def go_back_dir(path: str, number: int) -> str:
    """
    Goes back 'number' of directories from the given path.
    """
    if os.path.isfile(path):
        path = os.path.dirname(path)
    
    result = path
    for i in range(number):
        result = os.path.dirname(result)
    return result
