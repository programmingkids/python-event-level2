# 引数が二個ある関数。2番目の引数にはデフォルト値が設定されています
def add(a, b=10):
    total = a + b
    return total


# 引数
print(add(2,5))  # 「7」と表示
print(add(3))    # 「13」と表示
