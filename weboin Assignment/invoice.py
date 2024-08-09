import pandas as pd
from fpdf import FPDF
import os

class InvoicePDF(FPDF):
    def __init__(self):
        super().__init__()
        
    def header(self):
        self.set_fill_color(33, 46, 78)  # Navy blue
        self.rect(0, 0, 210, 50, 'F')  # Rectangle for background (A4 size, height adjusted)
        self.set_text_color(234, 209, 105)  # Golden yellow
        self.set_font('Times', 'B', 40)   # Font size and Font Style
        self.set_x(10)  
        self.cell(0, 30, "INVOICE", ln=1, align='L')
        self.ln(10)  
        self.set_text_color(33, 46, 78)

    def add_invoice_info(self, data):
        self.ln(20)
        self.set_font('Times', 'B', 18)
        self.set_text_color(234, 209, 105)
        self.cell(0, 5, f"INVOICE #{data['INVOICE No.']}", ln=1, align='L')
        self.set_font('Times', 'B', 10)
        self.set_text_color(33, 46, 78)
        self.cell(0, 10, f"Issued on {data['DATE']}", ln=1, align='L')
        self.ln(5)
        self.set_font('Times', 'B', 10)
        self.cell(0, 5, data['NAME'], ln=1, align='L')
        address_width = 63
        self.multi_cell(address_width, 5, f"NO: {data['ADDRESS']}", align='L')
        self.cell(0, 5, f"CONTACT NO: {data['CONTACT']}", ln=1, align='L')
        self.cell(0, 20, f"GST: {data['GSTIN']}", ln=1, align='L')

    def add_invoice_details(self, data):
        left_margin = 15
        right_margin = 15
        table_width = 210 - left_margin - right_margin
        col_padding = 20
        description_width = (table_width * 0.4) - col_padding
        qty_width = (table_width * 0.2) - col_padding
        price_width = (table_width * 0.2) - col_padding
        total_width = (table_width * 0.2) - col_padding

        self.set_left_margin(left_margin)
        self.set_right_margin(right_margin)

        self.set_font('Times', 'B', 10)
        self.set_text_color(234, 209, 105)  
        self.set_draw_color(33, 46, 78) 
        self.set_line_width(1)

        self.cell(description_width + col_padding, 10, "DESCRIPTION", border='B', align='L', ln=0)
        self.cell(qty_width + col_padding, 10, "QTY", border='B', align='L', ln=0)
        self.cell(price_width + col_padding, 10, "PRICE", border='B', align='L', ln=0)
        self.cell(total_width + col_padding, 10, "TOTAL", border='B', align='L')
        self.ln()

        self.set_font('Times', 'B', 10)
        self.set_text_color(33, 46, 78) 
        self.set_draw_color(33, 46, 78) 
        self.set_line_width(1)

        self.cell(description_width + col_padding, 20, data['DESCRIPTION'], border='B', align='L', ln=0)
        self.cell(qty_width + col_padding, 20, str(data['QTY']), border='B', align='L', ln=0)
        price = float(str(data['PRICE']).replace(',', ''))
        self.cell(price_width + col_padding, 20, f"Rs. {price:.2f}", border='B', align='L', ln=0)
        total = price * int(data['QTY'])
        self.cell(total_width + col_padding, 20, f"Rs. {total:.2f}", border='B', align='L')
        self.ln()

        self.ln(5)

        self.set_font('Times', 'B', 10)
        self.set_text_color(234, 209, 105)
        
        self.cell(description_width + col_padding, 10)
        self.cell(qty_width + col_padding, 10, "CGST @9%:", align='L', ln=0)
        self.cell(price_width + col_padding, 10)
        self.set_text_color(33, 46, 78)
        cgst_amount = total * 0.09
        self.cell(total_width + col_padding, 10, f"Rs. {cgst_amount:.2f}", align='L')
        self.ln()

        self.set_text_color(234, 209, 105)  

        self.cell(description_width + col_padding, 10)
        self.cell(qty_width + col_padding, 10, "SGST @9%:", align='L', ln=0)
        self.cell(price_width + col_padding, 10)
        self.set_text_color(33, 46, 78) 
        sgst_amount = total * 0.09
        self.cell(total_width + col_padding, 10, f"Rs. {sgst_amount:.2f}", align='L')
        self.ln()

        self.cell(description_width + col_padding, 10)

        self.set_text_color(234, 209, 105)
        self.cell(qty_width + col_padding, 10, "TOTAL AMOUNT:", align='L', ln=0)
        self.cell(price_width + col_padding, 10)
        self.set_text_color(33, 46, 78)
        total_amount = total + cgst_amount + sgst_amount
        self.cell(total_width + col_padding, 10, f"Rs. {total_amount:.2f}", align='L')
        self.ln()

    def footer(self):
        self.set_left_margin(5)
        self.set_y(-75)
        page_width = self.w
        image_width = page_width * 0.5
        self.image('weboin.png', x=self.l_margin, y=self.get_y(), w=image_width)
        self.set_y(self.get_y() + image_width * 0.5 - 18)
        self.set_font('Times', 'B', 18)
        self.set_text_color(33, 46, 78)
        self.set_x(self.l_margin)
        self.cell(page_width - self.l_margin, 6, 'WEBOIN', 0, 2, 'L')
        self.cell(page_width - self.l_margin, 6, 'TECHNOLOGIES', 0, 2, 'L')
        self.cell(page_width - self.l_margin, 6, 'PRIVATE LIMITED', 0, 2, 'L')
        self.set_font('Times', 'B', 10)
        self.set_text_color(33, 46, 78)
        self.set_x(self.l_margin)
        self.ln(2)
        self.cell(page_width - self.l_margin, 5, '813,     NIZARA      BONANZA,       6TH       FLOOR,', 0, 1, 'L')
        self.cell(page_width - self.l_margin, 5, 'ANNASALAI, CHENNAI - 600002', 0, 1, 'L')
        self.cell(page_width - self.l_margin, 5, 'GST Number: 33AADCW0171E1ZS', 0, 1, 'L')

def generate_invoice(data, output_file):
    try:
        pdf = InvoicePDF()
        pdf.add_page()
        pdf.add_invoice_info(data)
        pdf.add_invoice_details(data)
        pdf.output(output_file)
        print(f"Invoice generated: {output_file}")
    except Exception as e:
        print(f"Error generating invoice for invoice number {data['INVOICE No.']}: {e}")

def clean_data(df):
    df.columns = df.columns.str.strip()
    df['INVOICE No.'] = pd.to_numeric(df['INVOICE No.'], errors='coerce')
    df['PRICE'] = df['PRICE'].astype(str)
    df.fillna({'INVOICE No.': 0, 'PRICE': '0'}, inplace=True)
    df.dropna(subset=['INVOICE No.'], inplace=True)
    return df

def main():
    csv_file_path = "All_Bills.csv"
    output_dir = 'invoice_pdfs'

    if not os.path.exists(csv_file_path):
        print(f"File not found: {csv_file_path}")
        return

    df = pd.read_csv(csv_file_path)
    df = clean_data(df)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for index, row in df.iterrows():
        try:
            invoice_number = int(row['INVOICE No.'])
            output_file = os.path.join(output_dir, f'Invoice_{invoice_number}.pdf')
            generate_invoice(row, output_file)
        except Exception as e:
            print(f"Error processing row {index + 1}: {e}")

if __name__ == "__main__":
    main()
