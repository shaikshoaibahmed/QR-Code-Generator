import qrcode
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from fpdf import FPDF
import os

# ------------------- MAIN WINDOW -------------------
root = Tk()
root.title("Advanced QR Code Generator")
root.state("zoomed")  # Full screen
dark_mode = False

# ------------------- FUNCTIONS -------------------
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#222" if dark_mode else "#f5f5f5"
    fg = "white" if dark_mode else "black"
    root.config(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass

def generate_qr():
    data = entry.get()
    if not data.strip():
        messagebox.showwarning("Input Error", "Please enter some text or URL.")
        return

    try:
        logo_path = "logo.png"  # Your logo image
        logo = Image.open(logo_path)
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(data)
        qr.make()
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Add logo
        logo_size = 60
        logo = logo.resize((logo_size, logo_size))
        pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
        qr_img.paste(logo, pos)

    except FileNotFoundError:
        qr_img = qrcode.make(data)
        qr_img = qr_img.resize((200, 200))

    # Display
    qr_img = qr_img.resize((300, 300))
    img = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=img)
    qr_label.image = img

    save_btn.config(state=NORMAL)
    root.generated_img = qr_img
    root.generated_data = data

def save_qr():
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if path:
        root.generated_img.save(path)
        messagebox.showinfo("Saved", f"QR Code saved to:\n{path}")

        # Export to PDF
        pdf_path = path.replace(".png", ".pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.image(path, x=60, y=40, w=90, h=90)
        pdf.set_font("Arial", size=12)
        pdf.ln(100)
        pdf.cell(200, 10, txt="QR Data: " + root.generated_data, ln=True, align='C')
        pdf.output(pdf_path)
        messagebox.showinfo("PDF Saved", f"QR Code also saved as PDF:\n{pdf_path}")

# ------------------- UI -------------------
root.config(bg="#f5f5f5")

Label(root, text="Advanced QR Code Generator", font=("Arial", 26, "bold"), bg="#f5f5f5").pack(pady=20)

entry = Entry(root, font=("Arial", 16), width=50, justify=CENTER)
entry.pack(pady=10)

Button(root, text="Generate QR", font=("Arial", 14), command=generate_qr, bg="#00796b", fg="white").pack(pady=10)

qr_label = Label(root, bg="#f5f5f5")
qr_label.pack(pady=30)

save_btn = Button(root, text="Save & Export PDF", font=("Arial", 14), command=save_qr, state=DISABLED, bg="#388e3c", fg="white")
save_btn.pack(pady=10)

Button(root, text="🌗 Toggle Theme", command=toggle_theme, font=("Arial", 12), bg="#757575", fg="white").pack(pady=5)

Label(root, text="Copyright © Shoaib Ahmed 2025", font=("Arial", 12), bg="#f5f5f5").pack(side="bottom", pady=20)

root.mainloop()
