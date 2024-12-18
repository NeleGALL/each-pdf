# User Guide for **Sphinx-Each-PDF**

## Introduction
**Sphinx-Each-PDF** is a Sphinx extension that generates **a separate PDF file for each page** in a documentation project. 
It uses Playwright for rendering and integrates seamlessly with Sphinx. 
This is particularly useful for creating static websites where each page can be downloaded as an individual PDF.

---

## Installation

1. Ensure you have Python 3.8 or newer installed.
2. Install the package from PyPI:
   ```bash
   pip install sphinx-each-pdf
   ```

3. Install Chromium for Playwright (or any other supported engine, like Firefox or WebKit, based on your preference):
   ```bash
   playwright install chromium
   ```
   *You may replace `chromium` with `firefox` or `webkit` if desired.*

4. (Recommended) Install system dependencies for Chromium to ensure smooth operation:
   ```bash
   playwright install-deps chromium
   ```

---

## Package Structure

1. **convert.py**:
   - Contains the `convert_html_to_pdf` function, which converts individual HTML pages to PDFs.
   - Utilizes Playwright for rendering HTML with CSS support.
   - Removes unnecessary links around images for cleaner output.

2. **each_pdf.py**:
   - Defines the `CustomBuilder` class, extending Sphinx functionality.
   - Scans the Sphinx build directory for HTML files and generates a **separate PDF for each page**.

3. **__init__.py**:
   - Integrates the extension with Sphinx by adding the custom **Sphinx-Each-PDF** builder.
   - Adds PDF download links for individual pages in the generated HTML.

---

## Adding a PDF Download Link

To automatically include a download link to the PDF version of each page in the generated documentation, follow these steps:

1. **Enable the `pdf_link` Variable**:
   - The extension automatically sets a Sphinx variable `pdf_link` in the context of each page. This variable contains the relative path to the PDF file for the current page.

2. **Customize the Page Template**:
   - Create or edit the `_templates/layout.html` file in your Sphinx project (or create the `_templates` directory if it does not exist).
   - Add the following block of code where you want the PDF download link to appear (e.g., in the footer or header):
     ```html
     {% if pdf_link %}
     <a href="{{ pdf_link }}" class="pdf-download-link">Download PDF</a>
     {% endif %}
     ```
   - This will insert a link to the corresponding PDF file for each page if it exists.

3. **Configure Sphinx to Use Custom Templates**:
   - In your `conf.py` file, add the `_templates` directory to the `templates_path` configuration:
     ```python
     templates_path = ['_templates']
     ```

4. **Apply Custom Styling (Optional)**:
   - Add CSS rules to style the link (e.g., in your custom CSS file or the default `sphinx-each-pdf.css`):
     ```css
     .pdf-download-link {
         display: inline-block;
         margin-top: 10px;
         padding: 5px 10px;
         background-color: #007BFF;
         color: white;
         text-decoration: none;
         border-radius: 5px;
     }

     .pdf-download-link:hover {
         background-color: #0056b3;
     }
     ```

---

## Usage

### Connecting the Extension

You can enable the **Sphinx-Each-PDF** extension in Sphinx in one of two ways:

1. **Automatic Builder Mode**:
   - Add the following line to your `conf.py` file:
     ```python
     extensions.append('sphinx_each_pdf')
     ```

2. **Manual Extension Declaration**:
   - Add `'sphinx_each_pdf'` to your list of Sphinx extensions:
     ```python
     extensions = [
         'sphinx.ext.autodoc',
         'sphinx_each_pdf',  # Add here
     ]
     ```

### Running the Build

After adding the extension, run the following Sphinx build command:

```bash
sphinx-build -b each-pdf source_dir build_dir
```

Here:
- `source_dir` is the directory containing your Sphinx source files (e.g., `docs`).
- `build_dir` is the directory where the generated files will be placed (e.g., `_build`).

After the build completes, you will find **a separate PDF file for each HTML page** in the `build_dir`.

### Custom Styles

By default, the extension applies styles from the `sphinx-each-pdf.css` file in your Sphinx project directory. 
You can replace this file or specify a custom CSS path during the conversion process. The default CSS file path is:

```bash
<source_dir>/sphinx-each-pdf.css
```

---

## Manual HTML to PDF Conversion

If needed, you can use **convert.py** as a standalone script to convert an individual HTML file to a PDF:

```bash
python convert.py <html_path> <pdf_path> [css_path]
```

- `<html_path>`: Path to the source HTML file.
- `<pdf_path>`: Path to save the resulting PDF.
- `[css_path]`: (Optional) Path to a CSS file for custom styling.

---

## Notes

- The tool uses Playwright, which supports Chromium, Firefox, and WebKit. By default, `chromium` is recommended. 
  However, you can switch to another engine (e.g., Firefox or WebKit) by replacing `chromium` in the installation command:
  ```bash
  playwright install <engine>
  ```

- Install system dependencies for your chosen engine to avoid runtime errors:
  ```bash
  playwright install-deps <engine>
  ```
  Replace `<engine>` with `chromium`, `firefox`, or `webkit`.

- The **each_pdf.py** script uses multithreading to process multiple files efficiently.

---

## License
This tool is distributed under the MIT License.
