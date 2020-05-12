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
            if order.type.isDrawOrder():
                order.setAbsolutePosition(curPosition)
                curPosition = order.endPosition
                continue
