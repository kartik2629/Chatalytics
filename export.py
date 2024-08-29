import pdfkit
import pandas as pd

def export_to_csv(df, filename="export.csv"):
    df.to_csv(filename, index=False)

def export_to_pdf(html_content, filename="export.pdf"):
    pdfkit.from_string(html_content, filename)
