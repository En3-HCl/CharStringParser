# CharStringParser
opentypeフォントのCFFテーブルに含まれるCharStringを解析するプログラムです。

[fonttools](https://github.com/fonttools/fonttools)が必須となります。

charstringの詳しい仕様は[仕様書](https://wwwimages.adobe.com/www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5177.Type2.pdf)をご覧ください。

## 使い方

```python
charStringCode = """
0 15 hstem
0 100 vstem
100 hmoveto
-100 hlineto
20 3 10 2 20 10 20 -10 10 -2 20 flex1
endchar
"""

strParser = StringParser(charStringCode)
tokens = strParser.parseString()

tokensParser = TokenListParser(tokens)
orderSets = tokensParser.parseTokens()

analyzer = Analyzer(orderSets)
analyzer.setAbsoluteCoordinate()  //print absolute point list (now incomplete)
```
