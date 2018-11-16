message = "Hello"


def say_message():
    global message
    message = "How are you" # グローバル変数「message」への代入
    print(message) # 「How are you」と表示


say_message()
print(message) # 「How are you」と表示
