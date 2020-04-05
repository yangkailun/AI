import numpy as np 
from numpy import mat

#将各节点的有向图转换为概率转移矩阵
def probability_graph(w_ori_mat):
    N = w_ori_mat.shape[0]
    for i in range(N):
        w_ori_mat[:,i] = w_ori_mat[:,i] / np.sum(w_ori_mat[:,i])  #这个sum函数用的好，直接的想法事用for循环，而这一个是用数学的方法，这种要总结
    return w_ori_mat

def pangerank(w_ori_mat, iter_num, c_damping = 0.15):
    N = w_ori_mat.shape[0]
    w_ori_mat = probability_graph(w_ori_mat)
    e_j = np.ones((N,1)) / N
    rank = e_j
    for i in range(iter_num):
        rank = (1-c_damping) * w_ori_mat * rank + c_damping * e_j
    return rank

#测试
w_ori_mat = mat([[0,1,0],[1,0,1],[1,0,0]], dtype=float)  #这里一定要注意加dtype，否则可能在计算的时候自动存为int型

print(pangerank(w_ori_mat, 6))


        
