import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === Disk Scheduling Algorithms ===

def fcfs(requests, head):
    sequence = []
    total = 0
    for req in requests:
        total += abs(head - req)
        sequence.append(req)
        head = req
    return sequence, total

def sstf(requests, head):
    sequence = []
    total = 0
    requests = requests.copy()
    while requests:
        closest = min(requests, key=lambda x: abs(head - x))
        total += abs(head - closest)
        sequence.append(closest)
        head = closest
        requests.remove(closest)
    return sequence, total

def scan(requests, head, direction='right', disk_size=200):
    sequence = []
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    if direction == 'right':
        move = right + [disk_size - 1] + left[::-1]
    else:
        move = left[::-1] + [0] + right

    for track in move:
        if track != head:
            total += abs(head - track)
            sequence.append(track)
            head = track
    return sequence, total

def cscan(requests, head, disk_size=200):
    sequence = []
    total = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    move = right + [disk_size - 1, 0] + left
    for track in move:
        if track != head:
            total += abs(head - track)
            sequence.append(track)
            head = track
    return sequence, total

# === Animation Function ===

def animate_head_movement(sequence, head):
    fig, ax = plt.subplots(figsize=(6, 3))
    x = list(range(len(sequence) + 1))
    y = [head] + sequence

    line, = ax.plot([], [], marker='o', color='blue')
    ax.set_xlim(0, len(sequence))
    ax.set_ylim(min(y) - 10, max(y) + 10)
    ax.set_xlabel("Step")
    ax.set_ylabel("Track Number")
    ax.set_title("Animated Disk Head Movement")
    ax.grid(True)

    def update(i):
        line.set_data(x[:i+1], y[:i+1])
        return line,

    ani = FuncAnimation(fig, update, frames=len(x), interval=500, repeat=False)
    plt.tight_layout()
    plt.show()

# === Simulation Handler ===

def simulate():
    try:
        head = int(entry_head.get())
        requests = list(map(int, entry_requests.get().split(',')))
        algorithm = algo_choice.get()

        if algorithm == 'FCFS':
            sequence, total = fcfs(requests, head)
        elif algorithm == 'SSTF':
            sequence, total = sstf(requests, head)
        elif algorithm == 'SCAN':
            sequence, total = scan(requests, head)
        elif algorithm == 'C-SCAN':
            sequence, total = cscan(requests, head)
        else:
            messagebox.showerror("Error", "Unknown algorithm selected.")
            return

        result_label.config(text=f"Total Head Movement: {total}")
        animate_head_movement(sequence, head)

    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

# === GUI Setup ===

root = tk.Tk()
root.title("Disk Scheduling Simulator (Animated)")
root.geometry("520x320")
root.configure(bg="#f4f4f4")

style = ttk.Style()
style.configure('TLabel', font=('Segoe UI', 12))
style.configure('TButton', font=('Segoe UI', 12))
style.configure('TEntry', font=('Segoe UI', 12))

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="Initial Head Position:").grid(row=0, column=0, sticky="e", pady=5)
entry_head = ttk.Entry(frame, width=25)
entry_head.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Request Sequence (comma-separated):").grid(row=1, column=0, sticky="e", pady=5)
entry_requests = ttk.Entry(frame, width=25)
entry_requests.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Select Algorithm:").grid(row=2, column=0, sticky="e", pady=5)
algo_choice = ttk.Combobox(frame, values=["FCFS", "SSTF", "SCAN", "C-SCAN"], state='readonly')
algo_choice.current(0)
algo_choice.grid(row=2, column=1, pady=5)

ttk.Button(frame, text="Simulate", command=simulate).grid(row=3, column=0, columnspan=2, pady=15)

result_label = ttk.Label(frame, text="Total Head Movement: ", font=('Segoe UI', 12, 'bold'))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
