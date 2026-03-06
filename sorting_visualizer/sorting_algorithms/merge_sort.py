import matplotlib.pyplot as plt
import random

arr = [random.randint(1,50) for _ in range(20)]

def draw_array(arr, indices=[], action="compare", sorted_indices=[]):
    colors = ['blue'] * len(arr)

    if action == "compare":
        for idx in indices:
            colors[idx] = 'red'
    elif action == "merge":
        for idx in indices:
            colors[idx] = 'yellow'

    for index in sorted_indices:
        colors[index] = 'green'

    plt.clf()
    plt.bar(range(len(arr)), arr, color=colors)
    plt.pause(0.1)

def merge(arr, left, mid, right, sorted_indices):
    L = arr[left:mid+1]
    R = arr[mid+1:right+1]
    i = j = 0
    k = left

    while i < len(L) and j < len(R):
        yield arr, [k, left+i, mid+1+j], "compare", sorted_indices
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        yield arr, [k], "merge", sorted_indices
        k += 1

    while i < len(L):
        arr[k] = L[i]
        yield arr, [k], "merge", sorted_indices
        i += 1
        k += 1

    while j < len(R):
        arr[k] = R[j]
        yield arr, [k], "merge", sorted_indices
        j += 1
        k += 1

def merge_sort(arr, left=0, right=None, sorted_indices=[]):
    if right is None:
        right = len(arr)-1
    if left < right:
        mid = (left + right)//2
        yield from merge_sort(arr, left, mid, sorted_indices)
        yield from merge_sort(arr, mid+1, right, sorted_indices)
        yield from merge(arr, left, mid, right, sorted_indices)

        for idx in range(left, right+1):
            if idx not in sorted_indices:
                sorted_indices.append(idx)
        yield arr, [], "done", sorted_indices

plt.figure()
plt.title("Merge Sort Visualizer")

for arr_state, indices, action, sorted_indices in merge_sort(arr):
    draw_array(arr_state, indices, action, sorted_indices)

plt.show()