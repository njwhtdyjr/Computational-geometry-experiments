# author:njw

import random
import time
import matplotlib.pyplot as plt


# 点类
class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
# 线段类
class LineSegment:
    def __init__(self,point1,point2):
        self.point1=point1
        self.point2=point2
#   求两个向量的点积
def DotProduct(point1,point2):
    return point1.x*point2.x+point1.y*point2.y

# 求两个向量的叉积
def CrossProduct(point1,point2):
    return point1.x*point2.y-point1.y*point2.x

# 判断两线段的相对方向
def Direction(point1,point2,point3):
    d = CrossProduct(Point(point3.x-point1.x,point3.y-point1.y),Point(point2.x-point1.x,point2.y-point1.y))
    if d>0:
        return 1
    elif d<0:
        return -1
    else:
        return 0

# 判断一个点是否在线段上
def OnSegment(point1,point2,point3):
    return CrossProduct(Point(point2.x-point1.x,point2.y-point1.y),Point(point3.x-point1.x,point3.y-point1.y))==0 and \
    DotProduct(Point(point2.x-point1.x,point2.y-point1.y),Point(point3.x-point1.x,point3.y-point1.y))<=0

# TODO:判断两线段是否相交
# 判断两线段是否相交
def IsIntersect(lineSegment1,lineSegment2):
    d1 = Direction(lineSegment2.point1,lineSegment2.point2,lineSegment1.point1)
    d2 = Direction(lineSegment2.point1,lineSegment2.point2,lineSegment1.point2)
    d3 = Direction(lineSegment1.point1,lineSegment1.point2,lineSegment2.point1)
    d4 = Direction(lineSegment1.point1,lineSegment1.point2,lineSegment2.point2)
    if d1*d2<0 and d3*d4<0:
        return True
    elif d1==0 and OnSegment(lineSegment1.point1,lineSegment2.point1,lineSegment2.point2):
        return True
    elif d2==0 and OnSegment(lineSegment1.point2,lineSegment2.point1,lineSegment2.point2):
        return True
    elif d3==0 and OnSegment(lineSegment2.point1,lineSegment1.point1,lineSegment1.point2):
        return True
    elif d4==0 and OnSegment(lineSegment2.point2,lineSegment1.point1,lineSegment1.point2):
        return True
    else:
        return False


# 初始化多边形时，点的列表不包括初始点，连接点的顺序按照自然顺序
# 如果自然顺序连接不成多边形，则改变点的顺序
# 多边形类
class Polygon:
    def __init__(self,points):
        self.points=points
        self.n = len(points)
        self.edges=[]
        for i in range(self.n-1):
            self.edges.append(LineSegment(points[i],points[i+1]))
        self.edges.append(LineSegment(points[-1],points[0]))
    #     画多边形
    def plot(self):
        x=[]
        y=[]
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
        x.append(self.points[0].x)
        y.append(self.points[0].y)
        plt.plot(x,y)
        # plt.plot([1,2],[1,2])
        plt.show()
    #     算多边形的面积
    def area(self):
        area=0
        for i in range(self.n-1):
            area+=(self.points[i].x*self.points[i+1].y-self.points[i+1].x*self.points[i].y)/2
        return abs(area)
#     TODO：判断点是否在多边形内部
#    判断点是否在多边形内部，不包括边界
#    对该点作水平向右的射线，判断射线与多边形的交点个数，如果是奇数个，则在多边形内部，否则在多边形外部
    def IsInside(self,point):
        cnt=0
        for i in range(self.n):
            if self.points[i%self.n].y == self.points[(i+1)%self.n].y:
                continue
            if point.y < min(self.points[i%self.n].y,self.points[(i+1)%self.n].y):
                continue
            if point.y >= self.points[i%self.n].y and point.y >= self.points[(i+1)%self.n].y:
                continue
            x = (point.y - self.points[i%self.n].y)*(self.points[(i+1)%self.n].x - self.points[i%self.n].x)/(self.points[(i+1)%self.n].y - self.points[i%self.n].y) + self.points[i%self.n].x
            if x > point.x:
                cnt+=1

        # # special用来记录射线与多边形的交点是顶点以及水平边的特殊情况，在special中的边在最简单的情况中不需要再判断
        # special=[]
        # # 考虑到射线与多边形的交点可能是顶点，该情况比较特殊，单独提前判断
        # # 第一种是判断水平边的情况
        # for i in range(self.n):
        #       # 如果射线与多边形的交点是顶点，则通过判断这个顶点的前后两个边是否位于射线的两侧来确定cnt加多少，同侧加2，两侧加1
        #       # 对于水平边，忽视，考虑与水平边相连的两条边是否在射线的两侧，同侧加2，两侧加1
        #
        #       if point.y == self.points[i%self.n].y and point.y == self.points[(i+1)%self.n].y and point.x < self.points[i%self.n].x and point.x < self.points[(i+1)%self.n].x:
        #             if (self.points[(i-1)%self.n].y - point.y)*(self.points[(i+2)%self.n].y - point.y) > 0:
        #                 cnt+=2
        #             else:
        #                 cnt+=1
        #             #     记录下有关顶点和边，避免重复计算
        #             special.append(i%self.n)
        #             special.append((i-1)%self.n)
        #             special.append((i+1)%self.n)
        # # 第二种是射线与多边形交点是顶点的情况，但排除了水平边的情况
        # for i in range(self.n):
        #     if i not in special:
        #         if point.y == self.points[i%self.n].y and point.x < self.points[i%self.n].x:
        #             if (self.points[(i-1)%self.n].y - point.y)*(self.points[(i+1)%self.n].y - point.y) > 0:
        #                 cnt+=2
        #             else:
        #                 cnt+=1
        #             special.append(i%self.n)
        #             special.append((i-1)%self.n)
        # # 第三种是最简单的情况，射线与多边形的交点不是顶点
        # for i in range(self.n):
        #     if i not in special:
        #         if self.points[i%self.n].y == self.points[(i+1)%self.n].y:
        #             continue
        #         if point.y < min(self.points[i%self.n].y,self.points[(i+1)%self.n].y):
        #             continue
        #         if point.y > max(self.points[i%self.n].y,self.points[(i+1)%self.n].y):
        #             continue
        #         x = (point.y - self.points[i%self.n].y)*(self.points[(i+1)%self.n].x - self.points[i%self.n].x)/(self.points[(i+1)%self.n].y - self.points[i%self.n].y) + self.points[i%self.n].x
        #         if x > point.x:
        #             cnt+=1
        return cnt%2==1

#    TODO：判断两顶点连线是不是对角线
#  判断两顶点连线是不是对角线（判断连续的三个点形成的线段是不是对角线）
    def IsDiagonal(self,point1,point2):
        # 两顶点连线有三种情况：
        # 1.完全在多边形内部，是对角线
        # 2.完全在多边形外部
        # 3.部分在多边形内部，部分在多边形外部。
        # 第3种情况，可以通过判断连线与多边形的边的相交情况来确定
        # 如果与多边形的边相交大于4次，有可能在多边形外部，此时在连线上任取一点判断是否在多边形内部即可。
        # 正常的对角线与多边形的边相交4次（如果我们对多边形的每一条边都单独判断的话）
        cnt=0
        for edge in self.edges:
            if IsIntersect(edge,LineSegment(point1,point2)):
                cnt+=1
                if cnt>4:
                    return False
        return self.IsInside(Point((point1.x+point2.x)/2,(point1.y+point2.y)/2))

#   TODO：多边形三角剖分算法(递归切耳算法)
#   返回值是对角线的列表
    def triangulation(self):
        diagonal = []
        # 递归出口，三角形的情况
        if self.n == 3:
            return diagonal
        seed = int(time.time())
        permutation = list(range(self.n))
        random.Random(seed).shuffle(permutation)
        # 遍历所有的点，找到一个对角线 或者 采用随机化的方法，随机选取一个点，找到一个对角线
        # for i in range(self.n):
        for i in permutation:
            if self.IsDiagonal(self.points[i % self.n], self.points[(i + 2) % self.n]):
                diagonal.append(LineSegment(self.points[i % self.n], self.points[(i + 2) % self.n]))
                # 递归求解剩下的多边形
                newpoints = []
                for j in range(self.n):
                    if j != (i + 1) % self.n:
                        newpoints.append(self.points[j])
                newpolygon = Polygon(newpoints)
                diagonal.extend(newpolygon.triangulation())
                # 找到一个对角线就可以了
                break
        return diagonal
    # 把三角剖分的结果画出来
    def plotTriangulation(self):
        diagonal = self.triangulation()
        for edge in diagonal:
            plt.plot([edge.point1.x,edge.point2.x],[edge.point1.y,edge.point2.y])
        self.plot()


if __name__ == '__main__':
    # i.18
    # points = [
    #     Point(0, 0),
    #     Point(10, 7),
    #     Point(12, 3),
    #     Point(20, 8),
    #     Point(13, 17),
    #     Point(10, 12),
    #     Point(12, 14),
    #     Point(14, 9),
    #     Point(8, 10),
    #     Point(6, 14),
    #     Point(10, 15),
    #     Point(7, 18),
    #     Point(0, 16),
    #     Point(1, 13),
    #     Point(3, 15),
    #     Point(5, 8),
    #     Point(-2, 9),
    #     Point(5, 5)
    # ]
    # i.snake
    points = [
        Point(10, 0),
        Point(20, 10),
        Point(30, 0),
        Point(40, 10),
        Point(50, 0),
        Point(50, 10),
        Point(40, 20),
        Point(30, 10),
        Point(20, 20),
        Point(10, 10),
        Point(0, 20),
        Point(0, 10)
    ]

    # points = [
    #     Point(0, 0),
    #     Point(10, 0),
    #     Point(10, 10),
    #     Point(0, 10)
    # ]
    polygon=Polygon(points)
    polygon.plotTriangulation()
