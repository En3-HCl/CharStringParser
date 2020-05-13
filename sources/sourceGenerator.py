#Enumのケースマッチのコードを生成する。
def makeEnumPythonCode(name):
    text = """
        if orderString == "{name}":
            return OrderType.{name}
    """.format(name=name)
    return text

#テストに利用するNumberToken列のコードを生成する。
def makeNumberTokenExpression(list):
    result = []
    for i in range(len(list)):
        text = "NumberToken(\"{number}\")".format(number=list[i])
        result.append(text)
    return ", ".join(result)

list = [-15 ,3 ,-46 ,-6 ,-9 ,-21 ,-5 ,-29 ,-1 ,-35]
print(makeNumberTokenExpression(list))
