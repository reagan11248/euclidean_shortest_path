import math



class Point:

    def __init__(self, x, y, lp=None, np=None):
        self.x = x
        self.y = y
        self.last = lp
        self.next = np
        self.node = None

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

class L_set:
    L = []
    p: Point

    def __init__(self, p: Point):
        self.p = p

    def append(self, l: Line, p1: Point):
        if len(self.L) == 0:
            self.L.append(l)
        else:
            b = True
            for i in self.L:
                if i.p1.x == l.p1.x and i.p1.y == l.p1.y:
                    if i.p2.x == l.p2.x and i.p2.y == l.p2.y:
                        b = False
                if i.p2.x == l.p1.x and i.p2.y == l.p1.y:
                    if i.p1.x == l.p2.x and i.p1.y == l.p2.y:
                        b = False
            if b:
                # 判断顺序再插入
                b1 = (l.p2.y - l.p1.y) * l.p1.x + (l.p1.x - l.p2.x) * l.p1.y
                b2 = (p1.y - self.p.y) * self.p.x + (self.p.x - p1.x) * self.p.y
                d = (l.p2.x - l.p1.x) * (p1.y - self.p.y) - (p1.x - self.p.x) * (l.p2.y - l.p1.y)
                D1 = b2 * (l.p2.x - l.p1.x) - b1 * (p1.x - self.p.x)
                D2 = b2 * (l.p2.y - l.p1.y) - b1 * (p1.y - self.p.y)
                if d == 0:
                    s1 = min(((l.p1.x - self.p.x) ** 2 + (l.p1.y - self.p.y) ** 2) ** 0.5,
                             ((l.p2.x - self.p.x) ** 2 + (l.p2.y - self.p.y) ** 2) ** 0.5)
                else:
                    x0 = D1/d
                    y0 = D2/d
                    s1 = ((x0 - self.p.x) ** 2 + (y0 - self.p.y) ** 2) ** 0.5

                for i in self.L:
                    b1 = (i.p2.y - i.p1.y) * i.p1.x + (i.p1.x - i.p2.x) * i.p1.y
                    b2 = (p1.y - self.p.y) * self.p.x + (self.p.x - p1.x) * self.p.y
                    d = (i.p2.x - i.p1.x) * (p1.y - self.p.y) - (p1.x - self.p.x) * (i.p2.y - i.p1.y)
                    D1 = b2 * (i.p2.x - i.p1.x) - b1 * (p1.x - self.p.x)
                    D2 = b2 * (i.p2.y - i.p1.y) - b1 * (p1.y - self.p.y)
                    if d == 0:
                        s2 = min(((i.p1.x - self.p.x) ** 2 + (i.p1.y - self.p.y) ** 2) ** 0.5,
                                 ((i.p2.x - self.p.x) ** 2 + (i.p2.y - self.p.y) ** 2) ** 0.5)
                    else:
                        x0 = D1 / d
                        y0 = D2 / d
                        s2 = ((x0 - self.p.x) ** 2 + (y0 - self.p.y) ** 2) ** 0.5

                    if s1 <= s2:
                        if s1 == s2:
                            # 比较相对扫描线的偏转角大的排前面
                            x1 = i.p1.x - self.p.x
                            y1 = i.p1.y - self.p.y
                            x2 = i.p2.x - i.p1.x
                            y2 = i.p2.y - i.p1.y
                            x3 = l.p2.x - l.p1.x
                            y3 = l.p2.y - l.p1.y
                            r1 = math.acos((x1 * x2 + y1 * y2) / (x1 ** 2 + y1 ** 2) ** 0.5 /
                                           (x2 ** 2 + y2 ** 2) ** 0.5)
                            r2 = math.acos((x1 * x3 + y1 * y3) / (x1 ** 2 + y1 ** 2) ** 0.5 /
                                           (x3 ** 2 + y3 ** 2) ** 0.5)
                            if r1 < r2:
                                self.L.insert(self.L.index(i), l)
                                break
                            else:
                                self.L.insert(self.L.index(i) + 1, l)
                                break
                        else:
                            self.L.insert(self.L.index(i), l)
                            break
                    elif self.L.index(i) == (len(self.L) - 1):
                        self.L.append(l)
                        break
class Node:
    def __init__(self, point: Point):
        self.point = point
        self.lchild = None
        self.rchild = None

class BST:
    bp = None
    l = []

    def __init__(self, node_list, p: Point):
        self.root = Node(node_list[0])
        self.bp = p
        for point in node_list[1:]:
            self.insert(point)

    def angle(self, point1: Point):
        __x = point1.x - self.bp.x
        __y = point1.y - self.bp.y
        __l = (__x**2 + __y**2)**0.5
        __s = __y/__l
        __c = __x/__l
        if __y >= 0:
            return math.acos(__c)
        else:
            return 2 * math.pi - math.acos(__c)
    def distance(self, point: Point):
        return math.sqrt((math.pow((point.x - self.bp.x), 2) + pow((point.y - self.bp.y), 2)))


    # 搜索
    def search(self, node, parent, point):
        if point.x != self.bp.x or point.y != self.bp.y:
            if node is None:
                return False, node, parent
            if node.point.x == point.x and node.point.y == point.y:
                return True, node, parent
            if self.angle(node.point) > self.angle(point) or \
                    (self.angle(node.point) == self.angle(point) and
                     self.distance(node.point) > self.distance(point)):
                return self.search(node.lchild, node, point)
            else:
                return self.search(node.rchild, node, point)
        else:
            return True, node, parent

    # 插入
    def insert(self, point):
        if point.x != self.bp.x or point.y != self.bp.y:
            find, n, p = self.search(self.root, self.root, point)
            if not find:
                new_node = Node(point)
                if self.angle(p.point) > self.angle(point) or \
                    (self.angle(p.point) == self.angle(point) and
                     self.distance(p.point) > self.distance(point)):
                    p.lchild = new_node
                else:
                    p.rchild = new_node

    # 删除
    def delete(self, root, point):
        flag, n, p = self.search(root, root, point)
        if flag is False:
            return False
        else:
            if n.lchild is None:
                if n == p.lchild:
                    p.lchild = n.rchild
                else:
                    p.rchild = n.rchild
                del p
            elif n.rchild is None:
                if n == p.lchild:
                    p.lchild = n.lchild
                else:
                    p.rchild = n.lchild
                del p
            else:  # 左右子树均不为空
                pre = n.rchild
                if pre.lchild is None:
                    n.point = pre.point
                    n.rchild = pre.rchild
                    del pre
                else:
                    next = pre.lchild
                    while next.lchild is not None:
                        pre = next
                        next = next.lchild
                    n.data = next.data
                    pre.lchild = next.rchild
                    del p

    # 中序遍历
    def InOrderTraverse(self, node):
        if node is not None:
            self.InOrderTraverse(node.lchild)
            self.l.append(node.point)
            self.InOrderTraverse(node.rchild)

class Net_node:

    def __init__(self, p: Point):
        self.point = p
        self.check = False
        self.link = []
        self.path = [p]
        self.distance = 0