import tkinter as tk
from tkinter import messagebox
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список задач")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        self.tasks_file = "tasks.json"
        self.tasks = []
        
        self.setup_styles()
        self.load_tasks()
        self.create_widgets()
        self.update_task_list()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        self.bg_color = "#0a0a0a"
        self.panel_color = "#1a1a2e"
        self.accent_color = "#00ffcc"
        self.danger_color = "#ff0055"
        self.warning_color = "#ffaa00"
        self.text_color = "#00ffcc"
        self.secondary_text = "#8888ff"
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(title_frame, text=">_ СПИСОК ЗАДАЧ", 
                               font=("Courier New", 18, "bold"),
                               fg=self.accent_color, bg=self.bg_color)
        title_label.pack()
        
        sub_label = tk.Label(title_frame, text="СИСТЕМА v1.0 // МЕНЕДЖЕР ЗАДАЧ", 
                            font=("Courier New", 9), fg=self.secondary_text, bg=self.bg_color)
        sub_label.pack()
        
        top_frame = tk.Frame(self.root, bg=self.panel_color, relief=tk.FLAT, bd=2)
        top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(top_frame, text="> ВВЕДИТЕ ЗАДАЧУ:", font=("Courier New", 10, "bold"),
                fg=self.accent_color, bg=self.panel_color).pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        input_frame = tk.Frame(top_frame, bg=self.panel_color)
        input_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        self.task_entry = tk.Entry(input_frame, font=("Courier New", 11),
                                   bg="#0a0a0a", fg=self.accent_color,
                                   insertbackground=self.accent_color,
                                   relief=tk.FLAT, bd=1)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        add_button = tk.Button(input_frame, text="[ ДОБАВИТЬ ]", command=self.add_task,
                               bg="#0a0a0a", fg=self.accent_color,
                               font=("Courier New", 10, "bold"),
                               relief=tk.FLAT, bd=1, padx=10)
        add_button.pack(side=tk.RIGHT)
        
        control_frame = tk.Frame(self.root, bg=self.panel_color, relief=tk.FLAT, bd=2)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(control_frame, text="> КОМАНДЫ:", font=("Courier New", 10, "bold"),
                fg=self.accent_color, bg=self.panel_color).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        buttons_frame = tk.Frame(control_frame, bg=self.panel_color)
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        delete_button = tk.Button(buttons_frame, text="[ УДАЛИТЬ ВЫБРАННЫЕ ]", 
                                  command=self.delete_selected,
                                  bg="#0a0a0a", fg=self.danger_color,
                                  font=("Courier New", 9, "bold"),
                                  relief=tk.FLAT, bd=1)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        mark_all_button = tk.Button(buttons_frame, text="[ ВЫПОЛНИТЬ ВСЕ ]", 
                                    command=self.mark_all_completed,
                                    bg="#0a0a0a", fg=self.accent_color,
                                    font=("Courier New", 9, "bold"),
                                    relief=tk.FLAT, bd=1)
        mark_all_button.pack(side=tk.LEFT, padx=5)
        
        clear_all_button = tk.Button(buttons_frame, text="[ ОЧИСТИТЬ ВСЕ ]", 
                                     command=self.clear_all,
                                     bg="#0a0a0a", fg=self.warning_color,
                                     font=("Courier New", 9, "bold"),
                                     relief=tk.FLAT, bd=1)
        clear_all_button.pack(side=tk.LEFT, padx=5)
        
        stats_frame = tk.Frame(control_frame, bg=self.panel_color)
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.counter_label = tk.Label(stats_frame, text="[ СТАТУС: 0/0 ]", 
                                     font=("Courier New", 10, "bold"),
                                     fg=self.secondary_text, bg=self.panel_color)
        self.counter_label.pack(side=tk.LEFT)
        
        self.progress_bar = tk.Frame(stats_frame, height=15, bg="#0a0a0a", relief=tk.FLAT, bd=1)
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)
        
        self.progress_fill = tk.Frame(self.progress_bar, height=13, bg=self.accent_color)
        
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(list_frame, text="> СПИСОК ЗАДАЧ:", font=("Courier New", 10, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(anchor=tk.W, pady=(0, 5))
        
        list_container = tk.Frame(list_frame, bg=self.panel_color, relief=tk.FLAT, bd=2)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(list_container, bg=self.panel_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.canvas.yview,
                                bg=self.panel_color, troughcolor=self.bg_color)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.panel_color)
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        footer = tk.Frame(self.root, bg=self.bg_color)
        footer.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(footer, text="[ СИСТЕМА: АКТИВНА ]", font=("Courier New", 8),
                fg="#00aa00", bg=self.bg_color).pack(side=tk.LEFT)
        
        self.status_label = tk.Label(footer, text="[ ГОТОВ ]", font=("Courier New", 8),
                                    fg=self.secondary_text, bg=self.bg_color)
        self.status_label.pack(side=tk.RIGHT)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.task_entry.delete(0, tk.END)
            self.update_task_list()
            self.save_tasks()
            self.status_label.config(text="[ ЗАДАЧА ДОБАВЛЕНА ]")
            self.root.after(1000, lambda: self.status_label.config(text="[ ГОТОВ ]"))
        else:
            messagebox.showwarning("ОШИБКА", "> ВВЕДИТЕ ТЕКСТ ЗАДАЧИ")
    
    def delete_selected(self):
        tasks_to_delete = []
        if hasattr(self, 'task_vars'):
            for i, var in enumerate(self.task_vars):
                if var.get():
                    tasks_to_delete.append(i)
        
        if tasks_to_delete:
            for i in reversed(tasks_to_delete):
                del self.tasks[i]
            self.update_task_list()
            self.save_tasks()
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"[ УДАЛЕНО: {len(tasks_to_delete)} ]")
                self.root.after(1000, lambda: self.status_label.config(text="[ ГОТОВ ]"))
        else:
            if hasattr(self, 'status_label'):
                messagebox.showinfo("ИНФО", "> ЗАДАЧИ НЕ ВЫБРАНЫ")
    
    def mark_all_completed(self):
        for task in self.tasks:
            task["completed"] = True
        self.update_task_list()
        self.save_tasks()
        if hasattr(self, 'status_label'):
            self.status_label.config(text="[ ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ ]")
            self.root.after(1000, lambda: self.status_label.config(text="[ ГОТОВ ]"))
    
    def clear_all(self):
        if messagebox.askyesno("ПОДТВЕРЖДЕНИЕ", "> УДАЛИТЬ ВСЕ ЗАДАЧИ?"):
            self.tasks.clear()
            self.update_task_list()
            self.save_tasks()
            if hasattr(self, 'status_label'):
                self.status_label.config(text="[ ОЧИСТКА ЗАВЕРШЕНА ]")
                self.root.after(1000, lambda: self.status_label.config(text="[ ГОТОВ ]"))
    
    def toggle_task(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.update_task_list()
        self.save_tasks()
    
    def update_task_list(self):
        if not hasattr(self, 'scrollable_frame'):
            return
            
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.task_vars = []
        
        if not self.tasks:
            empty_label = tk.Label(self.scrollable_frame, 
                                   text="> ЗАДАЧИ НЕ НАЙДЕНЫ\n> ИСПОЛЬЗУЙТЕ [ДОБАВИТЬ] ДЛЯ СОЗДАНИЯ ЗАДАЧ",
                                   font=("Courier New", 11),
                                   fg=self.secondary_text, bg=self.panel_color, pady=50)
            empty_label.pack()
        else:
            for i, task in enumerate(self.tasks):
                task_frame = tk.Frame(self.scrollable_frame, bg=self.panel_color, pady=8, padx=10)
                task_frame.pack(fill=tk.X, padx=5, pady=2)
                
                if i > 0:
                    separator = tk.Frame(self.scrollable_frame, height=1, bg="#2a2a3e")
                    separator.pack(fill=tk.X, padx=10)
                
                var = tk.BooleanVar(value=task["completed"])
                self.task_vars.append(var)
                
                checkbox = tk.Checkbutton(task_frame, variable=var, command=lambda idx=i: self.toggle_task(idx),
                                         bg=self.panel_color, activebackground=self.panel_color,
                                         selectcolor=self.bg_color)
                checkbox.pack(side=tk.LEFT)
                
                task_id = tk.Label(task_frame, text=f"[{i:03d}]", font=("Courier New", 9),
                                  fg=self.secondary_text, bg=self.panel_color)
                task_id.pack(side=tk.LEFT, padx=(0, 10))
                
                task_text = task["text"]
                if task["completed"]:
                    task_text = f"~~{task_text}~~"
                
                task_label = tk.Label(task_frame, text=task_text, font=("Courier New", 10),
                                    bg=self.panel_color, wraplength=400, justify=tk.LEFT)
                
                if task["completed"]:
                    task_label.config(fg="#555555")
                else:
                    task_label.config(fg=self.text_color)
                
                task_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                
                delete_btn = tk.Button(task_frame, text="[X]", command=lambda idx=i: self.delete_single_task(idx),
                                     bg=self.panel_color, fg=self.danger_color, bd=0,
                                     font=("Courier New", 9, "bold"),
                                     activebackground=self.panel_color, cursor="hand2")
                delete_btn.pack(side=tk.RIGHT, padx=5)
        
        completed = sum(1 for task in self.tasks if task["completed"])
        total = len(self.tasks)
        
        if hasattr(self, 'counter_label'):
            self.counter_label.config(text=f"[ СТАТУС: {completed}/{total} ]")
        
        if hasattr(self, 'progress_bar'):
            progress_width = 0
            if total > 0:
                progress_width = int((completed / total) * 300)
            
            for widget in self.progress_bar.winfo_children():
                widget.destroy()
            
            self.progress_fill = tk.Frame(self.progress_bar, height=13, width=progress_width, bg=self.accent_color)
            self.progress_fill.pack(side=tk.LEFT)
            
            remaining = tk.Frame(self.progress_bar, height=13, width=300-progress_width, bg="#0a0a0a")
            remaining.pack(side=tk.LEFT)
    
    def delete_single_task(self, index):
        if messagebox.askyesno("УДАЛЕНИЕ", f"> УДАЛИТЬ ЗАДАЧУ {index:03d}?\n> {self.tasks[index]['text']}"):
            del self.tasks[index]
            self.update_task_list()
            self.save_tasks()
            if hasattr(self, 'status_label'):
                self.status_label.config(text="[ ЗАДАЧА УДАЛЕНА ]")
                self.root.after(1000, lambda: self.status_label.config(text="[ ГОТОВ ]"))
    
    def save_tasks(self):
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ОШИБКА СОХРАНЕНИЯ: {e}")
    
    def load_tasks(self):
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
        except Exception as e:
            print(f"ОШИБКА ЗАГРУЗКИ: {e}")
            self.tasks = []
    
    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()