import tkinter as tk
from tkinter import messagebox
import treepoem
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

def generate_code():
    user_input = entry1.get()
    last_digits = entry2.get()

    if len(user_input) != 8 or not user_input.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid 8-digit number.")
        return

    if len(last_digits) != 4 or not last_digits.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid 4-digit number.")
        return

    # Generate the final formatted number
    unix_timestamp = int(time.time())
    unique_8_digit = f'{unix_timestamp % 100000000:08d}'
    final_number = f'9347{user_input}{unique_8_digit}{last_digits}'
    
    # Display the generated number in the app
    number_label.config(text=f"Generated Number: {final_number}")

    # Generate Data Matrix barcode with treepoem
    barcode = treepoem.generate_barcode(
        barcode_type="datamatrix", 
        data=final_number
    )

    # Save the barcode as a PNG file
    barcode_image_pil = barcode.convert("1")  # Convert to black and white image
    barcode_image_pil.save("barcode.png")

    # Convert barcode to a format usable by Tkinter
    barcode_image_tk = ImageTk.PhotoImage(barcode_image_pil)

    # Display barcode in the GUI
    barcode_label.config(image=barcode_image_tk)
    barcode_label.image = barcode_image_tk

    # Display PN and SN
    pn_sn_label.config(text=f"PN: {user_input}\nSN: {unique_8_digit}")
    
    # Generate PDF for printing
    generate_pdf("barcode.png", final_number, user_input, unique_8_digit)

def generate_pdf(barcode_path, number_text, pn, sn):
    c = canvas.Canvas("barcode_print.pdf", pagesize=letter)
    c.drawString(100, 750, f"Generated Number: {number_text}")
    c.drawString(100, 730, f"PN: {pn}")
    c.drawString(100, 710, f"SN: {sn}")
    c.drawImage(barcode_path, 100, 600, width=200, height=200)
    c.showPage()
    c.save()

def print_barcode():
    # You can add functionality here to send the generated PDF to a printer.
    messagebox.showinfo("Print", "Barcode ready to be printed (check barcode_print.pdf).")

# GUI setup
root = tk.Tk()
root.title("Data Matrix Code Generator")

label1 = tk.Label(root, text="Enter 8-digit number:")
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="Enter 4-digit number:")
label2.pack()

entry2 = tk.Entry(root)
entry2.pack()

generate_button = tk.Button(root, text="Generate Barcode", command=generate_code)
generate_button.pack()

# Label to display the generated barcode
barcode_label = tk.Label(root)
barcode_label.pack()

# Label to display the generated number
number_label = tk.Label(root, text="Generated Number will appear here.")
number_label.pack()

# Label to display PN and SN
pn_sn_label = tk.Label(root, text="PN and SN will appear here.")
pn_sn_label.pack()

print_button = tk.Button(root, text="Print Barcode", command=print_barcode)
print_button.pack()

root.mainloop()
