from model import Item, Paper, User
from faker import Factory
from random import choice
from datetime import datetime

faker =  Factory.create('zh_CN')

d1 = datetime.now()

answer = ['A', 'B', 'C', 'D']
for i in range(100):
    answer_list = 'A.%s,B.%s,C.%s,D.%s' % (faker.word(), faker.word(), faker.word(), faker.word())

    data = Item.create(index=i+1,content=faker.text(),answer=choice(answer),answer_list=answer_list,
                answer_type='选择题',score=1,paper='001489370312806c48a1437217b44b6a3b9fc958d994c77000')
    print('item :'+ str(data.index)+ 'done')

    data.save()
d2 = datetime.now()
print((d2-d1))

#user = user = User.create(name='用户',email='test@qq.com',image='tets.jpg',code='xxxxxxxxxxx',setting='{}',tag='{}')
#user.save()
#for i in range(20):
#    data = Paper.create(name=faker.word(),munber=100,total=100)
#    data.save()