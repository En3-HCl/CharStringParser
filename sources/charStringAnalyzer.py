from charStringParser import *
from charStringOrder import *

class CharStringAnalyzer:
    #飛翔フォントにおける定数
    ascender = 880

    def __init__(self, orders):
        self.orders = orders    #CharStringOrderのリスト

    def yMaxCalculator(self):
        hstem = list(filter(lambda x:x.type == OrderType.hstem, self.orders))[0]
        return self.ascender-max(hstem.value)

    def setAbsoluteCoordinate(self):
        curPosition = (0,0)
        for order in self.orders:
            if order.type.isStemOrder() or order.type.isMaskOrder():
                continue
            if order.type.isEndOrder():
                break
            if order.type.isDrawOrder() or order.type.isMoveOrder():
                order.setAbsolutePosition(curPosition)
                curPosition = order.endPosition
                continue

    def glyphBoundCalculator(self):
        #!!!必ずsetAbsoluteCoordinateを呼び出してから利用すること!!!
        #返り値は (minX, minY, maxX, maxY)
        #各描画命令の領域値をもらってきて、minX, minY, maxX, maxYをそれぞれ更新していく。
        minX, minY, maxX, maxY = None, None, None, None
        for order in self.orders:
            if order.type.isStemOrder() or order.type.isMaskOrder() or order.type.isMoveOrder():
                continue
            if order.type.isEndOrder():
                break
            if order.type.isDrawOrder():
                bounds = order.getBounds()
                if minX is None:
                    minX, minY, maxX, maxY = bounds[0], bounds[1], bounds[2], bounds[3]
                    continue
                orderMinX, orderMinY, orderMaxX, orderMaxY = bounds[0], bounds[1], bounds[2], bounds[3]
                minX, minY, maxX, maxY = min(minX, orderMinX), min(minY, orderMinY), max(maxX, orderMaxX), max(maxY, orderMaxY)
        if minX is None:
            return (0,0,0,0)
        return (minX, minY, maxX, maxY)


    def expand(self, cffData, fdSelectIndex = None, subrFlag = False):
        """
        summary:
         - remove `callsubr` and `callgsubr` orders
        """
        expandedOrders = []
        for i in range(len(self.orders)):
            expandedOrders += self.expandOrder(self.orders[i], cffData, fdSelectIndex)


        unitestackOrders = []
        for i in range(len(expandedOrders)):
            if i == len(expandedOrders)-1:
                unitestackOrders.append(expandedOrders[i])
                break
            if expandedOrders[i].type == CharStringOrderType._stack and expandedOrders[i+1].type == CharStringOrderType._stack:
                expandedOrders[i+1] = CharStringOrder(CharStringOrderType._stack, expandedOrders[i].args + expandedOrders[i+1].args)
                continue
            unitestackOrders.append(expandedOrders[i])

        if subrFlag:
            return unitestackOrders

        nostackOrders = []

        for i in range(len(unitestackOrders)):
            if i == len(unitestackOrders)-1:
                nostackOrders.append(unitestackOrders[i])
                break
            if unitestackOrders[i].type ==  CharStringOrderType.hstemhm and unitestackOrders[i+1].type == CharStringOrderType._stack:
                hstem = CharStringOrder(CharStringOrderType.hstem, unitestackOrders[i].args)
                vstem = CharStringOrder(CharStringOrderType.vstem, unitestackOrders[i+1].args)
                nostackOrders.append(hstem)
                unitestackOrders[i+1] = vstem
                continue
            if unitestackOrders[i].type == CharStringOrderType._stack:
                if unitestackOrders[i+1].type == CharStringOrderType.hintmask:
                    nostackOrders[-1] = CharStringOrder(nostackOrders[-1].type, nostackOrders[-1].args+unitestackOrders[i].args)
                    continue
                unitestackOrders[i+1] = CharStringOrder(unitestackOrders[i+1].type, unitestackOrders[i].args + unitestackOrders[i+1].args)
                continue
            nostackOrders.append(unitestackOrders[i])
        return nostackOrders

    def expandOrder(self, order, cffData, fdSelectIndex = None):
        """
        args:
         - order
         - cffData
         - fdSelectIndex: if needed
        return:
         - [CharStringOrder] without callsubr
        """
        if not order.type in [CharStringOrderType.callsubr, CharStringOrderType.callgsubr]:
            return [order]
        if order.type == CharStringOrderType.callsubr:
            index = str(int(order.args[-1].toNumber() + cffData.subrIndexBias))
            print("subr:",index,"from:",order.args[-1].toNumber())
            if cffData.hasFontDict:
                expandedSubrOrdersSelectedDict = cffData.expandedSubrOrdersDict[fdSelectIndex]
                #すでに呼び出すsubrがnormalizeされていた場合
                if index in expandedSubrOrdersSelectedDict.keys():
                    expandedOrders = expandedSubrOrdersSelectedDict[index]
                    return expandedOrders
                #されていない場合
                else:
                    if not index in cffData.subrCharStringDict[fdSelectIndex].keys():
                        print(f"{index}に対応するデータがありません")
                        return
                    charStringCode = cffData.subrCharStringDict[fdSelectIndex][index]
                    #文字列の状態からトークン列へと変換する
                    strParser = CharStringParser(charStringCode)
                    tokens = strParser.parseString()
                    #トークン列から命令列へと変換する
                    tokensParser = TokenListParser(tokens)
                    orders = tokensParser.parseTokens()
                    #命令を分析するAnalyzerを作成する
                    analyzer = CharStringAnalyzer(orders)
                    expandedOrders = analyzer.expand(cffData, fdSelectIndex = fdSelectIndex, subrFlag = True)
                    #標準化された命令列を作成し、それを分析するAnalyzerを作成する。
                    #副作用としてexpanded(G)SubrOrdersDictは更新される。
                    cffData.expandedSubrOrdersDict[fdSelectIndex][index] = expandedOrders
                    return expandedOrders
            #FontDictでないタイプの場合
            else:
                if index in cffData.expandedSubrOrdersDict.keys():
                    expandedOrders = cffData.expandedSubrOrdersDict[index]
                    return expandedOrders
                else:
                    if not index in cffData.subrCharStringDict.keys():
                        print(f"{index}に対応するデータがありません")
                        return
                    charStringCode = cffData.subrCharStringDict[index]
                    #文字列の状態からトークン列へと変換する
                    strParser = CharStringParser(charStringCode)
                    tokens = strParser.parseString()
                    #トークン列から命令列へと変換する
                    tokensParser = TokenListParser(tokens)
                    orders = tokensParser.parseTokens()
                    #命令を分析するAnalyzerを作成する
                    analyzer = CharStringAnalyzer(orders)
                    #標準化された命令列を作成し、それを分析するAnalyzerを作成する。
                    #副作用としてexpanded(G)SubrOrdersDictは更新される。
                    expandedOrders = analyzer.expand(cffData, subrFlag = True)
                    cffData.expandedSubrOrdersDict[index] = expandedOrders
                    return expandedOrders

        if order.type == CharStringOrderType.callgsubr:
            index = str(int(order.args[-1].toNumber() + cffData.gsubrIndexBias))
            print("gsubr:",index,"from:",order.args[-1].toNumber())
            if index in cffData.expandedGsubrOrdersDict.keys():
                expandedOrders = cffData.expandedGsubrOrdersDict[index]
                addArgs = order.args[0:-1]
                print(len(addArgs))

                return [CharStringOrder(expandedOrders[0].type, addArgs + expandedOrders[0].args)] + expandedOrders[1:]
            else:
                if not index in cffData.gsubrCharStringDict.keys():
                    print(f"{index}に対応するデータがありません")
                    return
                charStringCode = cffData.gsubrCharStringDict[index]
                #文字列の状態からトークン列へと変換する
                strParser = CharStringParser(charStringCode)
                tokens = strParser.parseString()
                #トークン列から命令列へと変換する
                tokensParser = TokenListParser(tokens)
                orders = tokensParser.parseTokens()
                #命令を分析するAnalyzerを作成する
                analyzer = CharStringAnalyzer(orders)
                #標準化された命令列を作成し、それを分析するAnalyzerを作成する。
                #副作用としてexpanded(G)SubrOrdersDictは更新される。
                expandedOrders = analyzer.expand(cffData, subrFlag = True)
                cffData.expandedGsubrOrdersDict[index] = expandedOrders
                return expandedOrders

    #全ての描画・移動命令をrmoveto/rlineto/rrcurvetoに直す。そうすると処理がとても楽になって嬉しいと思う。
    def normalize(self):
        normalizedOrders = []
        for i in range(len(self.orders)):
            print(i,self.orders[i].type)
            normalizedOrders += self.normalizeOrder(self.orders[i])
        return normalizedOrders

    def normalizeOrder(self, order):
        """
        args:
         - order
         - cffData
         - fdSelectIndex: if needed
        side effect:
         - `cffData.normalizedSubrOrdersDict` and `cffData.normalizedGsubrOrdersDict` will be added some data
        return:
         - equivalent CharStringOrder expressed by `rmoveto` `rlineto` `rrcurveto`
        """
        if not(order.type.isDrawOrder() or order.type.isMoveOrder()):
            return []
        #内容をrmoveto, rlineto, rrcurvetoのみで表した形の命令列に変換したものを返す。
        if order.type in [CharStringOrderType.rmoveto, CharStringOrderType.rlineto, CharStringOrderType.rrcurveto]:
            return [order]

        if order.type == CharStringOrderType.hmoveto:
            return [CharStringOrder(CharStringOrderType.rmoveto, order.args+[NumberToken.zero])]
        if order.type == CharStringOrderType.vmoveto:
            return [CharStringOrder(CharStringOrderType.rmoveto, [NumberToken.zero]+order.args)]

        #新しい引数を入れる配列。
        newArgs = []

        if order.type == CharStringOrderType.hlineto:
            #引数の個数とは無関係に、偶数番がdx、奇数番がdyである。
            for i in range(len(order.args)):
                if i%2 == 0:
                    newArgs += [order.args[i], NumberToken.zero]
                if i%2 == 1:
                    newArgs += [NumberToken.zero, order.args[i]]
            return [CharStringOrder(CharStringOrderType.rlineto, newArgs)]
        if order.type == CharStringOrderType.vlineto:
            #引数の個数とは無関係に、偶数番がdx、奇数番がdyである。
            for i in range(len(order.args)):
                if i%2 == 1:
                    newArgs += [order.args[i], NumberToken.zero]
                if i%2 == 0:
                    newArgs += [NumberToken.zero, order.args[i]]
            return [CharStringOrder(CharStringOrderType.rlineto, newArgs)]

        #argsに手を加えたいので、加える前にコピーを取って作業する。
        _args = list(map(lambda x: x, order.args))

        if order.type == CharStringOrderType.hhcurveto:
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
        if order.type == CharStringOrderType.vvcurveto:
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
        if order.type == CharStringOrderType.hvcurveto:
            #引数の個数は4+8*n+1? または 8*n+1?である。引数はdx dx dy dy dy dx dy dxを並べたものになるので、それを考慮して処理を簡略化する。
            #4項ずつ見た場合、偶数番目の4項はdx dx dy dy、奇数番目の4項はdy dx dy dxである。
            for i in range(int((len(order.args)-len(order.args)%4)/4)):
                #偶数番目の4項：dx dx dy dy
                if i%2 == 0:
                    handle1dx, handle1dy = order.args[4*i], NumberToken.zero
                    handle2dx, handle2dy = order.args[4*i+1], order.args[4*i+2]
                    anchorDx, anchorDy = NumberToken.zero, order.args[4*i+3]
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
                #奇数番目の4項：dy dx dy dx
                if i%2 == 1:
                    handle1dx, handle1dy = NumberToken.zero, order.args[4*i]
                    handle2dx, handle2dy = order.args[4*i+1], order.args[4*i+2]
                    anchorDx, anchorDy = order.args[4*i+3], NumberToken.zero
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
            if len(order.args)%8 == 1:
                #このとき最後の1項dyが存在する。
                newArgs[-1] = order.args[-1]
            if len(order.args)%8 == 5:
                #このとき最後の1項dxが存在する。
                newArgs[-2] = order.args[-1]
            return [CharStringOrder(CharStringOrderType.rrcurveto, newArgs)]

        if order.type == CharStringOrderType.vhcurveto:
            #引数の個数は4+8*n+1? または 8*n+1?である。引数はdx dx dy dy dy dx dy dxを並べたものになるので、それを考慮して処理を簡略化する。
            #4項ずつ見た場合、偶数番目の4項はdx dx dy dy、奇数番目の4項はdy dx dy dxである。
            for i in range(int((len(order.args)-len(order.args)%4)/4)):
                #奇数番目の4項：dx dx dy dy
                if i%2 == 1:
                    handle1dx, handle1dy = order.args[4*i], NumberToken.zero
                    handle2dx, handle2dy = order.args[4*i+1], order.args[4*i+2]
                    anchorDx, anchorDy = NumberToken.zero, order.args[4*i+3]
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
                #偶数番目の4項：dy dx dy dx
                if i%2 == 0:
                    handle1dx, handle1dy = NumberToken.zero, order.args[4*i]
                    handle2dx, handle2dy = order.args[4*i+1], order.args[4*i+2]
                    anchorDx, anchorDy = order.args[4*i+3], NumberToken.zero
                    newArgs += [handle1dx, handle1dy] + [handle2dx, handle2dy] + [anchorDx, anchorDy]
            if len(order.args)%8 == 5:
                #このとき最後の1項dyが存在する。
                newArgs[-1] = order.args[-1]
            if len(order.args)%8 == 1:
                #このとき最後の1項dxが存在する。
                newArgs[-2] = order.args[-1]
            return [CharStringOrder(CharStringOrderType.rrcurveto, newArgs)]
        if order.type == CharStringOrderType.rcurveline:
            #rcurvelineはrrcurvetoとrlinetoの合成に等しいというので、教え通りに処理する。
            linetoArgs = order.args[-2:]
            orders = []
            #最後の2つを無視して6個ずつ見る。
            for i in range(int((len(order.args)-2)/6)):
                args = order.args[6*i:6*i+6]
                newOrder = CharStringOrder(CharStringOrderType.rrcurveto, args)
                orders.append(newOrder)
            orders.append(CharStringOrder(CharStringOrderType.rlineto, linetoArgs))
            return orders
        if order.type == CharStringOrderType.rlinecurve:
            #rcurvelineはrlinetoとrrcurvelineの合成に等しいというので、教え通りに処理する。
            curvetoArgs = order.args[-6:]
            orders = []
            #最後の6つを無視して2個ずつ見る。
            for i in range(int((len(order.args)-6)/2)):
                args = order.args[2*i:2*i+2]
                newOrder = CharStringOrder(CharStringOrderType.rlineto, args)
                orders.append(newOrder)
            orders.append(CharStringOrder(CharStringOrderType.rrcurveto, curvetoArgs))
            return orders
        if order.type == CharStringOrderType.flex:
            args = order.args[0:12]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]
        if order.type == CharStringOrderType.flex1:
            dx1, dy1 = order.args[0].toNumber(), order.args[1].toNumber()
            dx2, dy2 = order.args[2].toNumber(), order.args[3].toNumber()
            dx3, dy3 = order.args[4].toNumber(), order.args[5].toNumber()
            dx4, dy4 = order.args[6].toNumber(), order.args[7].toNumber()
            dx5, dy5 = order.args[8].toNumber(), order.args[9].toNumber()

            xSum, ySum = abs(dx1+dx2+dx3+dx4+dx5), abs(dy1+dy2+dy3+dy4+dy5)

            args = []
            if xSum <= ySum:
                args = order.args[0:10] + [NumberToken(str(-xSum)), order.args[10]]
            else:
                args = order.args[0:10] + [order.args[10], NumberToken(str(-ySum))]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]
        if order.type == CharStringOrderType.hflex:
            #  dx1 0 dx2 dy2 dx3 0 dx4 0 dx5 dy2 dx6 50 flex
            #= dx1 0 dx2 dy2 dx3 0 dx4 0 dx5 dy2 dx6 rrcurveto
            args = [order.args[0], NumberToken.zero, order.args[1], order.args[2], order.args[3], NumberToken.zero, order.args[4], NumberToken.zero, order.args[5], order.args[2], order.args[6], NumberToken.zero]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]
        if order.type == CharStringOrderType.hflex1:
            #dx1 dy1 dx2 dy2 dx3 0 dx4 0 dx5 dy5 dx6 {-(dy1+dy2+dy5)} rrcurveto
            dy6 = NumberToken(str(-(order.args[1].toNumber() + order.args[3].toNumber() + order.args[7].toNumber())))
            args = [order.args[0], order.args[1], order.args[2], order.args[3], order.args[4], NumberToken.zero, order.args[5], NumberToken.zero, order.args[6], order.args[7], order.args[8], dy6]
            return [CharStringOrder(CharStringOrderType.rrcurveto, args)]
