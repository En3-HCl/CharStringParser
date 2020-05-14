from orderParser import *
from analyzer import *

orderstring = """
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
strParser = StringParser(orderstring)
tokens = strParser.parseString()

tokensParser = TokenListParser(tokens)
orderSets = tokensParser.parseTokens()

analyzer = Analyzer(orderSets)
normalizedAnalyzer = Analyzer(analyzer.normalize())
normalizedAnalyzer.setAbsoluteCoordinate()
print(normalizedAnalyzer.glyphBoundCalculator())
