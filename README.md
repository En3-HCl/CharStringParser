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
を実行すると、fontfile.ttxがresultsディレクトリに出力されます。後者のコマンドはCFFテーブルのみを出力するので効率が良くなります。

その上で以下のコードを実行してください。

⚠️現在下記コードはCharStringParser/Sources/においてpython3を実行した場合のみ動作します。対処法は検討中です。

```python
from CFFParser import *
#絶対パスを指定してCFFParserに読み込ませる。
parser = CFFParser("fontfile.ttx")
#calcGlyphsCubicBoundsメソッドは全てのglyphの枠を計算し、{name: (minX, minY, maxX, maxY)}の形で返す。
dict = parser.calcGlyphsCubicBounds()
parser.extension = "ttx"        #デフォルトではttxとなっているので必須ではない

#フォントの構造に関する情報を与える
parser.ascender = 880
parser.descender = -120 #descenderは負の数値で指定すること
parser.height = 1000

parser.vheaAscent = 512
parser.vheaDescent = -512

#vmtxとvheaのttxファイルをcharstring/resultsに出力する
parser.get_vmtx_and_vhea_table()
```
## 未対応の命令
 - `add`などの計算
 - `callsubr`命令
 - `return`命令
