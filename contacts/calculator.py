class Calculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def sum(self):
        return self.num1 + self.num2

    def sub(self):
        return self.num1 - self.num2
    
    def mul(self):
        return self.num1 * self.num2

    def div(self):
        return self.num1 / self.num2

if __name__ == '__main__':
    calc = Calculator(6, 2)
    sumResult = calc.sum()
    print(sumResult)
    subResult = calc.sub()
    print(subResult)
    mulResult = calc.mul()
    print(mulResult)
    divResult = calc.div()
    print(divResult)