"""
http://blog.jobbole.com/21351/
自定义 metaclass 需要继承 type 对象
'type' 实际上是一个类，就像 'str' 和 'int' 一样


虚拟子类， 通过 register() 注册，
直接抽象子类需要完全覆写抽象基类中的抽象内容后，才能被实例化

元类（metaclass) 为了当创建类时能够动态的改变类
1. 拦截类的创建
2. 修改类
3. 返回修改后的类
典型用例 django 中 Model 的创建
class Person(models.Model):
    ...
models.Model 定义了 __metaclass__, 可以将刚定义的简单 Person 类转变成对数据库
的一个复杂 hook.

对于简单的类， 也可以不使用元类对类进行修改：
1. Monkey patching
2. class decorators
"""

# 自定义元类（metaclass)

class RobotMetalClass(type):
    TYPES = {}
    # http://www.cnblogs.com/ifantastic/p/3175735.html
    # __new__ 是在 __init__ 之前被调用的特殊方法
    # __new__ 是用来创建对象并返回的方法
    # __init__ 只是用来将传入的参数初始化给对象
    # 除非希望控制对象的创建，否则很少用到 __new__
    # __new__ 创建的对象是类，我们希望改写它

    def __new__(mcs, name, bases, attrs):
        # 如果要得到当前的实例，需要调用父类 (type) 中的 __new__
        # 不可调用自己 造成死循环
        # 使用没有继承关系的 __new__ 也是安全的
        return type.__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if '__type__' in attrs:
            if isinstance(attrs['__type__'], list):
                for _type in attrs['__type__']:
                    cls.TYPES[_type] = cls
            else:
                cls.TYPES[attrs['__type__']] = cls
        type.__init__(cls, name, bases, attrs)


"""
type  和 object 的区别：
object 是所有对象的基类，type 也继承自 object
type 是一切 type 的类型， object 的 type 是 type
可以去掉 type ， 只是没有一个东西可以标识它的类型。
但不能去掉 object

__new__ 决定是否调用 __init__, 也可以返回其他类的实例

"""