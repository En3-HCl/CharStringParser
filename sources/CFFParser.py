from charStringParser import *
from charStringAnalyzer import *
from xml.etree import ElementTree
import os

class CFFParser:
    def __init__(self, path):
        self.cffString = str
        root = ElementTree.parse(path).getroot()
        cffXML = None
        for child in root:
            if child.tag == "CFF":
                cffXML = child
                break
        if cffXML is None:
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
        self.extension = "ttx"
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
        analyzer = CharStringAnalyzer(orderSets)
        #標準化された命令列を作成し、それを分析するAnalyzerを作成する
        normalizedAnalyzer = CharStringAnalyzer(analyzer.normalize())
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
        self.glyphBoundsDict = dict
        return dict
    def makePath(self,name):
        #nameは拡張子を除いて指定する。拡張子を指定したい場合はCFFParser.extensionに指定する。
        path = f"../results/{name}.{self.extension}"
        i = 1
        while os.path.isfile(path):
            path = f"../results/{name}#{i}.{self.extension}"
            i += 1
        return path

    def writeFile(self, path, text):
        if not os.path.isfile(path):
            with open(path, mode='w') as file:
                file.write(text)
                return
        with open(path, mode='a') as file:
            file.write(text)

    def get_vmtx_and_vhea_table(self):
        glyphsCount = len(self.glyphBoundsDict)
        if glyphsCount == 0:
            self.calcCubicBounds()
        glyphsCount = len(self.glyphBoundsDict)
    #vmtxテーブルとvheaテーブルを生成する
        vmtxPath = self.makePath("vmtx")
        vheaPath = self.makePath("vhea")
        mintsb = self.ascender
        minbsb = -self.descender
        maxYMaxEx = 0
        root = """<?xml version="1.0" encoding="UTF-8"?>
<ttFont sfntVersion="OTTO" ttLibVersion="3.9">
        """
        self.writeFile(vmtxPath, root)

        self.writeFile(vmtxPath, "\n<vmtx>")

        for key in self.glyphBoundsDict.keys():
            yMin = round(self.glyphBoundsDict[key][1])
            yMax = round(self.glyphBoundsDict[key][3])
            tsb = self.ascender - yMax  #ascender - yMax
            bsb = yMin - self.descender #yMin - descender
            yMaxEx = tsb + (yMax - yMin)
            mintsb = min(tsb,mintsb)
            minbsb = min(bsb,minbsb)
            maxYMaxEx = max(yMaxEx, maxYMaxEx)

            element = f'\n<mtx name="{key}" height="{self.height}" tsb="{tsb}"/>'
            self.writeFile(vmtxPath, element)
        self.writeFile(vmtxPath,"\n</vmtx>")
        self.writeFile(vmtxPath,"\n</ttFont>")

        self.writeFile(vheaPath, root)
        vhea = f"""
    <vhea>
    <tableVersion value="0x00011000"/>
    <ascent value="{self.vheaAscent}"/>
    <descent value="{self.vheaDescent}"/>
    <lineGap value="0"/>
    <advanceHeightMax value="{self.height}"/>
    <minTopSideBearing value="{mintsb}"/>
    <minBottomSideBearing value="{minbsb}"/>
    <yMaxExtent value="{maxYMaxEx}"/>
    <caretSlopeRise value="0"/>
    <caretSlopeRun value="1"/>
    <caretOffset value="0"/>
    <reserved1 value="0"/>
    <reserved2 value="0"/>
    <reserved3 value="0"/>
    <reserved4 value="0"/>
    <metricDataFormat value="0"/>
    <numberOfVMetrics value="1"/>
    </vhea>
        """
        self.writeFile(vheaPath, vhea)
        self.writeFile(vheaPath,"\n</ttFont>")
