from orderParser import *
from analyzer import *

orderstring = """
          -71 44 413 51 hstemhm
          154.5 49.5 340 38 -38 60 hintmask 11101000
          236 410 rmoveto
          -15 3 -46 -6 -9 -21 -5 -29 -1 -35 rlinecurve
          -1 -19 -2 -22 -4 -27 -7 -111 1 -112 9 -111 26 -16 rcurveline
          27 1 32 4 36 8 rrcurveto
          8 36 23 4 9 hhcurveto
          20 -2 20 0 20 2 rrcurveto
          hintmask 11110000
          27 -2 27 -2 27 -1 27 -1 26 -6 24 -10 19 10 rcurveline
          9 114 -4 145 6 64 rrcurveto
          hintmask 11101000
          2 24 3 38 1 6 3 25 8 38 -11 38 -33 28 -39 8 -69 -17 -26 6 rcurveline
          -23 hlineto
          -60 -4 -58 -8 -55 -12 rrcurveto
          157 -24 rmoveto
          151 hlineto
          -3 -139 -5 -139 -7 -137 -51 -7 rcurveline
          -24 6 -15 -3 -18 6 -21 -3 -27 3 -47 3 -44 -5 -42 -13 rlinecurve
          -13 -3 -12 3 -11 9 2 69 rcurveline
          -2 32 3 93 0 92 11 92 rlinecurve
          23 16 24 10 26 3 9 -3 rcurveline
          10 29 31 5 33 hhcurveto
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
