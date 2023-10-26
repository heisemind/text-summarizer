from text_summarizer import TextSummarizer
from pdf_builder import PdfBuilder


long_file = 'bert_guide.txt'

summarizer = TextSummarizer()
title, summary = summarizer.digest(long_file)

builder = PdfBuilder()
builder.new_report(title, summary)
