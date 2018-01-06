
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


"""
关于字典的操作（创建 dict , 字典推导，设置默认值，pop方法, ）
http://blog.csdn.net/yelyyely/article/details/40404217

http://www.revotu.com/difference-dict-keys-values-items-between-python2-and-python3.html
"""
def opration_dict():
    # 参数赋值
    d = dict(a=1, b=2)
    print(d)
    # 可用迭代对象为参数且每一个迭代对象为（k, v) 对
    l1 = ['a', 'b', 'c']
    l2 = [1, 2, 3]
    # zip(l1, l2) = [('a', 1), ('b', 2)]
    d2 = dict(zip(l1, l2))
    print(d2)
    # 字典推导
    d3 = { c:ord(c) for c in 'abc'}
    print(d3)
    # 设置默认值
    l = ['a', 'b', 'c']
    d4 = {}
    print(d4.fromkeys(l, 0))
    # 使用 defaultdict
    from collections import defaultdict
    s = "hello, world."
    d5 = defaultdict(int)
    for c in s: d5[c] += 1
    print(d5)
    # 使用setdefault 同时设置默认值和取值
    d6 = {}
    for c in s: d6[c] = d6.setdefault(c, 0) + 1
    print(d6)
    # pop 取出并删除
    d6['is_mine'] = True
    if (d6.pop('is_mine', False)):
        print("is mine")
    else:
        print("is not mine")
    # 遍历 。 keys values, items, python3 中相当于 python2 中的 view 系列方法
    keys = d6.keys()
    print(keys)
    print(d6.values())
    print(d6.items())
    del d6['h']
    print(d6)


if __name__ == '__main__':
    namedtuple_training()
    print()
    orderedDict_training()
    opration_dict()


