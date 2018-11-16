class Person:
    def say_name(self):
        print("My name is " + self.name)

    def say_age(self):
        print("I am " + str(self.age) + " years old")


person1 = Person()
person1.name = "Yamada"
person1.age = 17
person1.say_name()
person1.say_age()

person2 = Person()
person2.name = "Sato"
person2.age = 18
person2.say_name()
person2.say_age()
