a = float( input ("Введите первое число") )
operation = input ("Введите операцию (+, -, *, /): ").strip()
b = float(input("Введите второе число: "))
if operation == "+":
    print('Результат:', a + b)
elif operation == "-":
    result = a - b
elif operation == "*":
    result = a * b  
elif operation == "/":
    if b == 0:
     result = "Ошибка: деление на ноль"
else:
    result = a / b
print("Результат:", result)