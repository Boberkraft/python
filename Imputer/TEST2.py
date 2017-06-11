import pdfkit
path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path)
pdfkit.from_url('http://localhost:5000/', 'out3.pdf', configuration=config)


# import weasyprint
# pdf = weasyprint.HTML('http://127.0.0.1:5000/').write_png()
# print(len(pdf))
# open('google.pdf','wb').write(pdf)