from model import Item, Paper
from faker import Factory
from random import choice
from datetime import datetime

faker =  Factory.create('zh_CN')

d1 = datetime.now()

answer = ['A', 'B', 'C', 'D']

for i in range(100):
    answer_list = 'A.%s    B.%s    C.%s    D.%s' % (faker.word(), faker.word(), faker.word(), faker.word())

    data = Item.create(index=i+1,content=faker.text(),answer=choice(answer),answer_list=answer_list,
                answer_type='选择题',score=1,paper='001488853815593ed92d53418ed4aca9751a39b14e03d33000')
    print('item :'+ str(data.index)+ 'done')

    data.save()
d2 = datetime.now()
print((d2-d1))

'''
for i in range(100):
    data = Paper.create(name=faker.name(),munber=100,total=100)

'''