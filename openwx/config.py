from importlib.util import module_from_spec

"""
getattr(obj, "attribute)
Get a named attribute from an object. AttributeError
eg:
class A(object):
    bar=1

a = A()
getattr(a, 'bar'）


http://www.cnblogs.com/pylemon/archive/2011/06/09/2076862.html

compile(source, filename, model[, flags[, dont_inherit]])
source -- 字符串或者AST（Abstract Syntax Trees）对象。。
filename -- 代码文件名称，如果不是从文件读取代码则传递一些可辨认的值。
mode -- 指定编译代码的种类。可以指定为 exec, eval, single。
flags -- 变量作用域，局部命名空间，如果被提供，可以是任何映射对象。。
flags和dont_inherit是用来控制编译源码时的标志

eg：
str = "for i in range(0, 10): print(i)"
c = compile(str, '', 'exec')
exec(c)

exec 执行存储在字符串或文件中的 python 语句
1. string
2. file obj
3. 代码对象
4. tuple
exec 等同于 if， while 等
exec(expr, globals, locals) 等效于 exec expr in globals, locals
http://www.mojidong.com/python/2013/05/10/python-exec-eval/
使用exec的时候应该总是记得，详细制定其执行的作用域
eg:
m_dic={'a':8, 'b':9}
exec("print(a, b)", m_dic)

"""
class ConfigAttribute(object):
    """
    让一个属性指向一个配置
    """

    def __init__(self, name):
        self.__name__ = name

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    """
    在一个 python 文件中读取配置

    """

    def from_pyfile(self, filename):
        # Return a new empty module object called name.
        d = module_from_spec('config')
        d.__file__ = filename
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        self.from_object(d)
        return True

    def from_object(self, obj):
        # dir 返回参数的属性，方法列表; 没有参数则返回当前域中的属性，方法列表
        for key in dir(obj):
            if key.isupper():  # 大写检查
                self[key] = getattr(obj, key)
                # obj 是上一步 new 的 module
