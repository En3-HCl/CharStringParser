import enum

class CharStringOrderType(enum.Enum):
    #数値列をstackしておくための命令。仕様には含まれない。
    _stack = "_stack"

    hstem = "hstem"
    vstem = "vstem"

    hstemhm = "hstemhm"
    vstemhm = "vstemhm"
    hintmask = "hintmask"
    cntrmask = "cntrmask"

    rmoveto = "rmoveto"
    hmoveto = "hmoveto"
    vmoveto = "vmoveto"

    rlineto = "rlineto"
    hlineto = "hlineto"
    vlineto = "vlineto"

    rrcurveto = "rrcurveto"
    hhcurveto = "hhcurveto"
    hvcurveto = "hvcurveto"
    vhcurveto = "vhcurveto"
    vvcurveto = "vvcurveto"
    rcurveline = "rcurveline"
    rlinecurve = "rlinecurve"

    hflex = "hflex"
    flex = "flex"
    hflex1 = "hflex1"
    flex1 = "flex1"

    callsubr = "callsubr"
    callgsubr = "callgsubr"

    endchar = "endchar"
    _return = "return"

    def isUniquefix(self):
        return self in [CharStringOrderType.hstemhm, CharStringOrderType.endchar, CharStringOrderType._return]
    def isPrefix(self):
        return self in [CharStringOrderType.hintmask, CharStringOrderType.cntrmask]
    def isPostfix(self):
        return not (self.isUniquefix() or self.isPrefix())

    def isStemOrder(self):
        return self in [CharStringOrderType.hstem, CharStringOrderType.hstemhm, CharStringOrderType.vstem, CharStringOrderType.vstemhm]
    def isMaskOrder(self):
        return self in [CharStringOrderType.cntrmask, CharStringOrderType.hintmask]
    def isMoveOrder(self):
        return self in [CharStringOrderType.rmoveto, CharStringOrderType.hmoveto, CharStringOrderType.vmoveto]
    def isDrawOrder(self):
        return not (self.isStemOrder() or self.isMaskOrder() or self.isEndOrder() or self.isMoveOrder())
    def isEndOrder(self):
        return self in [CharStringOrderType.endchar, CharStringOrderType._return]


    def getOrder(orderString):
        if orderString == "hstem":
            return CharStringOrderType.hstem

        if orderString == "vstem":
            return CharStringOrderType.vstem

        if orderString == "hstemhm":
            return CharStringOrderType.hstemhm

        if orderString == "vstemhm":
            return CharStringOrderType.vstemhm

        if orderString == "hintmask":
            return CharStringOrderType.hintmask

        if orderString == "cntrmask":
            return CharStringOrderType.cntrmask

        if orderString == "rmoveto":
            return CharStringOrderType.rmoveto

        if orderString == "hvcurveto":
            return CharStringOrderType.hvcurveto

        if orderString == "hmoveto":
            return CharStringOrderType.hmoveto

        if orderString == "vmoveto":
            return CharStringOrderType.vmoveto

        if orderString == "rlineto":
            return CharStringOrderType.rlineto

        if orderString == "hlineto":
            return CharStringOrderType.hlineto

        if orderString == "vlineto":
            return CharStringOrderType.vlineto

        if orderString == "rrcurveto":
            return CharStringOrderType.rrcurveto

        if orderString == "hvcurveto":
            return CharStringOrderType.hvcurveto

        if orderString == "hhcurveto":
            return CharStringOrderType.hhcurveto

        if orderString == "rcurveline":
            return CharStringOrderType.rcurveline

        if orderString == "rlinecurve":
            return CharStringOrderType.rlinecurve

        if orderString == "vhcurveto":
            return CharStringOrderType.vhcurveto

        if orderString == "vvcurveto":
            return CharStringOrderType.vvcurveto

        if orderString == "flex1":
            return CharStringOrderType.flex1

        if orderString == "hflex1":
            return CharStringOrderType.hflex1

        if orderString == "hflex":
            return CharStringOrderType.hflex

        if orderString == "flex":
            return CharStringOrderType.flex

        if orderString == "callsubr":
            return CharStringOrderType.callsubr

        if orderString == "callgsubr":
            return CharStringOrderType.callgsubr

        if orderString == "endchar":
            return CharStringOrderType.endchar

        if orderString == "return":
            return CharStringOrderType._return
