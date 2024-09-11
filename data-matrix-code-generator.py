import tkinter as tk
from tkinter import messagebox
from qrcodegen import QrCode
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
import io

def generate_code():
    user_input_1 = entry_1.get()
    user_input_2 = entry_2.get()

    if len(user_input_1) != 8 or not user_input_1.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid 8-digit number for the first input.")
        return

    if len(user_input_2) != 4 or not user_input_2.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid 4-digit number for the second input.")
        return
    
    # Generate the unique 8-digit number from the Unix Timestamp
    unix_timestamp = str(int(time.time()))
    unique_8_digit = unix_timestamp[-8:]  # Last 8 digits of Unix timestamp
    
    # Generate the final formatted number
    final_number = f'9347{user_input_1}{unique_8_digit}{user_input_2}'
    
    # Display the generated number in the app
    number_label.config(text=f"PN: {user_input_1}\nSN: {unique_8_digit}")

    # Generate Data Matrix code with qrcodegen
    qr = QrCode.encode_text(final_number, QrCode.Ecc.MEDIUM)

    # Convert the Data Matrix code to a PIL image
    qr_image = qr.to_image(10)  # Create a high-resolution image
    image_io = io.BytesIO()
    qr_image.save(image_io, 'PNG')
    image_io.seek(0)

    # Convert to an image that Tkinter can use
    pil_image = Image.open(image_io)
    data_matrix_image_tk = ImageTk.PhotoImage(pil_image)

    # Display the data matrix in the GUI
    barcode_label.config(image=data_matrix_image_tk)
    barcode_label.image = data_matrix_image_tk
    
    # Generate PDF for printing (optional)
    generate_pdf(pil_image, user_input_1, unique_8_digit)

def generate_pdf(image, pn, sn):
    c = canvas.Canvas("data_matrix_print.pdf", pagesize=letter)
    c.drawString(100, 750, f"PN: {pn}")
    c.drawString(100, 730, f"SN: {sn}")
    c.drawInlineImage(image, 100, 600, width=200, height=200)  # Embed the image in the PDF
    c.showPage()
    c.save()

def print_data_matrix():
    # You can add functionality here to send the generated PDF to a printer.
    messagebox.showinfo("Print", "Data Matrix code ready to be printed (check data_matrix_print.pdf).")

# GUI setup
root = tk.Tk()
root.title("Data Matrix Generator")

# Input for first 8-digit number (PN)
label_1 = tk.Label(root, text="Enter 8-digit number (PN):")
label_1.pack()

entry_1 = tk.Entry(root)
entry_1.pack()

# Input for second 4-digit number
label_2 = tk.Label(root, text="Enter 4-digit number:")
label_2.pack()

entry_2 = tk.Entry(root)
entry_2.pack()

generate_button = tk.Button(root, text="Generate Data Matrix", command=generate_code)
generate_button.pack()

# Label to display the generated Data Matrix
barcode_label = tk.Label(root)
barcode_label.pack()

# Label to display the generated number (PN and SN)
number_label = tk.Label(root, text="Generated PN and SN will appear here.")
number_label.pack()

print_button = tk.Button(root, text="Print Data Matrix", command=print_data_matrix)
print_button.pack()

root.mainloop()
