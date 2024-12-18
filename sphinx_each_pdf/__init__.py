from sphinx.application import Sphinx
from sphinx.util.logging import getLogger
from .sphinx_each_pdf import CustomBuilder

logger = getLogger(__name__)

def setup(app: Sphinx):
    # Подключение конвертера
    app.add_builder(CustomBuilder)
    
    # Подключение обработчика
    app.connect("html-page-context", add_pdf_link)

    logger.info("Each-PDF is here!")
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

def add_pdf_link(app, pagename, templatename, context, doctree):
    """
    Добавляет ссылку на PDF-версию текущей страницы.
    """
    # Формируем ссылку на PDF
    pdf_link = f"/{pagename}.pdf"
    
    # Добавляем в контекст
    context['pdf_link'] = pdf_link