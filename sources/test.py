from CFFParser import *
#絶対パスを指定してCFFParserに読み込ませる。
parser = CFFParser("/Users/en3_hcl_k/Desktop/CharStringTest-Regular.ttx")
#calcGlyphsCubicBoundsメソッドは全てのglyphの枠を計算し、{name: (minX, minY, maxX, maxY)}の形で返す。

dict = parser.calcGlyphsCubicBounds()
parser.extension = "ttx"        #デフォルトではttxとなっている
#フォントの構造に関する情報を与える
parser.ascender = 880
parser.descender = -120 #descenderは負の数値で指定すること
parser.height = 1000

parser.vheaAscent = 512
parser.vheaDescent = -512

#ファイルを出力する(charstring/results内にファイルが出ます)
parser.get_vmtx_and_vhea_table()
