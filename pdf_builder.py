from uuid import uuid4 as uuid
import os
import shutil


class PdfBuilder:
    """
    A class for generating PDF reports from a LaTeX template.
    """

    def new_report(self, title: str, summary: str) -> None:
        """
        Create a new report with the provided title and summary.

        Parameters:
        - title (str): The title of the report.
        - summary (str): The summary text for the report.

        Returns:
        None
        """
        pid = str(uuid())
        os.makedirs(f'/tmp/{pid}/latex/')
        os.system(f'cp -rf latex_template/* /tmp/{pid}/latex')
        self.update_main_tex(pid, title, summary)
        self.compile(pid)

    def compile(self, pid: str) -> None:
        """
        Compile the LaTeX report into a PDF.

        Parameters:
        - pid (str): The process ID for the report.

        Returns:
        None
        """
        os.system(
            f'cd /tmp/{pid}/latex; pdflatex -interaction=nonstopmode main.tex > /dev/null')
        os.system(f'cp /tmp/{pid}/latex/main.pdf out/{pid}.pdf')
        shutil.rmtree(f'/tmp/{pid}', ignore_errors=True)

    def update_main_tex(self, process_id: str, title: str, summary: str) -> None:
        """
        Update the main.tex file with the title and summary.

        Parameters:
        - process_id (str): The process ID for the report.
        - title (str): The title of the report.
        - summary (str): The summary text for the report.

        Returns:
        None
        """
        process_path = f'/tmp/{process_id}'
        with open(f'{process_path}/latex/main.tex', 'r') as f:
            content = f.read()
        content = content.replace('#TITLE', title)
        content = content.replace('#TEXT', self.generate_paragraphs(summary))
        with open(f'{process_path}/latex/main.tex', 'w') as f:
            f.write(content)

    def generate_paragraphs(self, summary: str) -> str:
        """
        Generate LaTeX-formatted paragraphs from the summary text.

        Parameters:
        - summary (str): The summary text for the report.

        Returns:
        str: LaTeX-formatted paragraphs.
        """
        paragraphs = [
            f'\\para{{{p.strip()}}}' for p in summary.split('\n') if p != '']
        return '\n    '.join(paragraphs)
