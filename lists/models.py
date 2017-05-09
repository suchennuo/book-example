from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class List(models.Model):
    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        unique_together = ('list', 'text')


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

"""
Model 的建立
    1. 继承 models.Model.
    2. 一个 modal 对应一张 table
    3. CharField , DecimalField, BooleanField ...
    4. ForeignKey()
    5. python3 manage.py check (预期：0 erros found)
    6. python3 manage.py sqlmigrate restaurants 000x (model 翻译成 sql 的结果）
    7. python3 manage.py makemigrations lists( APP_NAME )
    8. migration 文档 001...
    9. migration 文档主要有一个继承自 Migration 的class构成， 里面包含 dependencies 和
    operations 两个list:
        dependencies 表述了 migration 档案是基于哪一个 migration
        operations 表述在基础上再进行了哪些改动
    10. python3 manage.py migrate APP_NAME 000x  (建立 table)
        若不指定 APP_NAME 会对所有 APP 进行改动， 若不指定版本号，则更新到最新
    11. TABLE(key='value', ...), TABLE.save() 写入数据
    12. TABLE.object.create(key='value', ...) 等价于 11
    13. __unicode__
    14. table = TABLE.object.all() 等价于 select * from table; 返回 QuerySet
    15. cursor = table[0], cursor.phone_number ， 显示第一栏及其某个属性
    16. cursor = TABLE.object.get( name = 'wanted') 条件查询
    17. table [ 0 : 2]  查询集合 slicing 操作
    18. TABLE.object.filter(name='name')  or (name_contains='name') 过滤查询，多重过滤查询， 包含过滤
    19. TABLE.object.order_by('**') or ('**', '**', ...) or ('-**')
    20. class Meta:   # 某项属性是排序优先选择
            ordering = ['**']
    21. TABLE.object.order_by('**').filter( ** ).get(name_contains = '**')
    22. 外键 多表 联立查询
        eg: 根据 Food name find restaurant
        Food.objects.get( name='切糕').restaurant
        eg: 得到餐厅的所有食物
        Restaurant.objects.get( name='小山窝').food_set.all()
    23. UPDATE and DELETE
        TABLE.objects.filter(name='**').update(key='**)
        TABLE.objects.filter(name='**') or all()  delete()

"""

class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=50, blank=True)
    # blank 允许资料留空

    def __unicode__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=3, decimal_places=0)
    # Decimal 浮点数 。 还有 BooleanField ... ...

    comment = models.CharField(max_length=50, blank=True)
    restaurant = models.ForeignKey(Restaurant)

    def __unicode__(self):
        return self.name



