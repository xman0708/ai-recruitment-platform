from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import platform
import os

pdf_path = os.path.join(os.path.dirname(__file__), "dummy_resume_real.pdf")
c = canvas.Canvas(pdf_path, pagesize=letter)
c.setFont("Helvetica", 14)

resume_lines = [
    "Name: Li Ming",
    "Phone: +8613812345678",
    "Email: liming@example.com",
    "",
    "Education:",
    "Tsinghua University - Bachelor of Computer Science (2018-2022)",
    "",
    "Experience:",
    "ByteDance - Backend Engineer (2022-Present)",
    "Developed high-performance Go microservices and managed Redis clusters.",
    "",
    "Skills:",
    "Python, Go, Vue.js, MySQL, Redis, Docker"
]

y_position = 750
for line in resume_lines:
    c.drawString(50, y_position, line)
    y_position -= 20

c.save()
print(f"Created PDF: {pdf_path}")
