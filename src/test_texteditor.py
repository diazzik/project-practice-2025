import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
import os


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Текстовый редактор")
        self.root.geometry("800x600")
        self.current_file = None  # Текущий открытый файл
        self.setup_ui()
        
    def setup_ui(self):
        # Создание основного текстового виджета с полосой прокрутки
        self.text = tk.Text(self.root, wrap="word", undo=True)
        self.scrollbar = tk.Scrollbar(self.root, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.text.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Создание строки меню
        self.menubar = tk.Menu(self.root)
        
        # Меню "Файл"
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Создать", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_editor)
        self.menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню "Правка"
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        edit_menu.add_command(label="Отменить", command=self.text.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторить", command=self.text.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Копировать", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Вставить", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Выделить всё", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Очистить всё", command=self.clear_all)
        self.menubar.add_cascade(label="Правка", menu=edit_menu)
        
        # Меню "Формат"
        format_menu = tk.Menu(self.menubar, tearoff=0)
        
        # Подменю "Шрифт"
        font_menu = tk.Menu(format_menu, tearoff=0)
        self.font_family = tk.StringVar()
        self.font_family.set("Arial")
        
        # Добавление всех доступных шрифтов
        fonts = sorted(tkfont.families())
        for f in fonts:
            if not f.startswith("@"):  # Пропускаем вертикальные шрифты
                font_menu.add_radiobutton(label=f, variable=self.font_family, 
                                        command=self.change_font)
        
        # Подменю "Размер шрифта"
        size_menu = tk.Menu(format_menu, tearoff=0)
        self.font_size = tk.IntVar()
        self.font_size.set(12)
        
        for size in range(8, 33, 2):
            size_menu.add_radiobutton(label=str(size), variable=self.font_size, 
                                    command=self.change_font)
        
        format_menu.add_cascade(label="Шрифт", menu=font_menu)
        format_menu.add_cascade(label="Размер шрифта", menu=size_menu)
        format_menu.add_separator()
        
        # Форматирование текста
        self.bold_on = tk.BooleanVar()
        self.italic_on = tk.BooleanVar()
        format_menu.add_checkbutton(label="Жирный", variable=self.bold_on, 
                                  command=self.change_font, accelerator="Ctrl+B")
        format_menu.add_checkbutton(label="Курсив", variable=self.italic_on, 
                                  command=self.change_font, accelerator="Ctrl+I")
        
        self.menubar.add_cascade(label="Формат", menu=format_menu)
        
        # Меню "Справка"
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        self.menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=self.menubar)
        
        # Строка состояния
        self.status_bar = tk.Label(self.root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Горячие клавиши
        self.root.bind_all("<Control-n>", lambda event: self.new_file())
        self.root.bind_all("<Control-o>", lambda event: self.open_file())
        self.root.bind_all("<Control-s>", lambda event: self.save_file())
        self.root.bind_all("<Control-b>", lambda event: self.toggle_bold())
        self.root.bind_all("<Control-i>", lambda event: self.toggle_italic())
        
        # Установка начального шрифта
        self.change_font()
        
    def toggle_bold(self):
        """Переключение жирного начертания"""
        self.bold_on.set(not self.bold_on.get())
        self.change_font()
    
    def toggle_italic(self):
        """Переключение курсивного начертания"""
        self.italic_on.set(not self.italic_on.get())
        self.change_font()
    
    def change_font(self):
        """Изменение шрифта текста"""
        font_family = self.font_family.get()
        font_size = self.font_size.get()
        weight = "bold" if self.bold_on.get() else "normal"
        slant = "italic" if self.italic_on.get() else "roman"
        
        self.text.configure(font=(font_family, font_size, weight, slant))
    
    def new_file(self):
        """Создание нового файла"""
        self.text.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Текстовый редактор - Новый файл")
        self.status_bar.config(text="Создан новый файл")
    
    def open_file(self):
        """Открытие файла"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(1.0, content)
            
            self.current_file = file_path
            self.root.title(f"Текстовый редактор - {os.path.basename(file_path)}")
            self.status_bar.config(text=f"Открыт: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_file(self):
        """Сохранение файла"""
        if self.current_file:
            try:
                content = self.text.get(1.0, tk.END)
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(content)
                self.status_bar.config(text=f"Сохранено: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            self.save_as()
    
    def save_as(self):
        """Сохранение файла с указанием имени"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            content = self.text.get(1.0, tk.END)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            
            self.current_file = file_path
            self.root.title(f"Текстовый редактор - {os.path.basename(file_path)}")
            self.status_bar.config(text=f"Сохранено как: {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def exit_editor(self):
        """Выход из программы"""
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            self.root.destroy()
    
    def cut_text(self):
        """Вырезание текста"""
        self.text.event_generate("<<Cut>>")
    
    def copy_text(self):
        """Копирование текста"""
        self.text.event_generate("<<Copy>>")
    
    def paste_text(self):
        """Вставка текста"""
        self.text.event_generate("<<Paste>>")
    
    def select_all(self):
        """Выделение всего текста"""
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return "break"
    
    def clear_all(self):
        """Очистка всего текста"""
        self.text.delete(1.0, tk.END)
    
    def show_about(self):
        """Показ информации о программе"""
        messagebox.showinfo(
            "О программе",
            "Простой текстовый редактор\n\n"
            "Возможности:\n"
            "- Открытие, сохранение и редактирование текстовых файлов\n"
            "- Различные шрифты и форматирование текста\n"
            "- Отмена/повтор действий\n"
            "- Горячие клавиши"
        )


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()