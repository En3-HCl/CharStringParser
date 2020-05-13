from orderParser import *
from analyzer import *
orderstring = """
          20 3 10 2 20 10 20 -10 10 -2 20 flex1
          """
strParser = StringParser(orderstring)
tokens = strParser.parseString()

tokensParser = TokenListParser(tokens)
orderSets = tokensParser.parseTokens()

analyzer = Analyzer(orderSets)
analyzer.setAbsoluteCoordinate()
print(analyzer.glyphBoundCalculator())
