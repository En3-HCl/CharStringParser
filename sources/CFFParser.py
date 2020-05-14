from orderParser import *
from analyzer import *
from xml.etree import ElementTree

class CFFParser:
    def __init__(self, path):
        self.cffString = str
        root = ElementTree.parse(path).getroot()
        cffXML = root[0]
        if cffXML.tag != "CFF":
            print("有効なファイルではありません")
            return
        cffFontXML = None
        for child in cffXML:
            if child.tag == "CFFFont":
                cffFontXML = child
                break
        if cffFontXML is None:
            print("CFFFontテーブルが見つかりませんでした")
            return
        charstringsXML = None
        for child in cffFontXML:
            if child.tag == "CharStrings":
                charstringsXML = child
                break
        if charstringsXML is None:
            print("CharStringsテーブルが見つかりませんでした")
            return
        #CharStringを格納するコード。
        charStringsDict = {}
        for child in charstringsXML:
            charStringsDict[child.attrib["name"]] = child.text
        self.charStringsDict = charStringsDict
    def calcCubicBounds(self,name):
    #指定されたグリフのboundsを(minX, minY, maxX, maxY)の形で返す
        if self.charStringsDict[name] is None:
            print("データがありません")
            return
        charStringCode = self.charStringsDict[name]
        #文字列の状態からトークン列へと変換する
        strParser = StringParser(charStringCode)
        tokens = strParser.parseString()
        #トークン列から命令列へと変換する
        tokensParser = TokenListParser(tokens)
        orderSets = tokensParser.parseTokens()
        #命令を分析するAnalyzerを作成する
        analyzer = Analyzer(orderSets)
        #標準化された命令列を作成し、それを分析するAnalyzerを作成する
        normalizedAnalyzer = Analyzer(analyzer.normalize())
        #絶対座標を計算する
        normalizedAnalyzer.setAbsoluteCoordinate()
        #グリフの領域を計算し、(minX, minY, maxX, maxY)を表示する
        bounds = normalizedAnalyzer.glyphBoundCalculator()
        return bounds
    def calcGlyphsCubicBounds(self):
    #全てのグリフのboundsを{name: (minX, minY, maxX, maxY)}の形で返す
        dict = {}
        for key in self.charStringsDict.keys():
            dict[key] = self.calcCubicBounds(key)
        return dict
