import enum

class OrderType(enum.Enum):
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

    endchar = "endchar"

    def isUniquefix(self):
        return self in [OrderType.hstemhm, OrderType.endchar]
    def isPrefix(self):
        return self in [OrderType.hintmask, OrderType.cntrmask]
    def isPostfix(self):
        return not (self.isUniquefix() or self.isPrefix())

    def isStemOrder(self):
        return self in [OrderType.hstem, OrderType.hstemhm, OrderType.vstem, OrderType.vstemhm]
    def isMaskOrder(self):
        return self in [OrderType.cntrmask, OrderType.hintmask]
    def isMoveOrder(self):
        return self in [OrderType.rmoveto, OrderType.hmoveto, OrderType.vmoveto]
    def isDrawOrder(self):
        return not (self.isStemOrder() or self.isMaskOrder() or self.isEndChar() or self.isMoveOrder())
    def isEndChar(self):
        return self == OrderType.endchar


    def getOrder(orderString):
        if orderString == "hstem":
            return OrderType.hstem

        if orderString == "vstem":
            return OrderType.vstem

        if orderString == "hstemhm":
            return OrderType.hstemhm

        if orderString == "vstemhm":
            return OrderType.vstemhm

        if orderString == "hintmask":
            return OrderType.hintmask

        if orderString == "rmoveto":
            return OrderType.rmoveto

        if orderString == "hvcurveto":
            return OrderType.hvcurveto

        if orderString == "hmoveto":
            return OrderType.hmoveto

        if orderString == "vmoveto":
            return OrderType.vmoveto

        if orderString == "rlineto":
            return OrderType.rlineto

        if orderString == "hlineto":
            return OrderType.hlineto

        if orderString == "vlineto":
            return OrderType.vlineto

        if orderString == "rrcurveto":
            return OrderType.rrcurveto

        if orderString == "hvcurveto":
            return OrderType.hvcurveto

        if orderString == "hhcurveto":
            return OrderType.hhcurveto

        if orderString == "rcurveline":
            return OrderType.rcurveline

        if orderString == "rlinecurve":
            return OrderType.rlinecurve

        if orderString == "vhcurveto":
            return OrderType.vhcurveto

        if orderString == "vvcurveto":
            return OrderType.vvcurveto

        if orderString == "flex1":
            return OrderType.flex1

        if orderString == "hflex1":
            return OrderType.hflex1

        if orderString == "hflex":
            return OrderType.hflex

        if orderString == "flex":
            return OrderType.flex

        if orderString == "endchar":
            return OrderType.endchar

        if orderString == "cntrmask":
            return OrderType.cntrmask
