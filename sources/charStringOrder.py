from fontTools.misc.bezierTools import *
from charStringOrderType import *
class NumberToken:
    zero = ""
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

    def normalize(self, normalizedSubrOrdersDict, normalizedGsubrOrdersDict, subrIndexBias, gsubrIndexBias):
        """
        args:
         - normalizedSubrOrdersDict
         - normalizedGsubrOrdersDict
         - subrIndexBias: bias number which is defined by the total number of subrs
         - gsubrIndexBias: bias number which is defined by the total number of gsubrs
        side effect:
         - `normalizedSubrOrdersDict` and `normalizedGsubrOrdersDict` will be added some data
        return:
         - equivalent CharStringOrder expressed by `rmoveto` `rlineto` `rrcurveto`
        """
        if not(self.type.isDrawOrder() or self.type.isMoveOrder()):
            return []
        #内容をrmoveto, rlineto, rrcurvetoのみで表した形の命令列に変換したものを返す。
        if self.type in [CharStringOrderType.rmoveto, CharStringOrderType.rlineto, CharStringOrderType.rrcurveto]:
            return [self]

        if self.type == CharStringOrderType.hmoveto:
            return [CharStringOrder(CharStringOrderType.rmoveto, self.args+[NumberToken.zero])]
        if self.type == CharStringOrderType.vmoveto:
            return [CharStringOrder(CharStringOrderType.rmoveto, [NumberToken.zero]+self.args)]

        if self.type == CharStringOrderType.callsubr:
            pass
        if self.type == CharStringOrderType.callgsubr:
            pass


        #新しい引数を入れる配列。
        newArgs = []

        if self.type == CharStringOrderType.hlineto:
            #引数の個数とは無関係に、偶数番がdx、奇数番がdyである。
            for i in range(len(self.args)):
                if i%2 == 0:
                    newArgs += [self.args[i], NumberToken.zero]
                if i%2 == 1:
                    newArgs += [NumberToken.zero, self.args[i]]
            return [CharStringOrder(CharStringOrderType.rlineto, newArgs)]
        if self.type == CharStringOrderType.vlineto:
            #引数の個数とは無関係に、偶数番がdx、奇数番がdyである。
            for i in range(len(self.args)):
                if i%2 == 1:
                    newArgs += [self.args[i], NumberToken.zero]
                if i%2 == 0:
                    newArgs += [NumberToken.zero, self.args[i]]
            return [CharStringOrder(CharStringOrderType.rlineto, newArgs)]

        #argsに手を加えたいので、加える前にコピーを取って作業する。
        _args = list(map(lambda x: x, self.args))

        if self.type == CharStringOrderType.hhcurveto:
            #引数は4個を1セットで読む。実際の処理としてはこのように実装するのは冗長だが、後の変更を考慮しこのように実装した。
            handle1dy = NumberToken.zero
            if len(_args)%4 == 1:
                handle1dy = _args[0]
                _args.pop(0)
            for i in range(int(len(_args)/4)):
                handle1dx = _args[4*i]
                handle2dx, handle2dy = _args[4*i+1], _args[4*i+2]
                anchorDx, anchorDy = _args[4*i+3], NumberToken.zero

                newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]

                if not handle1dy == NumberToken.zero:
                    handle1dy = NumberToken.zero
            return [CharStringOrder(CharStringOrderType.rrcurveto, newArgs)]
        if self.type == CharStringOrderType.vvcurveto:
            #引数は4個を1セットで読む。実際の処理としてはこのように実装するのは冗長だが、後の変更を考慮しこのように実装した。
            handle1dx = NumberToken.zero
            if len(_args)%4 == 1:
                handle1dx = _args[0]
                _args.pop(0)
            for i in range(int(len(_args)/4)):
                handle1dy = _args[4*i]
                handle2dx, handle2dy = _args[4*i+1], _args[4*i+2]
                anchorDx, anchorDy = NumberToken.zero, _args[4*i+3]

                newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]

                if not handle1dx == NumberToken.zero:
                    handle1dx = NumberToken.zero
            return [CharStringOrder(CharStringOrderType.rrcurveto, newArgs)]
        if self.type == CharStringOrderType.hvcurveto:
            #引数の個数は4+8*n+1? または 8*n+1?である。引数はdx dx dy dy dy dx dy dxを並べたものになるので、それを考慮して処理を簡略化する。
            #4項ずつ見た場合、偶数番目の4項はdx dx dy dy、奇数番目の4項はdy dx dy dxである。
            for i in range(int((len(self.args)-len(self.args)%4)/4)):
                #偶数番目の4項：dx dx dy dy
                if i%2 == 0:
                    handle1dx, handle1dy = self.args[4*i], NumberToken.zero
                    handle2dx, handle2dy = self.args[4*i+1], self.args[4*i+2]
                    anchorDx, anchorDy = NumberToken.zero, self.args[4*i+3]
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
                #奇数番目の4項：dy dx dy dx
                if i%2 == 1:
                    handle1dx, handle1dy = NumberToken.zero, self.args[4*i]
                    handle2dx, handle2dy = self.args[4*i+1], self.args[4*i+2]
                    anchorDx, anchorDy = self.args[4*i+3], NumberToken.zero
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
            if len(self.args)%8 == 1:
                #このとき最後の1項dyが存在する。
                newArgs[-1] = self.args[-1]
            if len(self.args)%8 == 5:
                #このとき最後の1項dxが存在する。
                newArgs[-2] = self.args[-1]
            return [CharStringOrder(CharStringOrderType.rrcurveto, newArgs)]

        if self.type == CharStringOrderType.vhcurveto:
            #引数の個数は4+8*n+1? または 8*n+1?である。引数はdx dx dy dy dy dx dy dxを並べたものになるので、それを考慮して処理を簡略化する。
            #4項ずつ見た場合、偶数番目の4項はdx dx dy dy、奇数番目の4項はdy dx dy dxである。
            for i in range(int((len(self.args)-len(self.args)%4)/4)):
                #奇数番目の4項：dx dx dy dy
                if i%2 == 1:
                    handle1dx, handle1dy = self.args[4*i], NumberToken.zero
                    handle2dx, handle2dy = self.args[4*i+1], self.args[4*i+2]
                    anchorDx, anchorDy = NumberToken.zero, self.args[4*i+3]
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
                #偶数番目の4項：dy dx dy dx
                if i%2 == 0:
                    handle1dx, handle1dy = NumberToken.zero, self.args[4*i]
                    handle2dx, handle2dy = self.args[4*i+1], self.args[4*i+2]
                    anchorDx, anchorDy = self.args[4*i+3], NumberToken.zero
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
            if len(self.args)%8 == 5:
                #このとき最後の1項dyが存在する。
                newArgs[-1] = self.args[-1]
            if len(self.args)%8 == 1:
                #このとき最後の1項dxが存在する。
                newArgs[-2] = self.args[-1]
            return [CharStringOrder(CharStringOrderType.rrcurveto, newArgs)]
        if self.type == CharStringOrderType.rcurveline:
            #rcurvelineはrrcurvetoとrlinetoの合成に等しいというので、教え通りに処理する。
            linetoArgs = self.args[-2:]
            orderSets = []
            #最後の2つを無視して6個ずつ見る。
            for i in range(int((len(self.args)-len(self.args)%6)/6)):
                args = self.args[6*i:6*i+6]
                order = CharStringOrder(CharStringOrderType.rrcurveto, args)
                orderSets.append(order)
            orderSets.append(CharStringOrder(CharStringOrderType.rlineto, linetoArgs))
            return orderSets
        if self.type == CharStringOrderType.rlinecurve:
            #rcurvelineはrlinetoとrrcurvelineの合成に等しいというので、教え通りに処理する。
            curvetoArgs = self.args[-6:]
            orderSets = []
            #最後の6つを無視して2個ずつ見る。
            for i in range(int((len(self.args)-6)/2)):
                args = self.args[2*i:2*i+2]
                order = CharStringOrder(CharStringOrderType.rlineto, args)
                orderSets.append(order)
            orderSets.append(CharStringOrder(CharStringOrderType.rrcurveto, curvetoArgs))
            return orderSets
        if self.type == CharStringOrderType.flex:
            args = self.args[0:12]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]
        if self.type == CharStringOrderType.flex1:
            dx1, dy1 = self.args[0].toNumber(), self.args[1].toNumber()
            dx2, dy2 = self.args[2].toNumber(), self.args[3].toNumber()
            dx3, dy3 = self.args[4].toNumber(), self.args[5].toNumber()
            dx4, dy4 = self.args[6].toNumber(), self.args[7].toNumber()
            dx5, dy5 = self.args[8].toNumber(), self.args[9].toNumber()

            xSum, ySum = abs(dx1+dx2+dx3+dx4+dx5), abs(dy1+dy2+dy3+dy4+dy5)

            args = []
            if xSum <= ySum:
                args = self.args[0:10] + [NumberToken(str(-xSum)), self.args[10]]
            else:
                args = self.args[0:10] + [self.args[10], NumberToken(str(-ySum))]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]
        if self.type == CharStringOrderType.hflex:
            #  dx1 0 dx2 dy2 dx3 0 dx4 0 dx5 dy2 dx6 50 flex
            #= dx1 0 dx2 dy2 dx3 0 dx4 0 dx5 dy2 dx6 rrcurveto
            args = [self.args[0], NumberToken.zero, self.args[1], self.args[2], self.args[3], NumberToken.zero, self.args[4], NumberToken.zero, self.args[5], self.args[2], self.args[6], NumberToken.zero]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]
        if self.type == CharStringOrderType.hflex1:
            #dx1 dy1 dx2 dy2 dx3 0 dx4 0 dx5 dy5 dx6 {-(dy1+dy2+dy5)} rrcurveto
            dy6 = NumberToken(str(-(self.args[1].toNumber() + self.args[3].toNumber() + self.args[7].toNumber())))
            args = [self.args[0], self.args[1], self.args[2], self.args[3], self.args[4], NumberToken.zero, self.args[5], NumberToken.zero, self.args[6], self.args[7], self.args[8], dy6]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]

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
            minX, maxX = min(xList), max(xList)
            minY, maxY = min(yList), max(yList)
            return (minX, minY, maxX, maxY)
