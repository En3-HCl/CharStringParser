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

list = [165, 134, 134, 165, 165, -134, 134, -165, -165, -134, -134, -165, -165, 134, -134, 165]
print(makeNumberTokenExpression(list))
