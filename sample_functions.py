def func1(input_data):
    return sum(i * i for i in input_data)

def func2(input_data):
    total = 0
    for i in range(len(input_data)):
        for j in range(len(input_data)):
            total += i * j
    return total
