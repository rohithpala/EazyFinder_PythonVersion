from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

document = SimpleDocTemplate("table.pdf", pagesize=letter)
items = []
data = [['0', '2', '4', '6', '8'],
        ['10', '12', '14', '16', '18']]
t = Table(data, 5 * [1 * inch], 2 * [1 * inch])
t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                       ('VALIGN', (-1, -1), (-1, -1), 'RIGHT'),
                       ('ALIGN', (-1, -1), (-1, -1), 'RIGHT'),
                       ('VALIGN', (-1, -1), (-1, -1), 'TOP'),
                       ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
items.append(t)
document.build(items)
