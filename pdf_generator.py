from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_pdf(patrones):
    """Genera un PDF con los patrones encontrados por el autómata."""
    filename = "patrones_automata.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 50, "Patrones de autómata encontrados:")

    # Línea de separación debajo del título
    c.line(100, height - 60, width - 100, height - 60)

    # Listar los patrones
    c.setFont("Helvetica", 12)
    y_position = height - 80
    for patron in patrones:
        if y_position < 50:  # Crear una nueva página si se acaba el espacio
            c.showPage()
            y_position = height - 50
        c.drawString(100, y_position, patron)
        y_position -= 20

    c.save()
    return filename
