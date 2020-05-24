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
    #全ての描画・移動命令をrmoveto/rlineto/rrcurvetoに直す。そうすると処理がとても楽になって嬉しいと思う。
    def normalize(self, normalizedSubrOrdersDict, normalizedGsubrOrdersDict, subrIndexBias, gsubrIndexBias, fdSelectIndex=None):
        normalizedOrders = []
        for i in range(len(self.orders)):
            normalizedOrders += self.orders[i].normalize(normalizedSubrOrdersDict, normalizedGsubrOrdersDict, subrIndexBias, gsubrIndexBias, fdSelectIndex)
        return normalizedOrders
