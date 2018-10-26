import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pylab import mpl

data=pd.read_csv('Anjuke.csv',encoding='GBK')
# print(data.head())#查看前五行
# print(data.info())#查看列表信息
address_data=data['区域'].unique()#打印出地区唯一化之后的值
print(len(data['区域'].unique()))#打印唯一化之后的地区的个数
address_count=data['区域'].value_counts()

# groupby（n）:通过n进行分组;mean()返回平均值;sort_values()排序,ascengding排序方式（升序或者降序)默认为True
address=data.groupby('区域')['单价/每平米'].mean().sort_values(ascending=False)#得到每个区域的房价单价
area=data.groupby('区域')['面积/平方米'].mean().sort_values(ascending=False)#得到得到每个区域面积的平均值
price_all=data.groupby('区域')['总价/万'].mean().sort_values(ascending=False)#得到每个区域房屋的平均总价
max_price=data.groupby('区域')['单价/每平米'].max()
min_price=data.groupby('区域')['单价/每平米'].min()

mpl.rcParams['font.sans-serif']=['FangSong'] #指定默认字体
mpl.rcParams['axes.unicode_minus'] = False   #解决显示'-'为方块的问题
# 定义一个数组
#

bins1 = np.arange(0,60000,6000)

# 将数组进行离散化，按照一定的数值指标，将数据划分为不同的区间,在这里就是将单价/每平米这一列的数据进行归类，第一个参数传入要离散的列，第二个参数传入一个数组
data_ls1 = pd.cut(data['单价/每平米'], bins1)
# 数据透视化,第一为需要计算的列的名称，index表示下标,conlums表示离散化数据的区间，afffunc传入的是每个区间内存在的数据的数量
# 这里没有搞懂为什么要这样
table = data.pivot_table('面积/平方米', index='区域', columns=data_ls1, aggfunc='count')
# bar表示柱状图 stacked表示是否重叠
table.plot(kind='bar', stacked=True)
# 将表格展示出来
plt.show()

# 将总价的数据进行离散化操作
bins2 = np.array([0, 40, 80, 150, 250, 500, 2000])
data_ls2 = pd.cut(data['总价/万'], bins2)
table2 = data.pivot_table('总价/万', index='区域', columns=data_ls2, aggfunc='count')
table2.plot(kind='bar', stacked=True)
plt.show()
#
# 将房屋的面积进行离散化
bins3 = np.array([0, 50, 75, 100, 125, 150, 175, 200, 300, 1500])
data_ls3 = pd.cut(data['面积/平方米'], bins3)
table3 = data.pivot_table('面积/平方米', index='区域', columns=data_ls3, aggfunc='count')
table3.plot(kind='bar', stacked=True)
plt.show()


