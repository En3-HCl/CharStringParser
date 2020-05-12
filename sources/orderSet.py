class NumberToken:
    def __init__(self, number):
        self.value = number

    def toNumber(self):
        return float(self.value)
##############################################

#命令情報を入れるオブジェクト
class OrderSet:
    def __init__(self, type, args):
        self.args = args
        self.type = type

        #始点(あとでセットする)
        self.startPosition = (0,0)
        #終点(あとでセットする)
        self.endPosition = (0,0)
        #絶対座標に直した、辿る点を入れる。ハンドルとアンカーは区別せず入れる(暫定)
        self.absolutePositions = []
    def setAbsolutePosition(self, startPosition):
        if not self.type.isDrawOrder():
            return
        #始点を決定する。
        self.startPosition = startPosition
        #タイプ毎に読んでいく。
        if self.type == OrderType.rmoveto:
            self.absolutePositions = (self.startPosition[0] + self.args[0].toNumber(), self.startPosition[1] + self.args[1].toNumber())
            self.endPosition = (self.absolutePositions[0], self.absolutePositions[1])
            return

        if self.type == OrderType.hmoveto:
            self.absolutePositions = (self.startPosition[0] + self.args[0].toNumber(), self.startPosition[1])
            self.endPosition = (self.absolutePositions[0], self.absolutePositions[1])
            return
        if self.type == OrderType.vmoveto:
            self.absolutePositions = (self.startPosition[0], self.startPosition[1] + self.args[0].toNumber())
            self.endPosition = (self.absolutePositions[0], self.absolutePositions[1])
            return

        if self.type ==  OrderType.rlineto:
            #引数は偶数個とわかっている
            curPosition = (self.startPosition[0], self.startPosition[1])
            for i in range(int(len(self.args)/2)):
                dx = self.args[2*i].toNumber()
                dy = self.args[2*i+1].toNumber()
                curPosition = (curPosition[0]+dx, curPosition[1]+dy)
                self.absolutePositions.append(curPosition[0])
                self.absolutePositions.append(curPosition[1])
            self.endPosition = (curPosition[0], curPosition[1])
            return

        if self.type == OrderType.hlineto:
            curPosition = (self.startPosition[0], self.startPosition[1])
            #引数の個数とは無関係に、偶数番がdx、奇数番がdyである。
            for i in range(len(self.args)):
                if i%2 == 0:
                    dx = self.args[i].toNumber()
                    curPosition = (curPosition[0]+dx, curPosition[1])
                    self.absolutePositions.append(curPosition)
                if i%2 == 1:
                    dy = self.args[i].toNumber()
                    curPosition = (curPosition[0], curPosition[1]+dy)
                    self.absolutePositions.append(curPosition)
            self.endPosition = curPosition
            return
        if self.type == OrderType.vlineto:
            curPosition = (self.startPosition[0], self.startPosition[1])
            #引数の個数とは無関係に、偶数番がdy、奇数番がdyである。
            for i in range(len(self.args)):
                if i%2 == 1:
                    dx = self.args[i].toNumber()
                    curPosition = (curPosition[0]+dx, curPosition[1])
                    self.absolutePositions.append(curPosition)
                if i%2 == 0:
                    dy = self.args[i].toNumber()
                    curPosition = (curPosition[0], curPosition[1]+dy)
                    self.absolutePositions.append(curPosition)
            self.endPosition = curPosition
            return
        self.endPosition = startPosition

from orderType import *

testSet = OrderSet(OrderType.vlineto, [NumberToken("-569"), NumberToken("569"), NumberToken("569")])
testSet.setAbsolutePosition((15,589))
print(testSet.absolutePositions)
print(testSet.endPosition)
