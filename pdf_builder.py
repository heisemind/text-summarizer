from uuid import uuid4 as uuid
import os
import shutil


class PdfBuilder:
    def new_report(self, title, summary):
        pid = str(uuid())
        os.makedirs(f'/tmp/{pid}/latex/')
        os.system(f'cp -rf latex_template/* /tmp/{pid}/latex')
        self.update_main_tex(pid, title, summary)
        self.compile(pid)

    def compile(self, pid):
        os.system(
            f'cd /tmp/{pid}/latex; pdflatex -interaction=nonstopmode main.tex > /dev/null')
        os.system(f'cp /tmp/{pid}/latex/main.pdf out/{pid}.pdf')
        shutil.rmtree(f'/tmp/{pid}', ignore_errors=True)

    def update_main_tex(self, process_id, title, summary):
        process_path = f'/tmp/{process_id}'
        with open(f'{process_path}/latex/main.tex', 'r') as f:
            content = f.read()
        content = content.replace('#TITLE', title)
        content = content.replace('#TEXT', self.generate_paragraphs(summary))
        with open(f'{process_path}/latex/main.tex', 'w') as f:
            f.write(content)

    def generate_paragraphs(self, summary):
        paragraphs = [
            f'\\para{{{p.strip()}}}' for p in summary.split('\n') if p != '']
        return '\n    '.join(paragraphs)


if __name__ == '__main__':
    builder = PdfBuilder()
    title = 'Example Title'
    summary = """This is a summary about something."""
    builder.new_report(title, summary)
