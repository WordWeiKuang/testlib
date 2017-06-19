from model import Item, Paper, User, Code
from faker import Factory, Faker
from random import choice
from datetime import datetime
import hashlib

__token__ = 'kwdev'

faker = Faker()

faker_zh =  Factory.create('zh_CN')

def register_user():
    sha1_value = '%s:%s' % (faker.word(), __token__)
    code = Code.create(value=hashlib.sha1(sha1_value.encode('utf-8')).hexdigest())
    code.save()
    user = User.create(code=hashlib.sha1(code.value.encode('utf-8')).hexdigest())
    user.save()

def add_items():
    d1 = datetime.now()
    answer = ['A', 'B', 'C', 'D']
    answer2 = ['A', 'B']
    papers = Paper.select()
    for paper in papers:
        for i in range(30):
            if(i<=20):
                item = Item.create(index=i+1,content=faker_zh.text(),answer=choice(answer),
                                   answer_A=faker_zh.word(),answer_B=faker_zh.word(),answer_C=faker_zh.word(),answer_D=faker_zh.word(),
                                   answer_type = '选择题',score =1,paper=paper)
            else:
                item = Item.create(index=i + 1, content=faker_zh.text(), answer=choice(answer2),
                                   answer_A='正確', answer_B='錯誤',
                                   answer_type='判斷題', score=1, paper=paper)
            item.save()
            print('item:'+ str(item.index)+'done')
        #paper.munber = 30
        #paper.total = 30
        #paper.save()
        print('a paper save done')
    d2 = datetime.now()
    print('save success')
    print(d2-d1)

add_items()

'''

for i in range(100):
    answer_list = 'A.%s,B.%s,C.%s,D.%s' % (faker.word(), faker.word(), faker.word(), faker.word())

    data = Item.create(index=i+1,content=faker.text(),answer=choice(answer),answer_list=answer_list,
                answer_type='选择题',score=1,paper='001489370312806c48a1437217b44b6a3b9fc958d994c77000')
    print('item :'+ str(data.index)+ 'done')

    data.save()
'''
