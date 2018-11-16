class Person:
    def say_name(self):
        # インスタンスが保持する属性を使う場合、「self.name」となります
        print("My name is " + self.name)

    def say_age(self):
        # インスタンスが保持する属性を使う場合、「self.age」となります
        print("I am " + str(self.age) + " years old")


person1 = Person()
# インスタンスのデータ属性に「name」に値を代入
person1.name = "Yamada"
# インスタンスのデータ属性に「age」に値を代入
person1.age = 17
# メソッドの呼び出し
person1.say_name()
person1.say_age()
