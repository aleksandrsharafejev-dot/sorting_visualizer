import matplotlib.pyplot as plt
import random

arr = [random.randint(1,50) for _ in range(20)]

def draw_array(arr, i=-1, j=-1, action="compare", sorted_indices=[]):
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

def partition(arr, low, high, sorted_indices):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        yield arr, j, high, "compare", sorted_indices
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr, i, j, "swap", sorted_indices
    arr[i+1], arr[high] = arr[high], arr[i+1]
    yield arr, i+1, high, "swap", sorted_indices
    sorted_indices.append(i+1)
    return i+1

def quick_sort(arr, low, high, sorted_indices=[]):
    if low < high:
        pi = yield from partition(arr, low, high, sorted_indices)
        yield from quick_sort(arr, low, pi-1, sorted_indices)
        yield from quick_sort(arr, pi+1, high, sorted_indices)

plt.figure()
plt.title("Quick Sort Visualizer")

for arr_state, i, j, action, sorted_indices in quick_sort(arr, 0, len(arr)-1):
    draw_array(arr_state, i, j, action, sorted_indices)

plt.show()