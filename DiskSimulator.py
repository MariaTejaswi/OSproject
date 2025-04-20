import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

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

def animate_head_movement(sequence, head, speed, disk_size=200, save=False, filename="disk_animation.gif"):
    fig, ax = plt.subplots(figsize=(8, 4))
    x = list(range(len(sequence) + 1))
    y = [head] + sequence
    line, = ax.plot([], [], marker='o', color='blue', linewidth=2)
    
    ax.set_xlim(0, len(sequence))
    ax.set_ylim(0, disk_size)
    ax.set_xlabel("Step")
    ax.set_ylabel("Track Number")
    ax.set_title(f"Disk Head Movement ({algo_choice.get()})")
    ax.grid(True)

    def update(i):
        line.set_data(x[:i + 1], y[:i + 1])
        return line,

    interval = int(2000 * (1 - speed)) + 100
    ani = FuncAnimation(fig, update, frames=len(x), interval=interval, repeat=False)

    if save:
        ani.save(filename, writer=PillowWriter(fps=10))
        messagebox.showinfo("Exported", f"Animation saved as {filename}")
    else:
        plt.tight_layout()
        plt.show()

# === GUI Functionality ===

def simulate(export=False):
    try:
        head = int(entry_head.get())
        requests = list(map(int, entry_requests.get().split(',')))
        disk_size = int(entry_disk_size.get())
        algorithm = algo_choice.get()
        speed = speed_slider.get()
        seek_time = float(entry_seek_time.get())
        
        if any(r < 0 or r >= disk_size for r in requests):
            messagebox.showerror("Error", f"Requests must be between 0 and {disk_size-1}!")
            return
        
        if head < 0 or head >= disk_size:
            messagebox.showerror("Error", f"Head position must be between 0 and {disk_size-1}!")
            return

        if algorithm == 'FCFS':
            sequence, total = fcfs(requests, head)
        elif algorithm == 'SSTF':
            sequence, total = sstf(requests, head)
        elif algorithm == 'SCAN':
            direction = direction_choice.get().lower()
            sequence, total = scan(requests, head, direction, disk_size)
        elif algorithm == 'C-SCAN':
            sequence, total = cscan(requests, head, disk_size)
        else:
            messagebox.showerror("Error", "Invalid algorithm selected.")
            return

        total_seek_time = total * seek_time
        result_label.config(text=f"Total Head Movement: {total}\nTotal Seek Time: {total_seek_time:.2f} ms")

        if export:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".gif",
                filetypes=[("GIF files", "*.gif")],
                initialfile=f"{algorithm}_animation.gif"
            )
            if filepath:
                animate_head_movement(sequence, head, speed, disk_size, save=True, filename=filepath)
        else:
            animate_head_movement(sequence, head, speed, disk_size)

    except ValueError:
        messagebox.showerror("Error", "Invalid input format! Ensure all values are numbers.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def export_log():
    try:
        head = int(entry_head.get())
        requests = list(map(int, entry_requests.get().split(',')))
        disk_size = int(entry_disk_size.get())
        algorithm = algo_choice.get()
        seek_time = float(entry_seek_time.get())

        if algorithm == 'FCFS':
            sequence, total = fcfs(requests, head)
        elif algorithm == 'SSTF':
            sequence, total = sstf(requests, head)
        elif algorithm == 'SCAN':
            direction = direction_choice.get().lower()
            sequence, total = scan(requests, head, direction, disk_size)
        elif algorithm == 'C-SCAN':
            sequence, total = cscan(requests, head, disk_size)

        total_seek_time = total * seek_time
        log = f"""Algorithm: {algorithm}
Initial Head Position: {head}
Disk Size: {disk_size}
Requests: {requests}

Execution Order: {sequence}
Total Head Movement: {total}
Seek Time per Unit: {seek_time} ms
Total Seek Time: {total_seek_time:.2f} ms"""

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile=f"{algorithm}_log.txt"
        )
        if filepath:
            with open(filepath, 'w') as file:
                file.write(log)
            messagebox.showinfo("Log Saved", f"Log exported to {filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"Unable to export log: {str(e)}")

# === GUI Setup ===

root = tk.Tk()
root.title("Disk Scheduling Simulator (Animated)")
root.geometry("700x550")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure('TLabel', font=('Segoe UI', 11))
style.configure('TButton', font=('Segoe UI', 11))
style.configure('TEntry', font=('Segoe UI', 11))
style.configure('TCombobox', font=('Segoe UI', 11))

wrapper = ttk.Frame(root, padding=30)
wrapper.place(relx=0.5, rely=0.5, anchor='center')

main_frame = ttk.Frame(wrapper)
main_frame.pack()

# Input Fields
fields = [
    ("Initial Head Position:", 'entry_head'),
    ("Disk Size:", 'entry_disk_size', "200"),
    ("Seek Time per Unit (ms):", 'entry_seek_time', "1"),
    ("Request Sequence (comma-separated):", 'entry_requests')
]

entries = {}
for idx, field in enumerate(fields):
    label_text, var_name = field[0], field[1]
    default = field[2] if len(field) == 3 else ""
    ttk.Label(main_frame, text=label_text).grid(row=idx, column=0, sticky="e", pady=5, padx=10)
    entry = ttk.Entry(main_frame, width=30)
    entry.grid(row=idx, column=1, pady=5, padx=10)
    if default:
        entry.insert(0, default)
    entries[var_name] = entry

entry_head = entries['entry_head']
entry_disk_size = entries['entry_disk_size']
entry_seek_time = entries['entry_seek_time']
entry_requests = entries['entry_requests']

# Algorithm Choice
ttk.Label(main_frame, text="Select Algorithm:").grid(row=4, column=0, sticky="e", pady=5, padx=10)
algo_choice = ttk.Combobox(main_frame, values=["FCFS", "SSTF", "SCAN", "C-SCAN"], state='readonly', width=28)
algo_choice.current(0)
algo_choice.grid(row=4, column=1, pady=5, padx=10)
algo_choice.bind("<<ComboboxSelected>>", lambda e: direction_choice.grid() if algo_choice.get() == "SCAN" else direction_choice.grid_remove())

# SCAN Direction
ttk.Label(main_frame, text="SCAN Direction:").grid(row=5, column=0, sticky="e", pady=5, padx=10)
direction_choice = ttk.Combobox(main_frame, values=["Right", "Left"], state='readonly', width=28)
direction_choice.current(0)
direction_choice.grid(row=5, column=1, pady=5, padx=10)
direction_choice.grid_remove()

# Speed Slider
ttk.Label(main_frame, text="Animation Speed:").grid(row=6, column=0, sticky="e", pady=5, padx=10)
speed_slider = ttk.Scale(main_frame, from_=0, to=1, orient='horizontal', value=0.5)
speed_slider.grid(row=6, column=1, pady=5, padx=10, sticky="ew")

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=7, column=0, columnspan=2, pady=20)
ttk.Button(button_frame, text="Simulate", command=lambda: simulate(export=False)).pack(side='left', padx=5)
ttk.Button(button_frame, text="Export Graph", command=lambda: simulate(export=True)).pack(side='left', padx=5)
ttk.Button(button_frame, text="Export Log", command=export_log).pack(side='left', padx=5)

# Result
result_label = ttk.Label(main_frame, text="", font=('Segoe UI', 11, 'bold'), anchor='center', justify='center')
result_label.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
