"""

https://realpython.com/blog/python/inner-functions-what-are-they-good-for/

嵌套函数：
1. encapsulation
变量作用域的隐藏
所有参数检测都放在外部函数中，内部函数更专注于逻辑

2. keepin'it DRY
不同初始途径，相同处理方法，其实也是将路径的判断放在外部函数中，归一入口

3. closures and factory functions
When it comes to closure, that is not the case: You must utilize nested functions.
A closure simply causes the inner function to remember the state of its environment when called.

"""

def outer(num1):
    print("outer {} ".format(num1))
    def inner_increment(num1): # hidden from outer code
        print("inner {}".format(num1 + 1))
        return num1 + 1
    num2 = inner_increment(num1)
    print(num1, num2)


def factorial(number):
    if not isinstance(number, int):
        raise TypeError("sorry. number must be an integer")
    if not number >= 0:
        raise ValueError("sorry. number must be zero or positive")
    print("call factorial.")

    def inner_factorial(number):
        print("call inner_factorial.")
        if number <= 1:
            print("inner_factorial {} ".format(number))
            return 1
        print("inner_factorial {} ".format(number))
        return number * inner_factorial(number-1)
    return inner_factorial(number)


# 统计 NewYork City 有多少 WiFi hot spots 并且那个行政区最多.
# Accept either an open file object or a file name
def process(file_name):
    def do_stuff(file_process):
        wifi_locations = {}

        for line in file_process:
            values = line.split(',')
            # values[1] 对应的是行政区行（borough)
            wifi_locations[values[1]] = wifi_locations.get(values[1], 0) + 1
        max_key = 0
        for name, key in wifi_locations.items():
            all_locations = sum(wifi_locations.values())
            if key > max_key:
                max_key = key
                business = name
        print('There are {0} WiFi hot spots in NYC and {1} has the most with {2}.'.format(
            all_locations, business, max_key
        ))

    if isinstance(file_name, str):
        print("file name")
        with open(file_name, 'r') as f:
            do_stuff(f)
    else:
        print("file object")
        do_stuff(file_name)

# 惰性赋值
# def generate_power(number):
#     print("outer number {}".format(number))
#
#     def nth_power(power):
#         print("inner power {}".format(power))
#         return number ** power
#
#     return nth_power

"""
检查某些用户是否拥有访问某些页面的权限
也可以套着模板改为抓取用户 session 来检查是否有资格访问某些路由
也可以将简单的字符串相等判断改为查询数据库，检查权限，然后根据相应的资格返回正确的 view
"""
def has_permission(page):
    def inner(username):
        if username == 'Admin':
            return "'{0}' does have access to {1}.".format(username, page)
        else:
            return "'{0}' does NOT have access to {1}.".format(username, page)
    return inner



"""
使用 inner functions 来实现 闭包(closures) 和工厂方法（decorator)
含有参数的装饰器因为有闭包的特征，所以使用嵌套函数来实现很合适
"""
def generate_power(exponent):
    print("generate_power {}".format(exponent))

    def decorator(f):
        print("decorator {}".format(exponent))

        def inner(*args):
            result = f(*args)
            print("result {}".format(result))
            return  exponent**result

        print("return inner {}".format(inner))
        return inner

    print("return decorator {}".format(decorator))
    return decorator

@generate_power(2)
def raise_two(n):
    print("raise two {} ".format(n))
    return n
@generate_power(3)
def raise_three(n):
    print("raise three {} ".format(n))
    return n

if __name__ == '__main__':

    outer(10)
    print(factorial(4))

    file_name = "/Users/alpha/Downloads/NYC_Wi-Fi_Hotspot_Locations.csv"
    with open(file_name, 'r') as f:
        process(f)
    # process(file_name)

    # raise_two = generate_power(2)
    # raise_three = generate_power(3)

    print(raise_two(2))
    print(raise_three(2))

    current_user = has_permission('Admin Area')
    print(current_user('Admin'))
    random_user = has_permission('Admin Area')
    print(random_user('Not Admin'))


