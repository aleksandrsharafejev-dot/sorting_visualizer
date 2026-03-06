import matplotlib.pyplot as plt
import random

arr = [random.randint(1,50) for _ in range(20)]


def draw_array(arr, i=-1, j=-1, action = "compare", sorted_indices=[]):
    colors = ['blue'] * len(arr)

    if action == "compare":
        if i >= 0: colors[i] = 'red'
        if j >= 0: colors[j] = 'red'
    elif action == "swap":
        if i >= 0: colors[i] = 'yellow'
        if j >= 0: colors[j] = 'yellow'
    for index in sorted_indices:
        colors[index] = 'green'

    plt.clf()
    plt.bar(range(len(arr)), arr, color=colors)
    plt.pause(0.1)


def bubble_sort(arr):
    n = len(arr)
    sorted_indices = []

    for i in range(n):
        for j in range(n-i-1):
            yield arr, j, j+1, "compare", sorted_indices

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr, j, j+1, "swap", sorted_indices
        sorted_indices.append(n-i-1)
    yield arr, -1, -1, "done", list(range(n))

plt.figure()
plt.title("Bubble Sort Visualization")

for arr_state, i, j, action, sorted_indices in bubble_sort(arr):
    draw_array(arr_state, i, j, action, sorted_indices)


plt.show()