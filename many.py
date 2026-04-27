import tkinter as tk
from tkinter import messagebox
import random
import json

FILE = "tasks.json"

tasks = []
history = []


def add_task():
    text = entry.get().strip()
    category = category_var.get()

    if text == "":
        messagebox.showerror("Ошибка", "Введите задачу")
        return

    tasks.append({"text": text, "category": category})
    entry.delete(0, tk.END)


def generate_task():
    if not tasks:
        messagebox.showwarning("Внимание", "Нет задач")
        return

    task = random.choice(tasks)
    history.append(task)
    update_list()


def update_list(*args):
    listbox.delete(0, tk.END)
    filter_cat = filter_var.get()

    for task in history:
        if filter_cat == "Все" or task["category"] == filter_cat:
            listbox.insert(tk.END, f'{task["text"]} ({task["category"]})')


def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks, "history": history}, f, ensure_ascii=False)


def load():
    global tasks, history
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            tasks = data.get("tasks", [])
            history = data.get("history", [])
            update_list()
    except:
        pass


# --- GUI ---
root = tk.Tk()
root.title("Task Generator")

entry = tk.Entry(root)
entry.pack()

category_var = tk.StringVar(value="Учёба")
tk.OptionMenu(root, category_var, "Учёба", "Спорт", "Работа").pack()

tk.Button(root, text="Добавить", command=add_task).pack()
tk.Button(root, text="Сгенерировать", command=generate_task).pack()

filter_var = tk.StringVar(value="Все")
tk.OptionMenu(root, filter_var, "Все", "Учёба", "Спорт", "Работа", command=update_list).pack()

listbox = tk.Listbox(root, width=40)
listbox.pack()

tk.Button(root, text="Сохранить", command=save).pack()
tk.Button(root, text="Загрузить", command=load).pack()

root.mainloop()