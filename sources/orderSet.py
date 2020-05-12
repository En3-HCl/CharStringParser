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
            self.endPosition = (self.args[0].toNumber(), self.args[1].toNumber())
            return

        self.endPosition = startPosition

from orderType import *

testSet = OrderSet(OrderType.rmoveto, [NumberToken("10"),NumberToken("20")])
testSet.setAbsolutePosition((0,0))
print(testSet.endPosition)
