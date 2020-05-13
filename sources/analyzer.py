from orderParser import OrderType
from orderSet import OrderSet

class Analyzer:
    #飛翔フォントにおける定数
    ascender = 880

    def __init__(self, orderSets):
        self.orderSets = orderSets    #orderSetのリスト
        print(list(map(lambda x:x.type, self.orderSets)))
        print(list(map(lambda x:list(map(lambda y:y.value,  x.args)), self.orderSets)))

    def yMaxCalculator(self):
        hstem = list(filter(lambda x:x.type == OrderType.hstem, self.orders))[0]
        return self.ascender-max(hstem.value)

    def setAbsoluteCoordinate(self):
        curPosition = (0,0)
        for order in self.orderSets:
            if order.type.isStemOrder() or order.type.isMaskOrder():
                continue
            if order.type.isEndChar():
                break
            if order.type.isDrawOrder() or order.type.isMoveOrder():
                order.setAbsolutePosition(curPosition)
                curPosition = order.endPosition
                continue
        print(list(map(lambda x: x.absolutePositions, self.orderSets)))

    def glyphBoundCalculator(self):
        #!!!必ずsetAbsoluteCoordinateを呼び出してから利用すること!!!
        #各描画命令の領域値をもらってきて、minX, minY, maxX, maxYをそれぞれ更新していく。
        minX, minY, maxX, maxY = None, None, None, None
        for order in self.orderSets:
            if order.type.isStemOrder() or order.type.isMaskOrder() or order.type.isMoveOrder():
                continue
            if order.type.isEndChar():
                break
            if order.type.isDrawOrder():
                order.setBounds()
                print("analyzer",order.type)

                if minX is None:
                    minX, minY, maxX, maxY = order.bounds[0], order.bounds[1], order.bounds[0]+order.bounds[2], order.bounds[1]+order.bounds[3]
                    continue
                orderMinX, orderMinY, orderMaxX, orderMaxY = order.bounds[0], order.bounds[1], order.bounds[0]+order.bounds[2], order.bounds[1]+order.bounds[3]
                minX, minY, maxX, maxY = min(minX, orderMinX), min(minY, orderMinY), max(maxX, orderMaxX), max(maxY, orderMaxY)
        return (minX, minY, maxX-minX, maxY-minY)
