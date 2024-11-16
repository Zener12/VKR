from flask import Flask, render_template, request, send_from_directory
import os
import time

app = Flask(__name__)

# Указываем папку для сохранения файлов
OUTPUT_DIR = "C:\\Users\\user\\Desktop\\Диплом"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Создаем папку, если она отсутствует

class LatexFormatter:
    def __init__(self):
        self.font = "Times New Roman"
        self.font_size = "14pt"
        self.page_geometry = "top=20mm, bottom=20mm, left=30mm, right=10mm"
        self.paragraph_indent = "1.25cm"
        self.spacing = "1.5"

    def format_text(self, text):
        return text

    def generate_latex_content(self, name_of_work, annotation_text, intro_text, chapter1_text, chapter2_text, chapter3_text, conclusion_text, references_text):
        formatted_references = "\n".join([f"\\item {item.strip()}" for item in references_text.split("\n") if item.strip()])
        return f"""
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
        \\pagestyle{{plain}}
        \\setcounter{{secnumdepth}}{{0}}
        
        \\usepackage{{titlesec}}

        \\begin{{document}}

        \\tableofcontents
        
        \\newpage
        \\section*{{Аннотация}}
        \\addcontentsline{{toc}}{{section}}{{Аннотация}}
        {self.format_text(annotation_text)}
        
        \\newpage
        \\section*{{Введение}}
        \\addcontentsline{{toc}}{{section}}{{Введение}}
        {self.format_text(intro_text)}

        \\newpage
        \\section{{Глава 1}}
        {self.format_text(chapter1_text)}
        
        \\newpage
        \\section{{Глава 2}}
        {self.format_text(chapter2_text)}
        
        \\newpage
        \\section{{Глава 3}}
        {self.format_text(chapter3_text)}

        \\newpage
        \\section*{{Заключение}}
        \\addcontentsline{{toc}}{{section}}{{Заключение}}
        {self.format_text(conclusion_text)}

        \\newpage
        \\section*{{Список использованных источников}}
        \\addcontentsline{{toc}}{{section}}{{Список использованных источников}}
        \\begin{{enumerate}}
            {formatted_references}
        \\end{{enumerate}}

        \\end{{document}}
        """

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из формы
        name_of_work = request.form['name']
        annotation_text = request.form['annotation']
        intro_text = request.form['intro']
        chapter1_text = request.form['chapter1']
        chapter2_text = request.form['chapter2']
        chapter3_text = request.form['chapter3']
        conclusion_text = request.form['conclusion']
        references_text = request.form['references']

        # Генерация LaTeX-файла
        formatter = LatexFormatter()
        latex_content = formatter.generate_latex_content(name_of_work, annotation_text, intro_text, chapter1_text, chapter2_text, chapter3_text, conclusion_text, references_text)

        # Сохранение файла на сервер
        file_path = os.path.join(OUTPUT_DIR, f"{name_of_work}.tex")
        with open(file_path, "w", encoding="utf-8") as latex_file:
            latex_file.write(latex_content)

        # Ссылка на скачивание
        return f"""
        <h1>Файл успешно сгенерирован!</h1>
        <p>Скачать файл: <a href="/download/{name_of_work}">{name_of_work}.tex</a></p>
        """

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    # Отправляем файл из папки OUTPUT_DIR
    return send_from_directory(OUTPUT_DIR, f"{filename}.tex", as_attachment=True)

def clean_file(file_path):
    """Удаляет файл через 10 секунд после скачивания."""
    time.sleep(10)  # Ждем 10 секунд
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")

if __name__ == '__main__':
    app.run(debug=True)
