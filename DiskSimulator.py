import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

# === Algorithms ===

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
    move = right + [disk_size - 1] + left[::-1] if direction == 'right' else left[::-1] + [0] + right
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

def animate_head_movement(sequence, head, speed, save=False, filename="disk_animation.mp4"):
    fig, ax = plt.subplots(figsize=(6, 3))
    x = list(range(len(sequence) + 1))
    y = [head] + sequence
    line, = ax.plot([], [], marker='o', color='blue', linewidth=2)
    ax.set_xlim(0, len(sequence))
    ax.set_ylim(min(y) - 10, max(y) + 10)
    ax.set_xlabel("Step")
    ax.set_ylabel("Track Number")
    ax.set_title("Disk Head Animation")
    ax.grid(True)

    def update(i):
        line.set_data(x[:i+1], y[:i+1])
        return line,

    interval = int(2000 * (1 - speed)) + 100  # adjust based on slider
    ani = FuncAnimation(fig, update, frames=len(x), interval=interval, repeat=False)

    if save:
        ani.save(filename, writer='pillow')  # Save as gif or mp4
        messagebox.showinfo("Exported", f"Animation saved as {filename}")
    else:
        plt.tight_layout()
        plt.show()

# === GUI Functionality ===

def simulate(export=False):
    try:
        head = int(entry_head.get())
        requests = list(map(int, entry_requests.get().split(',')))
        algorithm = algo_choice.get()
        speed = speed_slider.get()

        if algorithm == 'FCFS':
            sequence, total = fcfs(requests, head)
        elif algorithm == 'SSTF':
            sequence, total = sstf(requests, head)
        elif algorithm == 'SCAN':
            sequence, total = scan(requests, head)
        elif algorithm == 'C-SCAN':
            sequence, total = cscan(requests, head)
        else:
            messagebox.showerror("Error", "Invalid algorithm selected.")
            return

        result_label.config(text=f"Total Head Movement: {total}")
        if export:
            filepath = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
            if filepath:
                animate_head_movement(sequence, head, speed, save=True, filename=filepath)
        else:
            animate_head_movement(sequence, head, speed)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def export_log():
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

        log = f"Algorithm: {algorithm}\nInitial Head: {head}\nRequests: {requests}\n\nExecution Order: {sequence}\nTotal Head Movement: {total}"
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, 'w') as file:
                file.write(log)
            messagebox.showinfo("Log Saved", f"Log exported to {filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"Unable to export log: {e}")

# === GUI Setup ===

root = tk.Tk()
root.title("Disk Scheduling Simulator (Animated)")
root.geometry("540x420")
root.configure(bg="#f4f4f4")

# Apply consistent styling
style = ttk.Style()
style.configure('TLabel', font=('Segoe UI', 12))
style.configure('TButton', font=('Segoe UI', 12))
style.configure('TEntry', font=('Segoe UI', 12))
style.configure('TCombobox', font=('Segoe UI', 12))

# Outer frame for centering
outer_frame = ttk.Frame(root)
outer_frame.place(relx=0.5, rely=0.5, anchor='center')

frame = ttk.Frame(outer_frame, padding=20)
frame.grid()

# Input fields and labels
ttk.Label(frame, text="Initial Head Position:").grid(row=0, column=0, sticky="e", pady=5)
entry_head = ttk.Entry(frame, width=25)
entry_head.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Request Sequence (comma-separated):").grid(row=1, column=0, sticky="e", pady=5)
entry_requests = ttk.Entry(frame, width=25)
entry_requests.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Select Algorithm:").grid(row=2, column=0, sticky="e", pady=5)
algo_choice = ttk.Combobox(frame, values=["FCFS", "SSTF", "SCAN", "C-SCAN"], state='readonly', width=23)
algo_choice.current(0)
algo_choice.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Animation Speed:").grid(row=3, column=0, sticky="e", pady=5)
speed_slider = ttk.Scale(frame, from_=0, to=1, orient='horizontal', value=0.5)
speed_slider.grid(row=3, column=1, pady=5)

ttk.Button(frame, text="Simulate", command=lambda: simulate(export=False)).grid(row=4, column=0, columnspan=2, pady=15)
ttk.Button(frame, text="Export Graph", command=lambda: simulate(export=True)).grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="Export Log", command=export_log).grid(row=6, column=0, columnspan=2, pady=5)

result_label = ttk.Label(frame, text="Total Head Movement: ", font=('Segoe UI', 12, 'bold'))
result_label.grid(row=7, column=0, columnspan=2, pady=15)

root.mainloop()

