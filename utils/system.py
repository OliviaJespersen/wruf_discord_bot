from functools import wraps
import inspect
from datetime import datetime
import asyncio

from config import ICON_SET
import utils

_dynamic_indent = 0

def reset_dynamic_indent():
    """
    Resets the dynamic indentation level to its initial value.
    """
    global _dynamic_indent
    _dynamic_indent = 0

def _pre_log(name: str) -> None:
    """
    Logs the function name and its arguments before the function is called.

    Parameters:
        name (str): The name of the function.
        args (tuple): The arguments passed to the function.
        kwargs (dict): The keyword arguments passed to the function.
    """
    global _dynamic_indent 
        
    _dynamic_indent += 1

    log(2, f"{name}, was called", _dynamic_indent)

def _post_log(name: str) -> None:
    """
    Logs the function name and its results after the function is called.

    Parameters:
        name (str): The name of the function.
        results (any): The results returned by the function.
    """
    global _dynamic_indent 

    log(0, f"{name}, returned", _dynamic_indent)

    _dynamic_indent -= 1

def _sync_log_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _pre_log(func.__name__)
        result = func(*args, **kwargs)
        _post_log(func.__name__)
        return result
    return wrapper

def _async_log_wrapper(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await asyncio.sleep(0) # Yield control to the event loop
        _pre_log(func.__name__)
        result = await func(*args, **kwargs)
        _post_log(func.__name__)
        return result
    return wrapper

def log(code: int, message: str, indent: int = 0) -> None:
    """
    Logs a message with a corresponding icon and timestamp.

    Parameters:
        code (int): The status code indicating the type of log.
            - 0: Success
            - 1: Failure
            - 2: Loading
            - 3: Error
        message (str): The message to log.
        indent (int, optional): The indentation level for the log message. Defaults to 0.
    """
    match code:
        case 0:
            icon = ICON_SET[0]
        case 1:
            icon = ICON_SET[1]
        case 2:
            icon = ICON_SET[2]
        case 3:
            icon = ICON_SET[3]

    print(f"{time()} | {"    " * indent}{icon} {message}")

def time() -> str:
    """
    Returns the current time formatted as HH:MM:SS.

    Returns:
        str: The current time in HH:MM:SS format.
    """
    return datetime.now().strftime("%H:%M:%S")

def log_all_utils() -> None:
    """
    Logs all functions in the utils module.
    """
    modules = [
        utils.analyzer,
        utils.database,
        utils.gemini,
        utils.image,
        utils.layout
    ]

    for module in modules:
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if inspect.isfunction(attr):
                if inspect.iscoroutinefunction(attr):
                    setattr(module, attr_name, _async_log_wrapper(attr))
                else:
                    setattr(module, attr_name, _sync_log_wrapper(attr))
