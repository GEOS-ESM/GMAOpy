def addTax(price, tax = 17.5):
    return price + price * tax / 100

print(addTax(10))
