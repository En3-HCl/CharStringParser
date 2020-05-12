def makeEnumPythonCode(name):
    text = """
        if orderString == "{name}":
            return OrderType.{name}
    """.format(name=name)
    return text
