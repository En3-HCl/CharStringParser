from charStringOrder import *
from charStringOrderType import *
#charstringをパースする
#流れは
#1. 文字列を数値と命令のトークンの列に変換する。
#2. トークンの列をオブジェクトの列に変換する。
#で行う。

class CharStringParser:

    def __init__(self, string):
        self.string = string
        self.count = len(string)
        self.stringIter = iter(string)
        self.curChar = "" #現在処理中の文字を格納する。
        self.result = []
    #次の1文字をcurCharに格納する。
    def next(self):
        if self.count == 0:
            self.curChar = "last"
            return
        self.count = self.count-1
        self.curChar = next(self.stringIter)

    #文字列となっている命令情報をパースしてトークン列に変換する。
    def parseString(self):
        while True:
            self.next()                     #後のparseTokensとはnextの位置が違うことに注意
            if self.curChar.isdecimal():
                self.parseNumber()
                continue
            if self.curChar == "-":
                self.parseNumber()
                continue
            if self.curChar == " ":
                continue
            if self.curChar == "\n":
                continue
            if self.curChar == "last":
                return self.result
                continue
            self.parseIdentifier()

    #数値をパースする。
    def parseNumber(self):
        number = self.curChar
        while True:
            self.next()
            if self.curChar in ["last", " ", "\n"]:
                self.result.append(NumberToken(number))
                return
            if self.curChar.isdecimal():
                number = number + self.curChar
            if self.curChar == ".":                             #小数点が複数存在する可能性は無視する。ありえないから。
                number = number + self.curChar

    #文字列(識別子)をパースする。
    def parseIdentifier(self):
        identifier = self.curChar
        while True:
            self.next()
            if self.curChar in ["last", " ", "\n"]:
                order = CharStringOrderType.getOrder(identifier)
                self.result.append(order)
                return
            identifier = identifier + self.curChar
##############################################
class TokenListParser:
    def __init__(self, tokens):
        self.stack = []
        self.count = 0
        self.curToken = ""
        self.tokens = tokens

    #次のトークンをcurTokenに格納する。
    def next(self):
        if self.count == len(self.tokens):
            self.curToken = "last"
            return
        self.curToken = self.tokens[self.count]
        self.count = self.count+1

    #トークン列をパースしてCharStringOrderオブジェクトの列にする。
    def parseTokens(self):
        orders = []

        #処理を行う。
        #パースは次の考え方で行う。
        # 1.命令は前置と後置が混ざっているため、命令を中心にパースする。
        # 2.命令がわからない段階では数値はstackに入れておく。
        # 3.命令がわかったらまとめてCharStringOrderオブジェクトとする。

        while True:
            #CharStringOrderオブジェクトの列を返して終了する。
            if self.curToken == "last":
                return orders
            if type(self.curToken) is str:
                self.next()
                continue
            #数値列の部分を読み取る。終了時点で命令がcurTokenとなる。
            if type(self.curToken) is NumberToken:
                self.parseNumberTokens()
                continue
            #後置命令のため、stackの数値列を受け取ってオブジェクトとする。
            if self.curToken.isPostfix():
                order = CharStringOrder(self.curToken, self.stack)
                self.stack = []
                orders.append(order)
                self.next()
                continue
            if self.curToken.isUniquefix():
                #後置命令だが直後のvstemは記述されないため、vstemの分までパースする。
                if self.curToken == CharStringOrderType.hstemhm:
                    hstem = CharStringOrder(CharStringOrderType.hstem, self.stack)
                    orders.append(hstem)

                    self.next()
                    self.parseNumberTokens()
                    vstem = CharStringOrder(CharStringOrderType.vstem, self.stack)
                    orders.append(vstem)
                    continue
                #endchar/returnが出てきた場合終了
                if self.curToken.isEndOrder():
                    orders.append(CharStringOrder(self.curToken, []))
                    return orders
                continue
            #前置命令のため、命令が来てから数値列をパースする。
            if self.curToken.isPrefix():
                self.next()
                self.parseNumberTokens(1)
                order = CharStringOrder(CharStringOrderType.hintmask, self.stack)
                orders.append(order)
                continue
            #次のトークンを呼び出す。
            self.next()

    #数値列をstackに格納する。
    def parseNumberTokens(self, count=-1):
        if not count == -1:
            result = []

            for i in range(count):
                result.append(self.curToken)
                self.next()
            self.stack = result
        if count == -1:
            result = []
            while True:
                if type(self.curToken) is NumberToken:
                    result.append(self.curToken)
                    self.next()
                    continue
                self.stack = result
                return
