# CharStringParser
opentypeフォントのCFFテーブルに含まれるCharStringを解析するプログラムです。

[fonttools](https://github.com/fonttools/fonttools)が必須となります。

charstringの詳しい仕様は[仕様書](https://wwwimages.adobe.com/www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5177.Type2.pdf)をご覧ください。

## 使い方
コマンドラインにおいて
```
ttx fontfile.otf
```
または
```
ttx -t CFF fontfile.otf
```
を実行すると、fontfile.ttxが出力されます。後者のコマンドはCFFテーブルのみを出力するので効率は後者の方が良くなります。

その上で以下のコードを実行してください。

⚠️現在下記コードはCharStringParser/Souces/においてpython3を実行した場合のみ動作します。対処法は検討中です。

```python
from CFFParser import *
#絶対パスを指定してCFFParserに読み込ませる。
parser = CFFParser("fontfile.ttx")
#calcGlyphsCubicBoundsメソッドは全てのglyphの枠を計算し、{name: (minX, minY, maxX, maxY)}の形で返す。
dict = parser.calcGlyphsCubicBounds()
print(dict)
```
