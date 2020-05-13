from orderParser import *
from analyzer import *

orderstring = """
          -98 805 hstem
          -103 805 vstem
          299 707 rmoveto
          -402 -402 403 -403 402 403 rlineto
          endchar
          """
strParser = StringParser(orderstring)
tokens = strParser.parseString()

tokensParser = TokenListParser(tokens)
orderSets = tokensParser.parseTokens()

analyzer = Analyzer(orderSets)
analyzer.setAbsoluteCoordinate()
print("bounds",analyzer.glyphBoundCalculator())
