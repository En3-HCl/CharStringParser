# CharStringParser
opentypeフォントのCFFテーブルに含まれるCharStringを解析するプログラムです。

[fonttools](https://github.com/fonttools/fonttools)が必須となります。

charstringの詳しい仕様は[仕様書](https://wwwimages.adobe.com/www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5177.Type2.pdf)をご覧ください。

## 使い方
コマンドラインにおいて
```
ttx -t CFF fontfile.otf
```
を実行すると、fontfile.ttxが出力されます。このfontfile.ttxの拡張子をxmlに変換したうえで、以下のコードを実行してください。
```python
from CFFParser import *
#絶対パスを指定してCFFParserに読み込ませる。
parser = CFFParser("fontfile.xml")
#calcGlyphsCubicBoundsメソッドは全てのglyphの枠を計算し、{name: (minX, minY, maxX, maxY)}の形で返す。
dict = parser.calcGlyphsCubicBounds()
print(dict)
```
