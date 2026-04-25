import tkinter as tk
from tkinter import messagebox
import json
import random
import os

# Путь к файлу данных. 
# Убедитесь, что папка 'data' существует в том же каталоге, что и app.py.
DATA_FILE = 'data/tasks.json'

def load_tasks():
    """
    Загружает задачи из файла JSON.
    Если файл не существует или пуст, возвращает пустой список.
    """
    # Проверяем, существует ли файл и не является ли он пустым
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Обрабатываем случай, если файл поврежден или возникла ошибка чтения
        messagebox.showwarning("Внимание", "Файл данных поврежден. Будет создан новый.")
        return []

def save_tasks(tasks):
    """
    Сохраняет список задач в файл JSON.
    Создает папку 'data', если она не существует.
    """
    # Создаем папку data, если ее нет
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except IOError as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.tasks = load_tasks() # Загружаем задачи при запуске

        self.create_widgets()
        self.update_listbox()

    def create_widgets(self):
        # --- Блок ввода ---
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_entry = tk.Entry(self.root, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='we')

        tk.Label(self.root, text="Описание:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.desc_entry = tk.Entry(self.root, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='we')

        tk.Label(self.root, text="Приоритет (1-5):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.prio_entry = tk.Entry(self.root, width=5)
        self.prio_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # --- Блок кнопок ---
        tk.Button(self.root, text="Добавить", command=self.add_task).grid(row=3, column=0, columnspan=3, pady=5)
        
        # Фильтр по названию (используем то же поле)
        tk.Button(self.root, text="Фильтровать по названию", command=self.filter_by_title).grid(row=4, column=0, pady=2)
        
        # Фильтр по приоритету (используем то же поле)
        tk.Button(self.root, text="Фильтровать по приоритету", command=self.filter_by_priority).grid(row=4, column=1, pady=2)
        
        tk.Button(self.root, text="Удалить", command=self.delete_task).grid(row=4, column=2, pady=2)

        # --- Блок списка задач ---
        self.listbox = tk.Listbox(self.root, width=60, height=15)
        self.listbox.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    def add_task(self):
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get().strip()
        prio = self.prio_entry.get().strip()

        # Валидация ввода
        if not title:
            messagebox.showerror("Ошибка", "Название задачи обязательно!")
            return

        if not prio.isdigit() or not (1 <= int(prio) <= 5):
            messagebox.showerror("Ошибка", "Приоритет должен быть числом от 1 до 5.")
            return

        task = {
            "id": random.randint(10000, 99999), # ID стал 5-значным для наглядности
            "title": title,
            "description": desc,
            "priority": int(prio)
        }
        
        self.tasks.append(task)
        save_tasks(self.tasks)
        
        # Очищаем поля и обновляем список после добавления
        self.clear_entries()
        self.update_listbox()

    def filter_by_title(self):
        """Фильтрует задачи по подстроке в названии."""
        filter_text = self.title_entry.get().lower()
        
        if not filter_text:
            # Если поле пустое - показываем все задачи
            filtered_tasks = self.tasks
            messagebox.showinfo("Фильтр", "Показаны все задачи.")
        else:
            filtered_tasks = [t for t in self.tasks if filter_text in t["title"].lower()]
        
        self.update_listbox(filtered_tasks)

    def filter_by_priority(self):
        """Фильтрует задачи по точному значению приоритета."""
        prio_text = self.prio_entry.get().strip()
        
        if not prio_text.isdigit():
            messagebox.showerror("Ошибка", "Введите число для фильтрации по приоритету.")
            return

        filter_prio = int(prio_text)
        
        if not (1 <= filter_prio <= 5):
            messagebox.showerror("Ошибка", "Приоритет для фильтрации должен быть от 1 до 5.")
            return

        filtered_tasks = [t for t in self.tasks if t["priority"] == filter_prio]
        
        if not filtered_tasks:
            messagebox.showinfo("Результат", "Задач с таким приоритетом не найдено.")
        
        self.update_listbox(filtered_tasks)

    def delete_task(self):
        """Удаляет выбранную в списке задачу."""
        selection = self.listbox.curselection()
        
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления.")
            return

        # Получаем ID из выделенной строки (первый элемент до разделителя ' | ')
        task_id_str = self.listbox.get(selection[0]).split(' | ')[0]
        
        try:
            task_id = int(task_id_str)
            
            # Фильтруем список задач на стороне приложения
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            
            # Сохраняем обновленный список в файл
            save_tasks(self.tasks)
            
            # Обновляем интерфейс
            self.update_listbox()
            
            # Очищаем поля ввода после удаления
            self.clear_entries()
            
        except (ValueError, IndexError):
            messagebox.showerror("Ошибка", "Не удалось определить ID задачи.")

    def update_listbox(self, tasks_to_display=None):
        """Обновляет видимый список задач в интерфейсе."""
        self.listbox.delete(0, tk.END) # Очищаем список

        # Используем отфильтрованный список или полный список задач
        display_tasks = tasks_to_display if tasks_to_display is not None else self.tasks

        for t in display_tasks:
            self.listbox.insert(tk.END,
                f"{t['id']} | {t['title']} | Приоритет: {t['priority']}")

    def clear_entries(self):
        """Очищает поля ввода."""
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.prio_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    
    # Увеличиваем минимальный размер окна для удобства
    root.minsize(500, 450)
    
    app = TaskManagerApp(root)
    root.mainloop()