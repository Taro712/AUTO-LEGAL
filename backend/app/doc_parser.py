import pdf2image, docx2pdf, pytesseract
import os
from PIL import Image

DATA_PATH = "data"

def get_all_files(data_path):
    # Get all files in the directory (pdf, docx, doc, png, jpg, jpeg, txt)
    exts = [".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".txt"]
    files = []
    for root, filenames in os.walk(data_path):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in exts:
                files.append(os.path.join(root, filename))
    return files

def docx_to_pdf(docx_path, pdf_path):
    docx2pdf.convert(docx_path, pdf_path)
    return pdf_path

def pdf_to_img(pdf_path):
    return pdf2image.convert_from_path(pdf_path)

def img_to_text(img):
    # img can be a path or a PIL Image
    if isinstance(img, str):
        img = Image.open(img)
    return pytesseract.image_to_string(img)

class doctype:
    def __init__(self, doc_path):
        self.doc_path = doc_path

    def to_text(self):
        ext = os.path.splitext(self.doc_path)[1].lower()
        text = ""
        if ext in [".docx", ".doc"]:
            # Convert DOCX to PDF
            pdf_path = self.doc_path.replace(ext, ".pdf")
            docx_to_pdf(self.doc_path, pdf_path)
            images = pdf_to_img(pdf_path)
            for img in images:
                text += img_to_text(img) + "\n"
        elif ext == ".pdf":
            images = pdf_to_img(self.doc_path)
            for img in images:
                text += img_to_text(img) + "\n"
        elif ext in [".png", ".jpg", ".jpeg"]:
            text = img_to_text(self.doc_path)
        elif ext == ".txt":
            with open(self.doc_path, 'r', encoding='utf-8') as file:
                text = file.read()
        else:
            text = "UNKNOWN FILEPATH"
        return text

if __name__ == "__main__":
    file_path = input("Enter the path to your file: ")
    open("data\input.img","a").write(file_path)
    if not os.path.isfile(file_path):
        print("File does not exist.")
    else:
        doc = doctype(file_path)
        extracted_text = doc.to_text()
        m = extracted_text
        print(m)
        # print(f"File: {file_path}\nExtracted Text:\n{extracted_text}\n{'-'*40}\n") 
