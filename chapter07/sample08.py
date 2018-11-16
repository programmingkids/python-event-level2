def say_hello():
    local_text = "this is local" # これはローカル変数
    print(local_text) #これは正しく表示されます


say_hello()
#エラー発生（local_textは宣言されていません）
print(local_text)
