import matplotlib.pyplot as plt

def draw_array(arr, indices=[], action="compare", sorted_indices=[], speed=0.05):
    colors = ['blue'] * len(arr)
    if action == "compare":
        for idx in indices:
            colors[idx] = 'red'
    elif action == "swap" or action == "merge":
        for idx in indices:
            colors[idx] = 'yellow'
    for index in sorted_indices:
        colors[index] = 'green'
    plt.clf()
    plt.bar(range(len(arr)), arr, color=colors)
    plt.pause(speed)
