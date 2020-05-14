import charStringParser as csp
import analyzer as ana

charStringCode = """
          -12 331 hstem
          0 86 vstem
          88 157 rmoveto
          -1 27 -1 28 28 vvcurveto
          28 7 26 7 25 vhcurveto
          -100 -161 rlineto
          -158 vmoveto
          1 27 27 1 28 hhcurveto
          28 26 -7 -7 25 hvcurveto
          -161 100 rlineto
          endchar
          """
#文字列の状態からトークン列へと変換する
strParser = csp.StringParser(charStringCode)
tokens = strParser.parseString()
#トークン列から命令列へと変換する
tokensParser = csp.TokenListParser(tokens)
orderSets = tokensParser.parseTokens()
#命令を分析するAnalyzerを作成する
analyzer = ana.Analyzer(orderSets)
#標準化された命令列を作成し、それを分析するAnalyzerを作成する
normalizedAnalyzer = ana.Analyzer(analyzer.normalize())
#絶対座標を計算する
normalizedAnalyzer.setAbsoluteCoordinate()
#グリフの領域を計算し、(minX, minY, maxX, maxY)を表示する
print(normalizedAnalyzer.glyphBoundCalculator())
