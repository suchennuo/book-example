"""
该训练主要为了简单的参数类型检查的装饰器

python 中的 inspect 模块
https://docs.python.org/3/library/inspect.html
1. 类型检查
2. 获取源码
3. 获取类或函数的参数信息
4. 解析堆栈
场景：
写框架的时候需要通过某种机制访问未知的属性，类似于反射

获取到的字段不能直接赋值，获取到的是指向同一个地方的引用， 赋值只能改变当前引用而已

inspect 模块封装了很多检查类型的方法，比 type 模块更轻松

dir(obj) #获取属性名，以列表形式返回
hasattr(obj, attribute)
setattr(obj, attribute)
getattr(obj, attribute)

signature(callable, *, follow_wrapped=True)
return a signature object for the given callable
parameters
An ordered mapping of parameters' names to the corresponding parameter objects
eg:
mappingproxy(OrderedDict([('x', <Parameter "x:int">), ('y', <Parameter "y:str='haha'">)]))
params.keys()
eg:
odict_keys(['x', 'y'])

tuple(seq) 将列表转化为元祖
eg:
('x', 'y')

enumerate()将一个可遍历的数据对象组合为一个索引序列， 同时列出数据和数据下标， 一般for
['spring', 'summer', 'fall', 'winter']
to
[(0, 'spring'), (1, 'summer'), (2, 'fall'), (3, 'winter')]

http://www.cnblogs.com/fengmk2/archive/2008/04/21/1163766.html
dict.items() 字典函数以列表返回可遍历的 tuple list



函数注解
https://mozillazg.github.io/2016/01/python-function-argument-type-check-base-on-function-annotations.html
inspect  类型检查

format()
http://kuanghy.github.io/2016/11/25/python-str-format
http://www.cnblogs.com/shaosks/p/5737089.html
replacement_field ::= "{" [field_name] ["!" conversion] [":" format_spec] "}"
指定转化
conversion ::= "r" | "s" | "a"
"!r" 对应 repr() 函数得到的字符串通常可以用来重新获得该对象，通常情况下 obj==eval(repr(obj)) 这个等式是成立的
"!s" 对应 str()函数得到的字符串可读性好
"!a" 对应 ascii()
eg:
a = 'hello, world.'
a == eval(repr(a)) #true


一下是 python 中 collections module 中一些数据类型
namedtuple()
创建类似于 tuple 的数据类型，除了能用索引来访问数据，也可以通过属性名来访问

有序字典（OrderedDict)
http://www.zlovezl.cn/articles/collections-in-python/


"""

import collections
import functools
import inspect


def check(func):
    msg = ('Expected type {expected!r} for argument {argument}, '
           'but got type {got!r} with value {value!r}')

    # 获得函数定义的参数
    sig = inspect.signature(func)
    parameters = sig.parameters # 参数有序字典
    arg_keys = tuple(parameters.keys()) # 参数名称

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        CheckItem = collections.namedtuple('CheckItem', ('anno', 'arg_name', 'value'))
        check_list = []

        # collect args *args 传入的参数以及对应的函数参数注解
        # *args 表任意多个无名参数
        for i, value in enumerate(args):
            arg_name = arg_keys[i]
            anno = parameters[arg_name].annotation  # eg: <class 'int'>
            check_list.append(CheckItem(anno, arg_name, value))

        # collect kwargs **kwargs 传入的参数以及对应的函数参数注解
        # **kwargs 表关键字参数，是一个 dict
        for arg_name, value in kwargs.items():
            anno = parameters[arg_name].annotation
            check_list.append(CheckItem(anno, arg_name, value))

        # check type
        for item in check_list:
            if not isinstance(item.value, item.anno):  # 判断 value 是否是声明的类型
                error = msg.format(expected=item.anno, argument=item.arg_name,
                                   got=type(item.value), value=item.value)
                raise TypeError(error)
        return func(*args, **kwargs)
    return wrapper


@check
def foobar(a: int, b: str, c: float = 3.2) -> tuple:
    return a, b, c


if __name__ == '__main__':
    foobar(1, 'b')
    foobar(1, 'b', 3.5)
    foobar('a', 'b')
