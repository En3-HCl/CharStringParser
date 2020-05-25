from fontTools.misc.bezierTools import *
from charStringOrderType import *
from charStringParser import *

class NumberToken:
    def __init__(self, number):
        self.value = number

    def toNumber(self):
        return float(self.value)
NumberToken.zero = NumberToken("0")
##############################################


#命令情報をまとめるオブジェクト
class CharStringOrder:
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
        """
        args:
         - startPosition: absolute (x, y)
        side effect:
         - initialize `absolutePosition`
         return: None
        """
        if not (self.type.isDrawOrder() or self.type.isMoveOrder()):
            return
        #始点を決定する。
        self.startPosition = startPosition
        #タイプ毎に読んでいく。
        if self.type == CharStringOrderType.rmoveto:
            #stack clearであることから、rmoveto命令が最後の2つを読むようにするためインデックスを-2, -1とした。
            self.absolutePositions = (self.startPosition[0] + self.args[-2].toNumber(), self.startPosition[1] + self.args[-1].toNumber())
            self.endPosition = (self.absolutePositions[0], self.absolutePositions[1])
            return
        #以降よく使うのでcurPositionをここで宣言する。
        curPosition = self.startPosition

        def processCurPosition(curPosition, dx, dy):
            #absolutePositionの計算まで行う。
            curPosition = (curPosition[0]+dx, curPosition[1]+dy)
            self.absolutePositions.append(curPosition)
            return curPosition

        if self.type ==  CharStringOrderType.rlineto:
            #引数は偶数個とわかっている
            for i in range(int(len(self.args)/2)):
                dx = self.args[2*i].toNumber()
                dy = self.args[2*i+1].toNumber()
                curPosition = processCurPosition(curPosition, dx, dy)
            self.endPosition = (curPosition[0], curPosition[1])
            return

        if self.type == CharStringOrderType.rrcurveto:
            #引数は6個を1セットで読む。実際の処理としてはこのように実装するのは冗長だが、後の変更を考慮しこのように実装した。
            for i in range(int(len(self.args)/6)):
                handle1dx = self.args[6*i].toNumber()
                handle1dy = self.args[6*i+1].toNumber()
                curPosition = processCurPosition(curPosition, handle1dx, handle1dy)

                handle2dx = self.args[6*i+2].toNumber()
                handle2dy = self.args[6*i+3].toNumber()
                curPosition = processCurPosition(curPosition, handle2dx, handle2dy)

                anchorDx = self.args[6*i+4].toNumber()
                anchorDy = self.args[6*i+5].toNumber()
                curPosition = processCurPosition(curPosition, anchorDx, anchorDy)

            self.endPosition = curPosition
            return

    def getBounds(self):
        """
        args: None
        return:
         - (minX, minY, maxX, maxY)
        """
        #normalizeを行ってからsetBoundsを呼ぶこと。
        if self.type == CharStringOrderType.rmoveto:
            return (self.startPosition[0], self.startPosition[1], self.startPosition[0], self.startPosition[1])
        if self.type == CharStringOrderType.rlineto:
            #lineTo命令においてはabsolutePositionは全て通過点なので、次の処理で良い。
            xList = list(map(lambda p:p[0],[self.startPosition]+self.absolutePositions))
            yList = list(map(lambda p:p[1],[self.startPosition]+self.absolutePositions))
            minX, maxX = min(xList), max(xList)
            minY, maxY = min(yList), max(yList)
            return (minX, minY, maxX, maxY)

        if self.type == CharStringOrderType.rrcurveto:
            self.absolutePositions += [self.startPosition] #一時的に末尾に追加するが、のちに消す。この位置にあると都合がいい。
            xList, yList = [], []
            for i in range(int(len(self.absolutePositions)/3)):
                anchor1 = self.absolutePositions[3*i-1]
                handle1 = self.absolutePositions[3*i]
                handle2 = self.absolutePositions[3*i+1]
                anchor2 = self.absolutePositions[3*i+2]
                curveBounds = calcCubicBounds(anchor1,handle1,handle2,anchor2)
                xList += [curveBounds[0], curveBounds[2]]
                yList += [curveBounds[1], curveBounds[3]]
            self.absolutePositions.pop(-1)                 #消した
            if len(xList) == 0:
                print(self.type,len(self.args))

            minX, maxX = min(xList), max(xList)
            minY, maxY = min(yList), max(yList)
            return (minX, minY, maxX, maxY)
