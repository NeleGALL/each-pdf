import os
import sys
import subprocess

from sphinx.builders import Builder
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

class CustomBuilder(Builder):
    name = 'each-pdf'

    def init(self):
        pass

    def write(self, *ignored):
        build_dir = self.env.app.builder.outdir

        tasks = []
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                if file.endswith('.html'):
                    source_html_path = os.path.join(root, file)
                    output_pdf_path = os.path.join(root, file.replace('.html', '.pdf'))
                    tasks.append((source_html_path, output_pdf_path, file, build_dir))

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.run_script, task[0], task[1], task[2], task[3]) for task in tasks]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")

    def run_script(self, source_html_path, output_pdf_path, file, build_dir):
        command = [sys.executable, str(Path(__file__).parent) + '/convert.py', source_html_path, output_pdf_path, str(self.env.app.builder.srcdir) + "/sphinx-each-pdf.css"]
        relapth = os.path.relpath(source_html_path, start=build_dir)
        try:
            subprocess.run(command, check=True)
            print(f'{relapth}')
        except subprocess.CalledProcessError as e:
            print(f'Error {file}: {e}')

    def get_outdated_docs(self):
        return []