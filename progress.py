import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class DailyTasks:
    def __init__(self, master):
        self.master = master
        self.master.title("Daily Tasks")
        self.tasks = ["Daily Calorie Goal", "Fitness Goal", "Sleep Goal", "Water Goal", "Morning Routine", "Night Routine"]
        self.task_status = {task: False for task in self.tasks}
        self.progress = 0
        self.max_days = 117
        self.data_file = 'progress_data.json'
        self.current_date = datetime.now().date()
        self.buttons = []

        self.progress_label = tk.Label(self.master, text="")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.master, length=200, mode='determinate', maximum=self.max_days)
        self.progress_bar.pack(pady=10)

        for task in self.tasks:
            btn = tk.Button(self.master, text=task, command=lambda task=task: self.complete_task(task))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.load_data()

    def complete_task(self, task):
        if not self.task_status[task]:
            confirm = messagebox.askyesno("Confirmation", f"Are you sure you completed {task}?")
            if confirm:
                self.task_status[task] = True
                if all(self.task_status.values()):
                    self.progress += 1
                    self.progress_bar['value'] = self.progress
                    self.task_status = {task: False for task in self.tasks}
                    if self.progress >= self.max_days:
                        messagebox.showinfo("Congratulations", "You have completed all tasks for 117 days!")
                    else:
                        messagebox.showinfo("All Tasks Completed", "No more tasks for today.")
                        for btn in self.buttons:
                            btn.config(state='disabled')
                self.save_data()
                self.update_progress_label()
        else:
            messagebox.showinfo("Task Completed", f"You have already completed {task} for today.")

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump((self.task_status, self.progress, str(self.current_date)), f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.task_status, self.progress, stored_date = json.load(f)
                self.progress_bar['value'] = self.progress
                self.update_progress_label()
                if datetime.strptime(stored_date, "%Y-%m-%d").date() != self.current_date:
                    self.task_status = {task: False for task in self.tasks}
                    for btn in self.buttons:
                        btn.config(state='normal')

    def update_progress_label(self):
        self.progress_label.config(text=f"Days Completed: {self.progress} / {self.max_days}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyTasks(root)
    root.mainloop()
