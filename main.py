from text_summarizer import TextSummarizer
from pdf_builder import PdfBuilder

# File path that want to summarize.
long_file = 'bert_guide.txt'

# Use the TextSummarizer to generate a title and summary.
summarizer = TextSummarizer()
title, summary = summarizer.digest(long_file)

# Build the report using PdfBuilder.
builder = PdfBuilder()
builder.new_report(title, summary)
