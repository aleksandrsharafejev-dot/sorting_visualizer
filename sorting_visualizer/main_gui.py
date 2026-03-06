from sorting_algorithms import bubble_sort, quick_sort, merge_sort
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox


def run_visualization(algorithm_key, size, speed, value_min, value_max):
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from sorting_algorithms import draw_array

    arr = [random.randint(value_min, value_max) for _ in range(size)]

    plt.figure()
    plt.title(f"Sorting Visualizer — {algorithm_key} | N={size}")

    start_time = time.time()

    if algorithm_key == "Bubble Sort":
        gen = bubble_sort(arr)
    elif algorithm_key == "Quick Sort":
        gen = quick_sort(arr, 0, len(arr) - 1)
    elif algorithm_key == "Merge Sort":
        gen = merge_sort(arr)
    else:
        raise ValueError("Unknown algorithm")

    for step in gen:
        arr_state, indices, action, sorted_indices = step
        draw_array(arr_state, indices, action, sorted_indices, speed)

    end_time = time.time()
    print("Sorting time:", round(end_time - start_time, 4), "seconds")
    plt.show()


def build_gui():
    root = tk.Tk()
    root.title("Sorting Visualizer")
    root.geometry("560x420")
    root.resizable(False, False)
    root.lift()
    root.attributes("-topmost", True)
    root.after(200, lambda: root.attributes("-topmost", False))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
    style.configure("Section.TLabel", font=("Helvetica", 11, "bold"))

    container = ttk.Frame(root, padding=20)
    container.pack(fill="both", expand=True)

    header = ttk.Label(container, text="Sorting Visualizer", style="Header.TLabel")
    header.pack(anchor="w")

    subtitle = ttk.Label(
        container,
        text="Academic project: algorithm selection and visualization settings",
        foreground="#444444",
    )
    subtitle.pack(anchor="w", pady=(4, 16))

    algo_label = ttk.Label(container, text="Algorithm", style="Section.TLabel")
    algo_label.pack(anchor="w")
    algorithm_var = tk.StringVar(value="Quick Sort")
    algo_box = ttk.Combobox(
        container,
        textvariable=algorithm_var,
        values=["Bubble Sort", "Quick Sort", "Merge Sort"],
        state="readonly",
        width=30,
    )
    algo_box.pack(anchor="w", pady=(6, 14))

    size_label = ttk.Label(container, text="Array size", style="Section.TLabel")
    size_label.pack(anchor="w")
    size_var = tk.IntVar(value=60)
    size_spin = ttk.Spinbox(container, from_=10, to=300, textvariable=size_var, width=10)
    size_spin.pack(anchor="w", pady=(6, 14))

    speed_label = ttk.Label(container, text="Animation speed (sec)", style="Section.TLabel")
    speed_label.pack(anchor="w")
    speed_var = tk.DoubleVar(value=0.03)
    speed_scale = ttk.Scale(
        container, from_=0.005, to=0.2, variable=speed_var, orient="horizontal"
    )
    speed_scale.pack(anchor="w", fill="x", pady=(6, 14))

    range_label = ttk.Label(container, text="Value range", style="Section.TLabel")
    range_label.pack(anchor="w")
    range_frame = ttk.Frame(container)
    range_frame.pack(anchor="w", pady=(6, 14))
    value_min_var = tk.IntVar(value=1)
    value_max_var = tk.IntVar(value=100)
    ttk.Label(range_frame, text="from").pack(side="left")
    ttk.Spinbox(range_frame, from_=1, to=1000, textvariable=value_min_var, width=8).pack(
        side="left", padx=(6, 16)
    )
    ttk.Label(range_frame, text="to").pack(side="left")
    ttk.Spinbox(range_frame, from_=2, to=2000, textvariable=value_max_var, width=8).pack(
        side="left", padx=(6, 0)
    )

    selected = {}

    def on_start():
        try:
            size = int(size_var.get())
            speed = float(speed_var.get())
            value_min = int(value_min_var.get())
            value_max = int(value_max_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please check that all parameters are valid.")
            return

        if size < 10 or size > 300:
            messagebox.showerror("Error", "Array size must be between 10 and 300.")
            return
        if value_min >= value_max:
            messagebox.showerror("Error", "Minimum value must be less than maximum value.")
            return
        if speed <= 0:
            messagebox.showerror("Error", "Speed must be greater than 0.")
            return

        selected["algorithm_key"] = algorithm_var.get()
        selected["size"] = size
        selected["speed"] = speed
        selected["value_min"] = value_min
        selected["value_max"] = value_max
        root.quit()

    def on_about():
        messagebox.showinfo(
            "About",
            "Sorting Visualizer\n"
            "Visualization of sorting algorithms.\n"
            "Prepared as an academic demonstration project.",
        )

    actions = ttk.Frame(container)
    actions.pack(anchor="w", pady=(8, 0))
    ttk.Button(actions, text="Start", command=on_start).pack(side="left")
    ttk.Button(actions, text="About", command=on_about).pack(side="left", padx=10)
    ttk.Button(actions, text="Exit", command=root.destroy).pack(side="left")

    root.mainloop()
    root.destroy()
    return selected if selected else None


if __name__ == "__main__":
    config = build_gui()
    if config:
        run_visualization(**config)
