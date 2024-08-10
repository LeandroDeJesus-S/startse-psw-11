from typing import Any


def cast(value: Any, type_class: object) -> Any:
    """converts a value to the given class inside a try ... except block
    and return None if it raises an exception
    
    Args:
        value (Any): some value to be converted
        type_class (object): the target class to cast the value
    
    Example:
    >>> x = cast('12', type_class=int)
    >>> x
    >>> 12
    >>> cast(x, float)
    >>> 12.0
    >>> cast(x, list)  # TypeError: 'int' object is not iterable
    >>> None
    """
    try:
        value = type_class(value)
        return value
    except Exception:
        return
