"""Utils module."""
import re
import inspect


def schema(schema):
    """Decorator.

    check if arguments of function are correct.
    """
    def decorator(func):
        def _schema(*args, **kwargs):
            func_arg_names = inspect.getargspec(func).args
            num_args = len(args)
            for key, val in schema.items():
                index = func_arg_names.index(key)
                code = 0
                if key in kwargs:
                    code = check_schema(kwargs[key], val)

                elif key in func_arg_names and index < num_args:
                    code = check_schema(args[index], val)

                if code == 1:
                    raise Exception("Schema error")

                elif code == 2:
                    raise TypeError("Type error in variable {}".format(key))

                elif code == 3:
                    raise ValueError("Value of {} dont match with pattern".format(key))

            return func(*args, **kwargs)
        return _schema
    return decorator


def check_schema(val, schema):
    """Match a schema."""
    if 'type' not in schema:
        return 1

    is_require = 'required' in schema and schema['required']

    if not isinstance(val, schema['type']) and (val is not None or is_require):
        return 2

    if isinstance(val, str) and 'pattern' in schema and \
       not re.match(schema['pattern'], val):
        return 3

    return 0
