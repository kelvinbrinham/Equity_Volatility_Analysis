'''
Test
'''


def sos(x):
    return sum([y ** 2 for y in x])


lst = [1, 3, 5]

print(sos(lst))