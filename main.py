import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from steg import encode_text, decode_text

def select_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.bmp")])
    if filepath:
        entry_image.delete(0, tk.END)
        entry_image.insert(0, filepath)

def save_image():
    return filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])

def encode_gui():
    image_path = entry_image.get()
    message = text_msg.get("1.0", tk.END).strip()
    if not image_path or not message:
        messagebox.showerror("Error", "Select an image and enter a message.")
        return
    out_path = save_image()
    if out_path:
        # Ask for optional password
        password = simpledialog.askstring("Password (optional)", "Enter password for encryption (leave blank for none):", show='*')
        try:
            encode_text(image_path, message, out_path, password=password if password else None)
            messagebox.showinfo("Success", "Message encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def decode_gui():
    image_path = entry_image.get()
    if not image_path:
        messagebox.showerror("Error", "Select an image to decode.")
        return
    # Ask for password (optional)
    password = simpledialog.askstring("Password (if encrypted)", "Enter password to decrypt (leave blank if none):", show='*')
    try:
        message = decode_text(image_path, password=password if password else None)
        text_msg.delete("1.0", tk.END)
        text_msg.insert(tk.END, message)
        messagebox.showinfo("Decoded", "Message successfully extracted.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("CyberSteganography")
root.geometry("500x400")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Image Path:").pack(anchor="w")
entry_image = tk.Entry(frame, width=50)
entry_image.pack(pady=5)
tk.Button(frame, text="Browse", command=select_image).pack()

tk.Label(frame, text="Message:").pack(anchor="w", pady=(10, 0))
text_msg = tk.Text(frame, height=8)
text_msg.pack()

tk.Button(frame, text="Encode Message", command=encode_gui, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(frame, text="Decode Message", command=decode_gui, bg="#2196F3", fg="white").pack(pady=5)

root.mainloop()
