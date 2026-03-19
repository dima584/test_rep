# Функція для перетворення  виразу 
def rpn(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}  # Пріоритети
    output = []  # Вихідний список 
    stack = []   # Стек 
    tokens = []  # токени 
    num = ''     # рядок для багатозначних чисел

    # Розділяємо рядок на токени
    for ch in expression:
        if ch.isdigit():
            num += ch  # Будуємо число
        else:
            if num:
                tokens.append(num)  # Додаємо повне число
                num = ''
            if ch.strip():  
                tokens.append(ch)
    if num:
        tokens.append(num)  # Додаємо останнє число

    for token in tokens:
        if token.isdigit():
            output.append(token)  # Число одразу в вихід
        elif token in precedence:

            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)  # Кладемо поточний оператор у стек
        elif token == '(':
            stack.append(token)  # Дужку просто запхаємо
        elif token == ')':

            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Видаляємо ( зі стеку

    while stack:
        output.append(stack.pop())

    return output

# Функція для обчислення значення
def evaluate_rpn(rpn):
    stack = []
    for token in rpn:
        if token.isdigit():
            stack.append(int(token))  # Числав стек
        else:
            b = stack.pop()  # Витягуємо другий операнд
            a = stack.pop()  # Потім перший

            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(a // b) 
    return stack[0]  

expression = input("Введи арифметичний вираз: ")
rpn = rpn(expression)

print("Зворотна польська нотація:", ' '.join(rpn))
result = evaluate_rpn(rpn)

print("Результат:", result)