import tkinter as tk

class LatexFormatter:
    def __init__(self):
        self.font = "Times New Roman"   # шрифт
        self.font_size = "14pt"        # размер шрифта
        self.page_geometry = "top=20mm, bottom=20mm, left=30mm, right=10mm"  # границы листа
        self.paragraph_indent = "1.25cm"  # красная строка
        self.spacing = "1.5"           # полуторный интервал

    def format_text(self, text):
        # Замена переносов строк на формат LaTeX
        return text.replace("\n", "\n\n")

    def generate_latex_content(self, name_of_work, intro_text, main_text, conclusion_text, references_text):
        # Формирование содержимого LaTeX
        latex_content = f"""
        \\documentclass[a4paper,{self.font_size}]{{article}}
        \\usepackage{{fontspec}}
        \\setmainfont{{{self.font}}}
        \\usepackage{{geometry}}
        \\geometry{{{self.page_geometry}}}
        \\usepackage{{setspace}}
        \\onehalfspacing
        \\usepackage[utf8]{{inputenc}}
        \\usepackage[russian]{{babel}}
        \\usepackage{{tocloft}}
        \\usepackage{{indentfirst}}
        \\setlength{{\\parindent}}{{{self.paragraph_indent}}}

        % Настройки для содержания
        \\renewcommand{{\\cftsecleader}}{{\\cftdotfill{{\\cftdotsep}}}}
        \\renewcommand{{\\cftsecfont}}{{\\normalsize\\bfseries}}
        \\renewcommand{{\\cftsecpagefont}}{{\\normalsize}}
        \\setlength{{\\cftbeforesecskip}}{{0.5em}}

        \\begin{{document}}

        \\newpage
        \\tableofcontents

        \\newpage
        \\section*{{Введение}}
        {self.format_text(intro_text)}

        \\newpage
        \\section{{Основная часть}}
        {self.format_text(main_text)}

        \\newpage
        \\section*{{Заключение}}
        {self.format_text(conclusion_text)}

        \\newpage
        \\section*{{Список литературы}}
        \\begin{{enumerate}}
            {references_text}
        \\end{{enumerate}}

        \\end{{document}}
        """
        return latex_content

class LatexFileCreator:
    def __init__(self):
        self.formatter = LatexFormatter()

    def create_latex_file(self, name_of_work, intro_text, main_text, conclusion_text, references_text):
        formatted_references = "\n".join([f"\\item {item.strip()}" for item in references_text.split("\n") if item.strip()])
        latex_content = self.formatter.generate_latex_content(name_of_work, intro_text, main_text, conclusion_text, formatted_references)

        with open(f"{name_of_work}.tex", "w", encoding="utf-8") as file:
            file.write(latex_content)

def submit_data():
    name_of_file = name.get("1.0", tk.END).strip()
    intro_text = intro_entry.get("1.0", tk.END).strip()
    main_text = main_entry.get("1.0", tk.END).strip()
    conclusion_text = conclusion_entry.get("1.0", tk.END).strip()
    references_text = references_entry.get("1.0", tk.END).strip()

    creator = LatexFileCreator()
    creator.create_latex_file(name_of_file, intro_text, main_text, conclusion_text, references_text)

# Создаем основное окно
root = tk.Tk()
root.title("LaTeX Generator")

# Создаем метки и текстовые поля для каждого раздела
tk.Label(root, text="Название работы").grid(row=0, column=0)
name = tk.Text(root, height=2, width=50)
name.grid(row=0, column=1)

tk.Label(root, text="Введение").grid(row=1, column=0)
intro_entry = tk.Text(root, height=5, width=50)
intro_entry.grid(row=1, column=1)

tk.Label(root, text="Основная часть").grid(row=2, column=0)
main_entry = tk.Text(root, height=10, width=50)
main_entry.grid(row=2, column=1)

tk.Label(root, text="Заключение").grid(row=3, column=0)
conclusion_entry = tk.Text(root, height=5, width=50)
conclusion_entry.grid(row=3, column=1)

tk.Label(root, text="Список литературы").grid(row=4, column=0)
references_entry = tk.Text(root, height=5, width=50)
references_entry.grid(row=4, column=1)

# Кнопка для отправки данных
submit_button = tk.Button(root, text="Сгенерировать LaTeX файл", command=submit_data)
submit_button.grid(row=5, column=1)

# Запуск главного цикла программы
root.mainloop()
