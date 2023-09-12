import geometry
import wx
import collections
import copy
import heapq
import math


class MyFrame(wx.Frame):
    state = 1
    start_end = collections.deque(maxlen=2)
    temporary_set = []
    point_set = []
    line_set = []
    short_line = []
    dis = None
    pa = []
    pos = []

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "Euclidean shortest distance", size=(800, 600))
        self.panel = wx.Panel(self, -1)
        self.panel2 = wx.Panel(self.panel, wx.ID_ANY, style=wx.BORDER_DOUBLE)
        self.panel2.SetTransparent(200)
        # self.panel2.SetBackgroundColour('#00ff00')

        self.button_point = wx.Button(self.panel, -1, "Point")
        self.button_polygon = wx.Button(self.panel, -1, "Polygon")
        self.button_start = wx.Button(self.panel, -1, "START")
        self.posCtrl = wx.TextCtrl(self.panel, -1, "")

        # self.Bind
        self.panel2.Bind(wx.EVT_MOTION, self.OnMove)
        self.panel2.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.panel2.Bind(wx.EVT_RIGHT_DOWN, self.key_press)
        self.panel2.Bind(wx.EVT_PAINT, self.onPaint)
        # self.panel2.Bind(wx.EVT_KEY_DOWN, self.key_press)

        self.Bind(wx.EVT_BUTTON, self.button_point_OnClick, self.button_point)
        self.Bind(wx.EVT_BUTTON, self.button_polygon_OnClick, self.button_polygon)
        self.Bind(wx.EVT_BUTTON, self.button_start_OnClick, self.button_start)
        # self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.posCtrl, 0)
        vbox.Add((-1, 25))
        vbox.Add(self.button_point, 0)
        vbox.Add((-1, 25))
        vbox.Add(self.button_polygon, 0)
        vbox.Add((-1, 25))
        vbox.Add(self.button_start, 0)

        hbox.Add(vbox, 0, flag = wx.ALL)
        hbox.Add((-1,500))
        hbox.Add(self.panel2, -1, wx.EXPAND)

        wx.StaticText(self.panel, -1, pos=(10, 12))
        self.panel.SetSizer(hbox)

        self.Show()

    def OnErase(self, event):
        pass

    def button_point_OnClick(self, event):
        self.state = 1
        self.temporary_set.clear()
        self.panel2.Refresh()
        self.Show()

    def button_polygon_OnClick(self, event):
        self.state = 2

    def button_start_OnClick(self, event):
        d = copy.deepcopy(self.point_set)
        d.append([self.start_end[0], self.start_end[1]])

        for i in d:
            for j in i:
                self.visiblevertices_1(j)
        self.shortestpath()
        self.panel2.Refresh()
        self.Show()

        dlg = wx.MessageDialog(None, "最短距离为%f" % self.dis, "提示", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()

    def key_press(self, event):
        """key = event.GetKeyCode()
        if key == "d":
            self.state = 0
            self.temporary_set.clear()
            print("d")
            #从画板和数据中删除未画完的多边形
        if key == "c":"""
        if len(self.temporary_set) > 0:
            self.temporary_set[0].last = self.temporary_set[len(self.temporary_set) - 1]
            self.temporary_set[len(self.temporary_set) - 1].next = self.temporary_set[0]
            # 算多边
            min = self.temporary_set[0].x
            mp = self.temporary_set[0]
            for po in self.temporary_set:
                if po.x < min:
                    min = po.x
                    mp = po
            if (mp.x - mp.last.x) * (mp.next.y - mp.y) - (mp.y - mp.last.y) * (mp.next.x - mp.x) > 0:
                for i in self.temporary_set:
                    i.last, i.next = i.next, i.last

            self.point_set.append(copy.deepcopy(self.temporary_set))
            # 闭合，存储和绘制多边形
        self.temporary_set.clear()
        self.panel2.Refresh()
        self.Show()

    def OnMove(self, event):
        self.pos = event.GetPosition()
        if len(self.temporary_set) > 0:
            self.posCtrl.SetValue("%s, %s" % (self.pos.x, self.pos.y))
            self.panel2.Refresh()
            self.Show()

    def onPaint(self, event):

        dc = wx.PaintDC(self.panel2)
        dc.Clear()
        dc.SetPen(wx.Pen('#000000'))
        dc.SetBrush(wx.Brush('#ff0000'))

        if len(self.temporary_set) > 0:
            dc.DrawLine(self.pos.x, self.pos.y, self.temporary_set[-1].x, self.temporary_set[-1].y)

        for i in self.start_end:
            dc.DrawCircle(i.x, i.y, 2)

        dc.SetPen(wx.Pen('#339933'))
        if len(self.temporary_set) > 1:
            temp=iter(self.temporary_set)
            next(temp)
            for i in temp:
                dc.DrawLine(i.last.x, i.last.y, i.x, i.y)

        dc.SetPen(wx.Pen('#663300'))
        dc.SetBrush(wx.Brush('#663300'))
        for i in self.point_set:
            pl = []
            for j in i:
                pl.append([j.x, j.y])
            dc.DrawPolygon(pl)

        dc.SetPen(wx.Pen('#0000ff'))
        for i in self.line_set:
            dc.DrawLine(i.p1.x, i.p1.y, i.p2.x, i.p2.y)

        dc.SetPen(wx.Pen('#ff0000', width=2))
        dc.SetBrush(wx.Brush('#ff0000'))
        last_x = None
        last_y = None
        for i in self.pa:
            if last_x != None:
                dc.DrawLine(i.x, i.y, last_x, last_y)
                last_x = i.x
                last_y = i.y
            else:
                last_x = i.x
                last_y = i.y

    def OnClick(self, event):
        if self.state == 1:
            pos = event.GetPosition()
            point = geometry.Point(pos.x, pos.y)
            self.start_end.appendleft(point)

        if self.state == 2:
            pos = event.GetPosition()
            point = geometry.Point(pos.x, pos.y)
            if len(self.temporary_set) > 0:
                point.last = self.temporary_set[len(self.temporary_set)-1]
                self.temporary_set[len(self.temporary_set)-1].next = point
            self.temporary_set.append(point)

        self.panel2.Refresh()
        self.Show()

    def distance(self, p1: geometry.Point, p2: geometry.Point):
        s = ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
        return s

    def shortestpath(self):
        node_list = []
        # 构建节点
        # 最后输入的点link错误

        for i in self.line_set:
            check1 = False
            check2 = False
            p1_node = None
            p2_node = None
            for n in node_list:
                if n.point.x == i.p1.x and n.point.y ==i.p1.y:
                    p1_node = n
                    check1 = True
                if n.point.x == i.p2.x and n.point.y ==i.p2.y:
                    p2_node = n
                    check2 = True
                if check1 and check2:
                    break
            if check1 == False:
                p1_node = geometry.Net_node(i.p1)
                node_list.append(p1_node)
            if check2 == False:
                p2_node = geometry.Net_node(i.p2)
                node_list.append(p2_node)

            p1_node.link.append([p2_node, self.distance(i.p1, i.p2)])
            p2_node.link.append([p1_node, self.distance(i.p1, i.p2)])

        for n in node_list:
            for i in n.link[:]:
                if i[0] == None:
                    n.link.remove(i)
                else:
                    pass
                    # print(i[0].point.x, i[0].point.y, i[1])

        start1 = None
        end1 = None
        open_list = []
        for i in node_list:
            if i.point.x == self.start_end[0].x and i.point.y == self.start_end[0].y:
                start1 = i
            if i.point.x == self.start_end[1].x and i.point.y == self.start_end[1].y:
                end1 = i

        heapq.heappush(open_list, [start1.distance + self.distance(start1.point, end1.point), start1])

        while end1.check == False:
            if len(open_list) == 0:
                break
            i = heapq.heappop(open_list)
            if i[1].check == False:
                for j in i[1].link:
                    if j[0].check == False:
                        if j[0].distance == 0 or j[0].distance > (i[1].distance + j[1]):
                            j[0].path = [j[0].point]
                            j[0].path.extend(i[1].path)
                            j[0].distance = i[1].distance + j[1]
                            h = j[0].distance + self.distance(j[0].point, end1.point)
                            heapq.heappush(open_list, [h, j[0]])
                i[1].check = True

#        while len(open_list) != 0:
#            open_list = self.bfs(open_list)

        self.dis = end1.distance
        self.pa = end1.path

    def cross(self, p1, p2, p3):  # 内积
        x1 = p2.x - p1.x
        y1 = p2.y - p1.y
        x2 = p3.x - p1.x
        y2 = p3.y - p1.y
        return x1 * y2 - x2 * y1

    def IsIntersec(self, p1, p2, p3, p4):
        # 快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交
        if (max(p1.x, p2.x) > min(p3.x, p4.x)
                and max(p3.x, p4.x) > min(p1.x, p2.x)
                and max(p1.y, p2.y) > min(p3.y, p4.y)
                and max(p3.y, p4.y) > min(p1.y, p2.y)):
            # 若通过快速排斥则进行跨立实验
            #if (p1.x == p4.x and p1.y == p4.y) or (p2.x == p4.x and p2.y == p4.y):
                #return True
            if (self.cross(p1, p2, p3) * self.cross(p1, p2, p4) < 0
                    and self.cross(p3, p4, p1) * self.cross(p3, p4, p2) < 0):
                return True
            elif(self.cross(p1, p2, p3) * self.cross(p1, p2, p4) == 0
                    or self.cross(p3, p4, p1) * self.cross(p3, p4, p2) == 0):
                if (self.cross(p1.last, p1.next, p3) * self.cross(p1.last, p1.next, p4) < 0
                        and self.cross(p3, p4, p1.last) * self.cross(p3, p4, p1.next) < 0):
                    return True
                else:
                    return False

            else:
                return False
        else:
            return False

    def angle(self, p, i):
        __x = i.x - p.x
        __y = i.y - p.y
        __l = (__x**2 + __y**2)**0.5
        __s = __y/__l
        __c = __x/__l
        if __y >= 0:
            return math.acos(__c)
        else:
            return 2 * math.pi - math.acos(__c)

    # p原点，i待扫描点，i_l上一个扫描过的点，l_list交线队列，point_list，tree二叉树,i_l_b i_l是否可视
    def visible(self, p, i, i_l, l_list, tree, i_l_b):
        if p.last == None:
            max = 8
            min = 0
        else:
            max = tree.angle(p.last)
            min = tree.angle(p.next)
        # 判断句，跳过俩个邻边之间的点

        if max < min:
            con1 = (tree.angle(i) >= min or tree.angle(i) <= max)
        else:
            con1 = (tree.angle(i) >= min and tree.angle(i) <= max)

        if i.last == None:
            max = 8
            min = 0
        else:
            max = self.angle(i, i.last)
            min = self.angle(i, i.next)
        # 判断句，跳过俩个邻边之间的点
        an = self.angle(i, p)
        if max < min:
            con2 = (an >= min or an <= max)
        else:
            con2 = (an >= min and an <= max)
        if con1 and con2:
            pass
        else:

            return False
        if len(l_list.L) == 0:
            return True
        if i_l == None:
            if self.IsIntersec(l_list.L[0].p1, l_list.L[0].p2, p, i):

                return False
            else:
                return True
        else:
            if tree.angle(i) == tree.angle(i_l):
                if i_l_b:
                    for k in l_list.L:
                        if self.IsIntersec(k.p1, k.p2, i_l, i):

                            return False
                    return True
                else:

                    return False
            elif self.IsIntersec(l_list.L[0].p1, l_list.L[0].p2, p, i):

                return False
            else:
                return True

    def visiblevertices_1(self, p):

        point_list = []
        u = [self.start_end[0], self.start_end[1]]

        for i in u:
            if i.x == p.x and i.y == p.y:
                u.remove(i)
                break
        tree = geometry.BST(u, p)
        tree.l.clear()
        for i in self.point_set:
            for j in i:
                tree.insert(j)

        tree.InOrderTraverse(tree.root)

        for i in tree.l:
            point_list.append(i)

        l_list = geometry.L_set(p)
        l_list.L.clear()
        p0 = geometry.Point(99999, p.y)
        i_l = None
        i_l_b = True
        for i in self.point_set:
            for j in i:
                if j.next is not None:
                    # p0 = geometry.Point(99999, p.y)
                    if self.IsIntersec(j, j.next, p, p0):
                        l_list.append(geometry.Line(j, j.next), j)

        for i in point_list:
            # 删线
            for k in l_list.L[:]:
                if k.p1.x == i.x and k.p1.y == i.y:
                    x1 = i.x - p.x
                    y1 = i.y - p.y
                    x2 = k.p2.x - i.x
                    y2 = k.p2.y - i.y
                    if x1 * y2 - x2 * y1 < 0:
                        l_list.L.remove(k)
                elif k.p2.x == i.x and k.p2.y == i.y:
                    x1 = i.x - p.x
                    y1 = i.y - p.y
                    x2 = k.p1.x - i.x
                    y2 = k.p1.y - i.y
                    if x1 * y2 - x2 * y1 < 0:
                        l_list.L.remove(k)

            # 增线

            if i.next is not None:
                if (i.x - p.x) * (i.last.y - i.y) - (i.last.x - i.x) * (i.y - p.y) > 0:
                    l_list.append(geometry.Line(i, i.last), i)

                if (i.x - p.x) * (i.next.y - i.y) - (i.next.x - i.x) * (i.y - p.y) > 0:
                    l_list.append(geometry.Line(i, i.next), i)

            # 输出
            # p原点，i待扫描点，i_l上一个扫描过的点，l_list交线队列，point_list，tree二叉树,i_l_b i_l是否可视
            if self.visible(p, i, i_l, l_list, tree, i_l_b):
                self.line_set.append(geometry.Line(p, i))

                i_l_b = True
            else:
                i_l_b = False
            i_l = i
        del tree


class App(wx.App):
    def OnInit(self):
        return True


if __name__ == '__main__':
    app = App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
