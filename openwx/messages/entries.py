from openwx.utils import to_text

"""
__dict__ 分层存储属性，子类不重复存储父类中的属性，
字典 键为属性名

https://my.oschina.net/mickelfeng/blog/906164

https://www.ibm.com/developerworks/cn/opensource/os-pythondescriptors/index.html

descriptor，实现描述符协议， 即__get__（只实现这个，非数据描述符）,
__set__（同时实现这个，数据描述符，属性可读写）, 和 __delete__， 并且
该类的实例对象通常是另一个类的类属性（有别于实例属性）
初衷，添加额外的类型检查逻辑代码
是一种创建托管属性的方法，保护属性不被修改，属性类型检查，自动更新某个依赖属性的值
类属性（父类，祖先）
数据描述符
实例的属性
非数据描述符
即时生成属性 __getattr__

创建属性描述符：
类方法创建：__get__ , __set__, __del__
属性类型创建：property(fget, fset, fdel, doc) 依赖某个属性的其他属性即时变化
属性修饰符创建：@property @property.setter @property.deleter
"""
# 静态语言也不需要这么麻烦

def get_value(instance, path, default=None):
    dic = instance.__dict__
    for entry in path.split('.'):
        dic = dic.get(entry)
        if dic is None:
            return default
    return dic or default


class BaseEntry(object):
    def __init__(self, entry, default=None):
        self.entry = entry
        self.default = default


class IntEntry(BaseEntry):
    def __get__(self, instance, owner):
        try:
            return int(get_value(instance, self.entry, self.default))
        except TypeError:
            return


class FloatEntry(BaseEntry):
    def __get__(self, instance, owner):
        try:
            return float(get_value(instance, self.entry, self.default))
        except TypeError:
            return


class StringEntry(BaseEntry):
    def __get__(self, instance, owner):
        v = get_value(instance, self.entry, self.default)
        if v is not None:
            return to_text(v)
        return v