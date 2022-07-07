from faker import Faker
import xlwt

num=input('请输入需要创建多少条数据:')
fake = Faker(locale='zh_CN') # 设置造的数据是中文的
data=[['客户名称','日期','消费金额','消费数量']]
data+=[[fake.company(),    # 公司名
        fake.date(),       # 日期
        fake.pyint(),      # 数
        fake.random_int()] for x in range(int(num))] # 随机数据生成
#print(data)
#print(data[1][0])

nwb = xlwt.Workbook('utf-8')        # 新建工作簿
nws=nwb.add_sheet('RFM随机数据')      # 工作簿添加新表

for x in range(int(num)+1):
    for y in range(4):
        nws.write(x,y,data[x][y])    #把随机生成的数据放到excel里

nwb.save('RFM随机数据.xls')           # 保存工作簿
print('完成')
