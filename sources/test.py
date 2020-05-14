from orderParser import *
from analyzer import *

orderstring = """
          57 598 hstem
          1 598 vstem
          511 145 rmoveto
          117 116 0 190 -117 116 -116 117 -190 0 -116 -117 -117 -116 0 -190 117 -116 116 -117 190 0 116 117 rrcurveto
          """
strParser = StringParser(orderstring)
tokens = strParser.parseString()

tokensParser = TokenListParser(tokens)
orderSets = tokensParser.parseTokens()

analyzer = Analyzer(orderSets)
normalizedAnalyzer = Analyzer(analyzer.normalize())
normalizedAnalyzer.setAbsoluteCoordinate()
print(normalizedAnalyzer.glyphBoundCalculator())
