import sys
import os
from playwright.sync_api import sync_playwright

def convert_html_to_pdf(html_path, pdf_path, css_path=None):
    with sync_playwright() as p:
        # Запуск Chromium
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Загрузка HTML
        page.goto(f'file://{os.path.abspath(html_path)}', wait_until='networkidle')

        # Добавление кастомного CSS
        if css_path and os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as css_file:
                custom_css = css_file.read()
                page.add_style_tag(content=custom_css)

        # Удаление ссылок вокруг изображений
        page.evaluate("""
            document.querySelectorAll('a > img').forEach(img => {
                const parent = img.parentElement;
                if (parent.tagName.toLowerCase() === 'a') {
                    parent.replaceWith(img); // Убираем ссылку, оставляем изображение
                }
            });
        """)

        # Конвертация в PDF
        page.pdf(
            path=pdf_path,
            format='A4',
            print_background=True  # Включить фон
        )

        # Закрытие браузера
        browser.close()

if __name__ == "__main__":
    # Получение аргументов из командной строки
    if len(sys.argv) < 3:
        print("Использование: python script.py <путь_к_html> <путь_к_pdf> [путь_к_css]")
        sys.exit(1)

    html_path = sys.argv[1]
    pdf_path = sys.argv[2]
    css_path = sys.argv[3] if len(sys.argv) > 3 else None

    convert_html_to_pdf(html_path, pdf_path, css_path)