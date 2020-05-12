from orderParser import *
from analyzer import *
orderstring = """
          114 37 -23 21 -21 27 116 25 149 30 23 53 -34 24 -24 49 88 49 -46 56 -45 52 67 53 -46 57 hstemhm
          23 67 -63 59 211 43 5 70 -63.5 63.5 110 53 21 62.5 -62.5 64 -17 45 -17 8 242 67 -64 64 hintmask 00000000000000000000000000000000
          hintmask 00000001000011001000000000000000
          398 510 rmoveto
          14 18 -3 13 rlineto
          4 45 2 45 46 vvcurveto
          46 3 44 7 43 vhcurveto
          -10 21 -93 22 -96 4 -98 -14 rlinecurve
          -9 4 -31 4 -28 -3 -27 -10 rlinecurve
          -7 -101 -3 -100 -99 vvcurveto
          4 -13 rlineto
          hintmask 00000001000000100000000000000000
          -4 -15 4 -15 rlineto
          hintmask 01000000000001000000000000000000
          -4 -19 4 -8 rlineto
          hintmask 00000001000000100000000000000000
          -1 -183 -3 -181 -7 -179 35 -22 rcurveline
          15 6 7 22 -9 8 6 10 11 183 6 184 -1 185 rlinecurve
          35 -12 rlineto
          hintmask 00000001000011001000000000000000
          93 28 93 7 91 -14 rrcurveto
          hintmask 00000100000100000000100010000000
          603 279 rmoveto
          -6 27 -23 10 -23 8 -25 6 rlinecurve
          -59 3 -47 0 -37 -3 -37 -3 -27 -1 -17 -1 -16 3 rcurveline
          -32 -5 -33 -4 -33 -3 13 -73 5 -74 -5 -77 5 -22 -5 -19 -13 -17 10 -34 rcurveline
          40 -15 95 5 95 2 95 -1 rlinecurve
          11 -90 2 -91 -7 -92 -1 -96 -3 -95 -5 -95 -3 -20 2 -18 7 -16 11 -19 rcurveline
          19 -5 16 5 11 13 10 294 7 294 3 294 -3 9 rcurveline
          hintmask 00000000010011000100000000000000
          -898 16 rmoveto
          3 85 85 2 85 hhcurveto
          -7 -81 -26 7 -29 3 -31 -3 rlinecurve
          -98 -7 -27 -3 -24 2 -23 6 rlinecurve
          -3 27 4 23 9 21 rrcurveto
          hintmask 00000010100100100000100000000000
          821 -98 rmoveto
          -111 12 -49 2 -45 -3 -43 -9 rlinecurve
          -13 7 6 73 111 18 89 1 66 -16 rlinecurve
          -846 -232 rmoveto
          hintmask 00000000010000100000000000000000
          2 15 -2 10 2 8 -2 22 -5 25 3 21 10 18 rlinecurve
          11 3 9 -2 7 -7 rrcurveto
          hintmask 00000001001000001000000000000000
          47 2 43 4 40 5 40 5 33 -4 27 -12 -6 -77 rcurveline
          -14 vlineto
          -40 -3 -40 -4 -41 -5 rrcurveto
          hintmask 00000010000000100000000000000000
          -41 -5 -42 -5 -41 -3 rrcurveto
          hintmask 00000100100000000001000100000000
          818 5 rmoveto
          -28 7 -160 -4 -64 4 -9 73 3 10 150 18 rlineto
          37 34 -4 -8 33 hvcurveto
          10 -40 -3 -9 3 -10 2 -14 -2 -12 -6 -11 rlinecurve
          hintmask 01001000000000000010001000000000
          -496 -102 rmoveto
          19 -7 20 5 20 2 19 1 rlinecurve
          38 3 36 -2 32 -8 102 -126 -11 23 97 -64 19 -8 rcurveline
          21 1 5 6 -90 69 16 -8 -114 123 rlinecurve
          -30 9 -30 7 -29 5 -9 -2 rcurveline
          -16 4 rlineto
          -2 -21 -23 0 -23 hhcurveto
          -21 -21 -3 -6 -18 hvcurveto
          1 -9 4 -7 7 -6 rrcurveto
          -72 -19 rmoveto
          -3 14 -36 15 -5 -1 -25 -122 -10 46 -106 -116 rlinecurve
          3 -14 16 -10 10 -1 7 1 7 3 rlinecurve
          98 95 -25 -74 69 164 rrcurveto
          501 -493 rmoveto
          -86 -1 -88 0 -88 1 -11 10 rcurveline
          87 vlineto
          -4 42 rlineto
          -3 9 -1 -12 15 vvcurveto
          14 -3 -45 4 74 vhcurveto
          17 2 31 4 27 -6 28 -7 rlinecurve
          9 10 rlineto
          hintmask 01010000000000010000010000000000
          -2 25 rlineto
          4 22 3 23 22 vvcurveto
          23 3 -40 1 22 vhcurveto
          -2 57 -10 9 -14 5 -15 1 rlinecurve
          -4 -52 -53 0 -53 hhcurveto
          -1 hlineto
          -8 2 rlineto
          -123 hlineto
          -19 -1 -21 -3 -20 -7 rrcurveto
          -2 -67 -2 -6 -68 vvcurveto
          9 -6 -5 -8 rlineto
          -5 vlineto
          -13 14 18 -6 20 hhcurveto
          5 hlineto
          -61 -104 -21 14 -66 -104 rrcurveto
          -7 vlineto
          26 -15 6 -1 4 2 5 3 rlinecurve
          hintmask 10000000000000010010000000000000
          59 91 23 -11 73 120 -3 10 rcurveline
          10 vlineto
          33 6 31 3 29 -1 11 2 10 -2 8 -4 -1 -95 6 23 5 -94 14 -29 rcurveline
          13 -7 15 -7 14 -5 47 3 rcurveline
          22 -3 9 3 129 -3 28 -1 25 4 22 7 rlinecurve
          -7 12 rlineto
          hintmask 01010000000000010000010000000000
          -338 223 rmoveto
          -23 2 -49 -2 -49 -4 -46 -5 rlinecurve
          -21 3 rlineto
          95 vlineto
          33 3 -38 4 28 vhcurveto
          6 92 89 4 91 hhcurveto
          5 -3 11 3 11 -4 rlineto
          hintmask 00100000000000000000010000000000
          1 -16 0 -16 1 -9 -11 -73 rcurveline
          -11 2 rlineto
          hintmask 01010000000000010000010000000000
          -31 -1 -33 -2 -34 -3 rrcurveto
          46 -78 rmoveto
          -1 vlineto
          -1 7 0 -1 1 -5 rrcurveto
          endchar
          """
strParser = StringParser(orderstring)
tokens = strParser.parseString()

tokensParser = TokenListParser(tokens)
orderSets = tokensParser.parseTokens()

analyzer = Analyzer(orderSets)
analyzer.setAbsoluteCoordinate()
