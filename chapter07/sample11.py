# 関数の定義は今までと同じです
def add(a, b):
    total = a + b
    return total


# 普通に呼び出す
print( add(3,2) ) # 「5」と表示

# キーワード引数で呼び出す
print( add(b=4, a=3) ) # 「7」と表示

