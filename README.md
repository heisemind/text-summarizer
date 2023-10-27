# Text Summarizer

This project provides a solution for summarizing long text documents and generating PDF reports from them using Python. It leverages the capabilities of the Langchain library for text summarization and the PdfBuilder class for creating PDF reports.

**Table of Contents**

- Description
- Installation
- License
- Check Out Heise Mind

**Description**

This project contains two main components:

1. `text_summarizer`: Responsable for summarizing text using LangChain and OpenAI's LLM.
2. `pdf_builder`: Includes the operational part of compiling the LaTeX file in /tmp.
3. `latex_template/`: Template used to build the report.

**Installation**

1. Clone the repository:

```bash
   git clone https://github.com/heisemind/text-summarizer.git
   cd text-summarizer
```

2. Install the required Python dependencies:

```bash
   pip install -r requirements.txt
```

3. Install the texlive package (Arch Linux):

```bash
   pacman -Syy texlive
```

**License**

This project is licensed under the MIT License.

---

**Check Out Heise Mind**

If you're interested in AI, check out my YouTube channel, [Heise Mind](https://www.youtube.com/@HeiseMind). I create deep-tech content about a variety of tech-related topics.

You might find my video on "Summarizing Text into PDF Reports" particularly helpful: [Watch the Video](https://www.youtube.com/watch?v=vuj69j60_nc).
