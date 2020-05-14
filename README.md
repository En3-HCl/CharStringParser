# CharStringParser
opentypeフォントのCFFテーブルに含まれるCharStringを解析するプログラムです。

[fonttools](https://github.com/fonttools/fonttools)が必須となります。

charstringの詳しい仕様は[仕様書](https://wwwimages.adobe.com/www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5177.Type2.pdf)をご覧ください。

## 使い方

```python
from orderParser import *
from analyzer import *

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
print(normalizedAnalyzer.glyphBoundCalculator())
```
