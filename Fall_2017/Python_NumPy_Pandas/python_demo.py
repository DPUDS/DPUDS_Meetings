def python_numbers():
    a = 3
    print('a:', a)

    b = 2
    print('b:', b)

    c = a + b
    print('c:', c)

    print('Multiplication for a and b:', a * b)

    print('Normal (float) division for a and b:', a / b)

    print('Floor (integer) division for a and b:', a // b)

    print('a to the power of b:', a ** b)

def python_string():
    a = 'I am a string'
    print('a:', a)

    b = 'I am a different string'
    print('b:', b)

    c = a + b
    print('String concatenation:', c)

    print('Looping through characters in a string:')
    for i in a:
        print(i)

    d = c[1:4]
    print('Making sub-strings by slicing a string from index 1 to index 4:', d)

def python_list():
    a = ['a', 'b', 'c']
    print('A whole list could be printed out all at once:', a)

    b = [1, 2, 3]
    print('Looping through elements in a list:')
    for i in b:
        print(i)

    print('Accessing an element at a specific index:', a[0], b[1])

    c = a + b
    print('List concatenation', c)

    d = c[1:3]
    print('Slicing a list from index 1 to index 3:', d)

def python_dictionary():
    a = {'a': 1, 'b': 2}
    print('A whole dictionary could be printed out all at once:', a)

    a['c'] = 3
    print('Assign a value to a new key to add items to a dictionary:', a)

    print('Looping through keys in a dictionary and getting the value at each key:')
    for key in a:
        print('key:', key)
        print('value:', a[key])

def python_condition():
    a = 1
    b = 2
    c = 4

    if a == 1:
        print('a is equal to 1.')
    else:
        print('a is not equal to 1.')

    if a == 2:
        print('a is equal to 2.')
    elif c == b * 2:
        print('c is twice b')
    else:
        print('No condition is true.')

def python_for_loop():
    a = [1, 'a', 'A String']

    for item in a:
        print(item)

def main():
    python_numbers()
    python_string()
    python_list()
    python_dictionary()
    python_condition()
    python_for_loop()

main()
