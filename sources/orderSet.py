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
        self.startPosition = startPosition
        self.endPosition = startPosition
