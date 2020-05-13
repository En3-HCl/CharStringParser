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

        #以降よく使うのでcurPositionをここで宣言する。
        curPosition = self.startPosition

        def processCurPosition(curPosition, dx, dy):
            curPosition = (curPosition[0]+dx, curPosition[1]+dy)
            self.absolutePositions.append(curPosition)
            return curPosition


        if self.type ==  OrderType.rlineto:
            #引数は偶数個とわかっている
            for i in range(int(len(self.args)/2)):
                dx = self.args[2*i].toNumber()
                dy = self.args[2*i+1].toNumber()
                curPosition = processCurPosition(curPosition, dx, dy)
            self.endPosition = (curPosition[0], curPosition[1])
            return

        if self.type == OrderType.hlineto:
            #引数の個数とは無関係に、偶数番がdx、奇数番がdyである。
            for i in range(len(self.args)):
                if i%2 == 0:
                    dx = self.args[i].toNumber()
                    curPosition = processCurPosition(curPosition, dx, 0)
                if i%2 == 1:
                    dy = self.args[i].toNumber()
                    curPosition = processCurPosition(curPosition, 0, dy)
            self.endPosition = curPosition
            return
        if self.type == OrderType.vlineto:
            #引数の個数とは無関係に、偶数番がdy、奇数番がdyである。
            for i in range(len(self.args)):
                if i%2 == 1:
                    dx = self.args[i].toNumber()
                    curPosition = processCurPosition(curPosition, dx, 0)
                if i%2 == 0:
                    dy = self.args[i].toNumber()
                    curPosition = processCurPosition(curPosition, 0, dy)
            self.endPosition = curPosition
            return

        if self.type == OrderType.rrcurveto:
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
        if self.type == OrderType.hhcurveto:
            #引数は4個を1セットで読む。実際の処理としてはこのように実装するのは冗長だが、後の変更を考慮しこのように実装した。
            handle1dy = 0
            if len(self.args)%4 == 1:
                handle1dy = self.args[0].toNumber()
                self.args.pop(0)
            for i in range(int(len(self.args)/4)):
                handle1dx = self.args[4*i].toNumber()
                curPosition = processCurPosition(curPosition, handle1dx, handle1dy)

                handle2dx = self.args[4*i+1].toNumber()
                handle2dy = self.args[4*i+2].toNumber()
                curPosition = processCurPosition(curPosition, handle2dx, handle2dy)

                anchorDx = self.args[4*i+3].toNumber()
                curPosition = processCurPosition(curPosition, anchorDx, 0)

                if not handle1dy == 0:
                    handle1dy = 0
            self.endPosition = curPosition
            return
        if self.type == OrderType.hvcurveto:
            #引数の個数は4+8*n+1? または 8*n+1?である。引数はdx dx dy dy dy dx dy dxを並べたものになるので、それを考慮して処理を簡略化する。
            #4項ずつ見た場合、偶数番目の4項はdx dx dy dy、奇数番目の4項はdy dx dy dxである。
            for i in range(int((len(self.args)-len(self.args)%4)/4)):
                #偶数番目の4項：dx dx dy dy
                if i%2 == 0:
                    handle1dx = self.args[4*i].toNumber()
                    curPosition = processCurPosition(curPosition, handle1dx, 0)

                    handle2dx = self.args[4*i+1].toNumber()
                    handle2dy = self.args[4*i+2].toNumber()
                    curPosition = processCurPosition(curPosition, handle2dx, handle2dy)

                    anchorDy = self.args[4*i+3].toNumber()
                    curPosition = processCurPosition(curPosition, 0, anchorDy)
                #奇数番目の4項：dy dx dy dx
                if i%2 == 1:
                    handle1dy = self.args[4*i].toNumber()
                    curPosition = processCurPosition(curPosition, 0, handle1dy)

                    handle2dx = self.args[4*i+1].toNumber()
                    handle2dy = self.args[4*i+2].toNumber()
                    curPosition = processCurPosition(curPosition, handle2dx, handle2dy)

                    anchorDx = self.args[4*i+3].toNumber()
                    curPosition = processCurPosition(curPosition, anchorDx, 0)

            if len(self.args)%8 == 1:
                #このとき最後の1項dyが存在する。
                dy = self.args[-1].toNumber()
                curPosition = processCurPosition(curPosition, 0,dy)
            if len(self.args)%8 == 5:
                #このとき最後の1項dxが存在する。
                dx = self.args[-1].toNumber()
                curPosition = processCurPosition(curPosition, dx,0)
            self.endPosition = curPosition
            return
        self.endPosition = startPosition

from orderType import *
testSet0 = OrderSet(OrderType.hhcurveto, [
NumberToken("1"), NumberToken("27"), NumberToken("27"), NumberToken("1"),
 NumberToken("28")
])
testSet0.setAbsolutePosition((0,0))

testSet1 = OrderSet(OrderType.hvcurveto, [
NumberToken("28"), NumberToken("26"), NumberToken("-7"), NumberToken("-7"),
 NumberToken("25")
])
testSet1.setAbsolutePosition(testSet0.endPosition)
print(testSet1.absolutePositions)
print(testSet1.endPosition)
