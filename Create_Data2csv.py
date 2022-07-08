from faker import Faker
import csv
import time

num=input('请输入需要创建多少条数据:')
start=time.time()
fake = Faker(locale='zh_CN') # 设置造的数据是中文的
title=['客户名称','消费日期','消费金额']
data=[[fake.company(),    # 公司名
        fake.date(),       # 日期
        fake.random_int()] for x in range(int(num))] # 随机数据生成
#print(data)
#print(data[1][0])

path = 'RFM随机数据.csv'
try:                                                            # 解码器encoding='utf-8-sig' 不加的话用pandas读取中文会变成乱码
   with open(path, 'w', newline='',encoding='utf-8-sig') as t:  # numline是来控制空的行数的
    writer = csv.writer(t)  # 这一步是创建一个csv的写入器
    writer.writerow(title)  # 写入标签
    writer.writerows(data)  # 写入样本数据
except:
   pass
end=time.time()
print('完成,总用时为:',end-start)

# 文件读取
'''
f = open('RFM随机数据.csv', 'r')
with f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
'''
'''
import pandas as pd
df = pd.read_csv('RFM随机数据.csv')
print(df)
'''