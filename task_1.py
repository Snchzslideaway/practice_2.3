import tkinter as tk
from tkinter import ttk, messagebox
import requests
import psutil
import json
import os
import threading




class PracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учебная практика 2.2 - Настольное приложение")
        self.root.geometry("800x600")

        # Создание вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.setup_task1()
        self.setup_task2()
        self.setup_task3()
        self.setup_task4()

    # --- ЗАДАНИЕ 1: Монитор сайтов ---
    def setup_task1(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Монитор сайтов")

        btn = ttk.Button(frame, text="Проверить доступность", command=self.check_sites)
        btn.pack(pady=10)

        self.txt_sites = tk.Text(frame, height=20, width=80)
        self.txt_sites.pack(padx=10, pady=10)

    def check_sites(self):
        urls = ["https://github.com", "https://binance.com", "https://tomtit.tomsk.ru",
                "https://typicode.com", "https://tomtit-tomsk.ru"]
        self.txt_sites.delete(1.0, tk.END)
        for url in urls:
            try:
                r = requests.get(url, timeout=5, verify=False)
                res = f"{url} – {r.status_code} (Доступен)\n"
            except:
                res = f"{url} – Ошибка соединения\n"
            self.txt_sites.insert(tk.END, res)

    # --- ЗАДАНИЕ 2: Системный монитор ---
    def setup_task2(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Системный монитор")

        self.lbl_cpu = ttk.Label(frame, text="Загрузка CPU: ...", font=("Arial", 12))
        self.lbl_cpu.pack(pady=20)

        self.lbl_ram = ttk.Label(frame, text="Оперативная память: ...", font=("Arial", 12))
        self.lbl_ram.pack(pady=20)

        self.lbl_disk = ttk.Label(frame, text="Загрузка диска: ...", font=("Arial", 12))
        self.lbl_disk.pack(pady=20)

        ttk.Button(frame, text="Обновить данные", command=self.update_sys_info).pack()

    def update_sys_info(self):
        self.lbl_cpu.config(text=f"Загрузка CPU: {psutil.cpu_percent()}%")
        ram = psutil.virtual_memory()
        self.lbl_ram.config(text=f"Память: {ram.percent}% (Использовано {ram.used // (1024 ** 2)} МБ)")
        disk = psutil.disk_usage('/')
        self.lbl_disk.config(text=f"Загрузка диска: {disk.percent}%")

    # --- ЗАДАНИЕ 3: Курсы валют ---
    def setup_task3(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Курсы валют")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", padx=10)

        ttk.Button(btn_frame, text="Загрузить курсы", command=self.load_currency).pack(side="left", padx=5)

        self.currency_tree = ttk.Treeview(frame, columns=("Code", "Value", "Name"), show="headings")
        self.currency_tree.heading("Code", text="Код")
        self.currency_tree.heading("Value", text="Курс (руб)")
        self.currency_tree.heading("Name", text="Валюта")
        self.currency_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def load_currency(self):
        url = "https://cbr-xml-daily.ru"
        try:
            r = requests.get(url, timeout=10, verify=False)
            data = r.json()['Valute']
            self.currency_tree.delete(*self.currency_tree.get_children())
            for code, info in data.items():
                self.currency_tree.insert("", "end", values=(code, info['Value'], info['Name']))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    # --- ЗАДАНИЕ 4: GitHub API ---
    def setup_task4(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="GitHub Поиск")

        top = ttk.Frame(frame)
        top.pack(pady=10)

        ttk.Label(top, text="Логин GitHub:").pack(side="left")
        self.ent_user = ttk.Entry(top)
        self.ent_user.pack(side="left", padx=5)
        ttk.Button(top, text="Найти профиль", command=self.search_github).pack(side="left")

        self.txt_github = tk.Text(frame, height=15, width=70)
        self.txt_github.pack(padx=10, pady=10)

    def search_github(self):
        user = self.ent_user.get()
        if not user: return
        try:
            r = requests.get(f"https://github.com{user}")
            if r.status_code == 200:
                d = r.json()
                info = f"Имя: {d.get('name', 'Нет')}\n"
                info += f"Репозиториев: {d['public_repos']}\n"
                info += f"Подписчиков: {d['followers']}\n"
                info += f"Ссылка: {d['html_url']}"
                self.txt_github.delete(1.0, tk.END)
                self.txt_github.insert(tk.END, info)
            else:
                messagebox.showwarning("Внимание", "Пользователь не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    import urllib3

    urllib3.disable_warnings()

    root = tk.Tk()
    app = PracticeApp(root)
    root.mainloop()
