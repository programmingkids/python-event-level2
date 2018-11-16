class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def getName(self):
        print("私の名前は" + self.name)

    def getAge(self):
        print("私は" + str(self.age) + "才です")


person1 = Person("山田", 18)
person1.getName()
person1.getAge()

person2 = Person("佐藤", 17)
person2.getName()
person2.getAge()
