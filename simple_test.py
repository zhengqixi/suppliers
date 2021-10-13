from models.supplier import Supplier
from models.product import Product

coke = Product("coke")
coke.id = 1000
s = Supplier(name="Tom", id=4, email='hello@gmail.com', products=set([coke]))

s2 = Supplier("Tom", address='usa')
s2.id = 33195
apple = Product("apple", "1")
pear = Product("pear", "2")
apple.id = 1
pear.id = 2
s2.products = [apple, pear]
print(s.to_json())
print(s2.to_json())
