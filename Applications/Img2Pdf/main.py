from fpdf import FPDF
import os

pdf = FPDF()
path = "./images/"
ls = os.listdir(path)
imagelist = [path+img for img in ls]
for image in imagelist:
    pdf.add_page()
    pdf.image(image,0,0, 210, 300)
pdf.output("Result.pdf", "F")