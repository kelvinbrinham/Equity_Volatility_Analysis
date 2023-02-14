'''
Test
'''
import numpy as np

lst = [9, 10, 11, 10, 9, 200, 8]
lst_diff = np.diff(lst)

print(lst)
print(lst_diff)

std = np.std(lst_diff)
cutoff = std

for i in range(len(lst_diff) - 1):
    if lst_diff[i] > cutoff and lst_diff[i + 1] < - cutoff:
        lst[i + 1] = np.nan

    elif lst_diff[i] < -cutoff and lst_diff[i + 1] > cutoff:
        lst[i + 1] = np.nan


print('----')
print(lst)
print(lst_diff)