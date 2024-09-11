import tkinter as tk
from tkinter import messagebox
import zint
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Unique number tracking
unique_number_counter = 1

def generate_code():
    global unique_number_counter
    user_input = entry.get()

    if len(user_input) != 8 or not user_input.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid 8-digit number.")
        return
    
    # Generate the final formatted number
    unique_8_digit = f'{unique_number_counter:08d}'
    final_number = f'9347{user_input}{unique_8_digit}1234'  # Last part is a 4-digit placeholder (1234)
    unique_number_counter += 1
    
    # Generate Data Matrix barcode
    barcode = zint.Barcode(zint.Barcode.DATAMATRIX)
    barcode.data = final_number.encode()
    barcode_image = barcode.render()

    # Convert barcode to a PIL image
    barcode_image_pil = Image.fromarray(barcode_image)
    barcode_image_tk = ImageTk.PhotoImage(barcode_image_pil)
    
    # Display barcode in the GUI
    barcode_label.config(image=barcode_image_tk)
    barcode_label.image = barcode_image_tk
    
    # Save the barcode to file and prepare for printing
    barcode_image_pil.save("barcode.png")
    generate_pdf("barcode.png", final_number)

def generate_pdf(barcode_path, number_text):
    c = canvas.Canvas("barcode_print.pdf", pagesize=letter)
    c.drawString(100, 750, f"Generated Number: {number_text}")
    c.drawImage(barcode_path, 100, 600, width=200, height=200)
    c.showPage()
    c.save()

def print_barcode():
    # You can add functionality here to send the generated PDF to a printer.
    messagebox.showinfo("Print", "Barcode ready to be printed (check barcode_print.pdf).")

# GUI setup
root = tk.Tk()
root.title("Barcode Generator")

label = tk.Label(root, text="Enter 8-digit number:")
label.pack()

entry = tk.Entry(root)
entry.pack()

generate_button = tk.Button(root, text="Generate Barcode", command=generate_code)
generate_button.pack()

barcode_label = tk.Label(root)
barcode_label.pack()

print_button = tk.Button(root, text="Print Barcode", command=print_barcode)
print_button.pack()

root.mainloop()
