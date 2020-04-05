import itertools
import random

#这个算法的局限：对鸢尾花数据集使用，并且是分三个类的时候可以评估算法优劣。对其他情况可以分类，但是不能评估

class Kmeans:
    def __init__(self):
        pass

    def list_add(self, a, b):
        c = []
        for i in range(len(a)):
            c.append(a[i] + b[i])
        return c

    #计算两点之间的距离
    #输入是测量的两个点（一维情况）
    #输出两点距离
    def distance(self, a, b):
        dis = abs(a-b)
        return dis

    def first_close(self, one_point, some_point):
        min_point = self.distance(one_point, some_point[0])
        num = 0
        for index in range(len(some_point)):
            dis = self.distance(one_point, some_point[index])
            if dis < min_point:
                num = index
                min_point = dis
        return num

    #range_value是两个元素的列表，第一个是最小值，第二个是最大值。再两个值之间选择k个中心点
    #平均选取
    #kind = 1
    def choose_point(self, range_value, k, kind):
        point = []
        if kind == 1:  #平均选取聚类中心
            step = (range_value[1] - range_value[0]) / (k + 1)
            point = [range_value[0] + i * step for i in range(1, k+1)]
        elif kind == 2:  #随机选择聚类中心,首先把一个范围分为k个区域，在每个区域内随机（自己想的）
            step = (range_value[1] - range_value[0]) / k  #这个step和上一个step不同
            point = [random.random() * (range_value[0] + (i+1) * step - (range_value[0] + i * step)) + range_value[0] + i * step \
                for i in range(k)]
        return point

    def change_point(self, result, data, point, k):
        ch_point = []
        for i in range(k):
            num = len(result[i])
            if num != 0:
                total = 0
                for index in result[i]:
                    total = total + data[index]
                ch_point.append(total / num)
            else:
                ch_point.append(point[i])
        return ch_point

    #data:一个列表，代表各个点的坐标
    def kmeans(self, data, k):
        length = len(data)
        point = []  #记录聚类中心的坐标
        result = {}  #记录分的类中的点
        result_label = []  #存放每个样本的分类标签
        for i in range(k):  #初始化结果字典，每个类里都是空的
            result[i] = []
        point = self.choose_point([min(data),max(data)], k, 2)
        for i in range(length):
            result_label.append(self.first_close(data[i], point))
            result[self.first_close(data[i], point)].append(i)
        old_point = point 
        point = self.change_point(result, data, point, k) #根据第一个聚类的结果，移动聚类中心
        while old_point != point:
            result = {}  
            result_label = []  
            for i in range(k):  
                result[i] = []
            for i in range(length):
                result_label.append(self.first_close(data[i], point))
                result[self.first_close(data[i], point)].append(i)
            old_point = point 
            point = self.change_point(result, data, point, k)
        return {'data':data, 'point':point, 'result':result, 'result_label':result_label}



    def change_label(self, origin_label):
        label_name = [0, 1, 2]
        total_label = []
        for name in itertools.permutations(label_name):
            label = []
            for each in origin_label:
                if each == 'setosa':
                    label.append(name[0])
                elif each == 'versicolor':
                    label.append(name[1])
                else:
                    label.append(name[2])
            total_label.append(label)
        return total_label

    def CA(self, origin_label, result_label):  #准确性 Cluster Accuracy
        origin_label = self.change_label(origin_label)
        right_num_max = 0
        label_max = origin_label[0]
        total_num = len(result_label)
        for i in range(len(origin_label)):
            right_num = 0
            for index in range(len(result_label)):
                if origin_label[i][index] == result_label[index]:
                    right_num = right_num + 1
            if right_num > right_num_max:
                right_num_max = right_num
                label_max = origin_label[i]
        ca_value = right_num_max / total_num
        return {'ca':ca_value, 'label_max':label_max}
        
#评估

# # iris = pd.read_csv(r'I:\实验室\算法学习\Kmeans聚类\自己编写\iris1.csv')
# iris = pd.read_csv(r'I:\实验室\算法学习\Kmeans聚类\自己编写\iris.csv')

# sepal_length = iris.sepal_length.values #得到九个样本的sepal length长度
# sepal_width = iris.sepal_width.values
# petal_length = iris.petal_length.values
# petal_width = iris.petal_width.values
# species = iris.species.values

# alg = Kmeans()

# output = [alg.kmeans(sepal_length, 3), alg.kmeans(sepal_width, 3), alg.kmeans(petal_length, 3), alg.kmeans(petal_width, 3)]
# output1 = alg.kmeans(alg.list_add(petal_length, petal_width), 3)
# output_label = iris.columns.values[0:-1]

# # 输出准确度
# for index in range(len(output)):
#     print({output_label[index]:alg.CA(species, output[index]['result_label'])['ca']})
# print({'(petal_length+petal_width)/2':alg.CA(species, output1['result_label'])['ca']})




