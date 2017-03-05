from model import Item
from faker import Faker
from random import choice
from datetime import datetime

faker = Faker()

answer = ['A', 'B', 'C', 'D']
d1 = datetime.now()
for i in range(100):
    answer_list = 'A.%s    B.%s    C.%s    D.%s' % (faker.name(), faker.name(), faker.name(), faker.name())

    data100 = Item.create(index=i+1,content=faker.text(),answer=choice(answer),answer_list=answer_list,
                answer_type='choice',score=1,paper='testdata')

    data100.save()

d2 = datetime.now()

print((d2-d1))