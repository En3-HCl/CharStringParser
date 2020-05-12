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
        #絶対座標に直した引数
        self.absoluteArgs = []

    def setAbsolutePosition(self, startPosition):
        if not self.type.isDrawOrder():
            return
        #始点を決定する。
        self.startPosition = startPosition
        #タイプ毎に読んでいく。
        if self.type == OrderType.rmoveto:
            self.absoluteArgs = (self.startPosition[0] + self.args[0].toNumber(), self.startPosition[1] + self.args[1].toNumber())
            self.endPosition = (self.absoluteArgs[0], self.absoluteArgs[1])
            return

        if self.type == OrderType.hmoveto:
            self.absoluteArgs = (self.startPosition[0] + self.args[0].toNumber(), self.startPosition[1])
            self.endPosition = (self.absoluteArgs[0], self.absoluteArgs[1])
            return
        if self.type == OrderType.vmoveto:
            self.absoluteArgs = (self.startPosition[0], self.startPosition[1] + self.args[0].toNumber())
            self.endPosition = (self.absoluteArgs[0], self.absoluteArgs[1])
            return

        if self.type ==  OrderType.rlineto:
            #引数は偶数個とわかっている
            curPosition = (self.startPosition[0], self.startPosition[1])
            for i in range(int(len(self.args)/2)):
                dx = self.args[2*i].toNumber()
                dy = self.args[2*i+1].toNumber()
                curPosition = (curPosition[0]+dx, curPosition[1]+dy)
                self.absoluteArgs.append(curPosition[0])
                self.absoluteArgs.append(curPosition[1])
            self.endPosition = (curPosition[0], curPosition[1])
            return

        self.endPosition = startPosition

from orderType import *

testSet = OrderSet(OrderType.rlineto, [NumberToken("-402"), NumberToken("-402"), NumberToken("403"), NumberToken("-403"),NumberToken("402"),NumberToken("403"),])
testSet.setAbsolutePosition((299,707))
print(testSet.absoluteArgs)
print(testSet.endPosition)
