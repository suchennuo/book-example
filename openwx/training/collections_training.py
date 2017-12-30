
# ttp://www.zlovezl.cn/articles/collections-in-python/
# https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001411031239400f7181f65f33a4623bc42276a605debf6000
from collections import namedtuple, OrderedDict

"""
namedtuple
有这样一个数据结构，每个对象是拥有三个元素的 tuple
使用 namedtuple 可以生成可读性更高的数据结构
成员函数：
https://blog.stdioa.com/2015/10/learning-python-collections/#22
_make(iterable) 讲一个可迭代对象转化为一个 namedtuple 对象


"""

def namedtuple_training():
    websites = [
        ('Sohu', 'http://www.sohu.com', '张朝阳'),
        ('Sina', 'http://www.sing.com', '王志东')
    ]

    easy_read_website = namedtuple('easy_read_websites', ['name', 'url', 'founder'])

    for site in websites:
        print(site)
        site = easy_read_website._make(site)
        print(site)

"""
orderedDict
dict 由于 hash 的特性，是无序的。
orderedDict 的 key 会按照插入的顺序排序，而不是 key 本身排序

"""

def orderedDict_training():
    items = (('A', 1), ('B', 2), ('C', 3))

    regular_dict = dict(items)
    ordered_dict = OrderedDict(items)
    print("regular dict: ")
    for k, v in regular_dict.items():
        print(k, v)

    print("ordered dict:")
    for k, v in ordered_dict.items():
        print(k, v)




if __name__ == '__main__':
    namedtuple_training()
    print()
    orderedDict_training()

