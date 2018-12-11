# ここにBookクラスを定義します
class Book:
    def __init__(self, title, price, category):
        self.title = title
        self.price = price
        self.category = category

    def get_title(self):
        print("本のタイトルは" + self.title)

    def get_price(self):
        print("本の金額は" + str(self.price))

    def get_category(self):
        print("本のカテゴリは" + self.category)


book = Book("ミッキーの冒険", 800, "小説")
book.get_title()
book.get_price()
book.get_category()
