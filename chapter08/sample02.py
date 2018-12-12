class Person:
    def say_name(self):
        # インスタンスが保持する属性を使う場合、「self.name」となります
        print("My name is " + self.name)

    def say_age(self):
        # インスタンスが保持する属性を使う場合、「self.age」となります
        print("I am " + str(self.age) + " years old")

