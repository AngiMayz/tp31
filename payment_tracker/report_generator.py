from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os

REPORTS_DIR = "reports"

def ensure_reports_dir():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def generate_report(username, payments, period="", category=""):
    ensure_reports_dir()
    filename = os.path.join(REPORTS_DIR, f"report_{username}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Заголовок отчёта
    title_text = "Список платежей"
    if period:
        title_text += f"<br/><i>Период: {period}</i>"
    if category and category != "-":
        title_text += f"<br/><i>Категория: {category}</i>"
    elements.append(Paragraph(title_text, styles['Title']))
    elements.append(Spacer(1, 24))

    categories = {}
    for p in payments:
        cat = p["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    total_sum = sum(p["total"] for p in payments)

    for cat, items in categories.items():
        elements.append(Paragraph(f"<b>Категория: {cat}</b>", styles['Normal']))
        data = [["Дата", "Назначение", "Цена", "Количество", "Сумма"]]
        for item in sorted(items, key=lambda x: x["date"]):
            data.append([
                item["date"][:10],
                item["purpose"],
                f"{item['price']:.2f} руб.",
                str(item["quantity"]),
                f"{item['total']:.2f} руб."
            ])
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 24))
    elements.append(Paragraph(f"<b>Итого: {total_sum:.2f} руб.</b>", styles['Normal']))

    def on_page(canvas, document):
        canvas.saveState()
        page_num = canvas.getPageNumber()
        text = f"ФИО: {username}, Страница {page_num}"
        canvas.setFont('Times-Roman', 9)
        canvas.drawString(450, 20, text)
        canvas.restoreState()

    doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)
    return filename