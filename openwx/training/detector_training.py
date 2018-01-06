"""
内置装饰器： @staticmathod, @classmethod, @property
@wraps 可以保留原函数的信息
"""

from functools import wraps

# 简单的装饰器
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called.")
        return func(*args, **kwargs)
    return with_logging

# 带参数的装饰器
def use_logged(level):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if level == "warn":
                print(func.__name__ + " was called.")
            print("return func")
            return func(*args, **kwargs)
        print("return wrapper")
    print("return decorator")
    return decorator


# @use_logged(level="warn")
def f(x):
    return print(x + x*x)

if __name__ == '__main__':
    f(10)
    print(f.__name__)
    # wf = logged(f, level="warn")
    # wf(10)
