from fpdf import FPDF

class CreatePDF:
    def __init__(self, username, source, destination, route, cost, mst, couponName, couponDiscount, totalCost):
        self.username = username
        self.source = source
        self.destination = destination
        self.route = route
        self.cost = cost
        self.mst = mst
        self.couponName = couponName
        self.couponDiscount = couponDiscount
        self.totalCost = totalCost

    def createPDF(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Poppins", size = 15)

