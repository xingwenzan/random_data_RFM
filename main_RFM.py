import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

start=time.time()                    # 记录开始时间
data=pd.read_csv("C:.\RFM随机数据.csv")           # 读入数据
#print(data)

data['消费日期']=pd.to_datetime(data['消费日期'])

data=data.groupby('客户名称').agg(                # groupby 分组; agg 聚合 用法:agg('列名','函数')
    last_date=('消费日期','max'),                 # 最近一次消费日期
    F=('消费日期','count'),                       # 消费次数
    M=('消费金额','mean')                         # 用户平均消费金额
).reset_index()
#print(data) #[324 rows x 4 columns]
data['R']=(datetime.datetime.now()-data['last_date']).dt.days       # 最近一次消费与当前日子相差天数
#data['R']=(pd.to_datetime('2022-07-10')-data['last_date']).dt.days
#print(data)

# 对R、F、M分箱打分
data['R_score']=pd.cut(data['R'],                # cut 将数据分成不同区间; bins 分组依据
    bins=[-100,7,14,30,60,90,180,500],           # 任意指定区间,区间必须足够大，否则会出现NaN，出现 Cannot convert float NaN to integer 错误，int改float可以发现
    labels=[7,6,5,4,3,2,1],                      # 返回的标签，与 bins 的区间对应
).astype('int')                                  # 指定返回的数据类型

data['F_score']=pd.cut(data['F'],
    bins=[0,1000,5000,7000,8000,9000,10000,100000],               # 任意指定区间
    labels=[1,2,3,4,5,6,7],
).astype('int')

data['M_score']=pd.cut(data['M'],
    bins=[0,500,1000,2000,2500,3000,5000,10000],               # 任意指定区间
    labels=[1,2,3,4,5,6,7],
).astype('int')
#print(data)

#以R、F、M均值为标准评价高低，1高0低，*1是为了将布尔值转化为1、0
data['R_level']=(data['R_score']>data['R_score'].mean())*1
data['F_level']=(data['F_score']>data['F_score'].mean())*1
data['M_level']=(data['M_score']>data['M_score'].mean())*1
# RFM值; .astype() 转换数据类型; .str.cat() 字符串连接
data['RFM']=data['R_level'].astype('str').str.cat([data['F_level'].astype('str'),
                                                   data['M_level'].astype('str')])
# RFM值转换成对应评价; replace 替换
data['RFM']=data['RFM'].replace(['111','101','011','001','110','100','010','000'],
                                ['重要价值客户','重要发展客户','重要保持客户','重要挽留客户','一般价值客户','一般发展客户','一般保持客户','一般挽留客户'])
#print(data)

#数据保存; 命名后默认保存当前路径，取消index
#data.to_excel('RFM.xls',index=False)

# 可视化

sns.set(font='SimHei',style='darkgrid')         # 默认主题
user_RFM = data.groupby(data['RFM']).size()     # 计算各组元素个数
plt.figure(figsize = (10,4),dpi=80)             # 画板，有这个才能画
user_RFM.sort_values(ascending=True,inplace=True)         # 排序，正序 https://zhuanlan.zhihu.com/p/35013079
plt.title(label='随机数据RFM',                    # 设置标题
    fontsize=22,
    color='white',
    backgroundcolor='#334f65',
    pad=10)                   # 距离图像高度
s = plt.barh(                 # 创建条形图（横柱状图）
    user_RFM.index,
    user_RFM.values,
    height=0.8,
    color=plt.cm.coolwarm_r(np.linspace(0,1,len(user_RFM))))
for rect in s:
    width = rect.get_width()  # 获取图像宽度
    plt.text(                 # 设置图像文本
        width+5,                                # 文本位置(x,y)的x（横向位置，而非x轴）
        rect.get_y() + rect.get_height()/3,     # 文本位置的y（纵向位置）
        str(width),                             # 文本内容
        ha= 'center')                           # 不知道有啥用，去掉结果不变
plt.grid(axis='y')                              # 显示y轴方向的网格 https://www.runoob.com/matplotlib/matplotlib-grid.html
plt.show()


'''
fig = px.bar(data['RFM'],
             x=data['RFM'].unique(),
             y=data['RFM'].value_counts(),
             color=data['RFM'].value_counts(),

             )
fig.show()
end=time.time()
print('总用时为:',end-start)
'''

'''
# (此方法不好使，目前不知道为什么）
# 可视化准备
# Pandas中Series和DataFrame的两种数据类型中都有nunique（）和unique（）方法。
# 这两个方法都是求Series或Pandas中的不同值，但是unique（）方法返回的是去重之后的不同值，而nunique（）方法则直接放回不同值的个数。
# 按RFM分组，用nunique（）返回不同 客户名称 个数，将 客户名称 这个series对象转换从DataFrame格式
dcount=data.groupby('RFM')['客户名称'].nunique().to_frame('用户数').reset_index
#print(dcount)
fig = px.bar(dcount,x="RFM",y="用户数")
fig.show()
'''

'''
# （好使，但不好看，莫名其妙有一些乱码）
plt.figure(figsize = (10,4),dpi=80)
dcount=data.groupby('RFM')['客户名称'].nunique().to_frame('用户数')#.reset_index
x=data['RFM'].unique()
y=dcount['用户数']
plt.bar(x,y)
plt.xlabel('RFM')
plt.ylabel('用户数')
plt.show()
'''