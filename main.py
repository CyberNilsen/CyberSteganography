import tkinter as tk
from tkinter import filedialog, messagebox
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
        try:
            encode_text(image_path, message, out_path)
            messagebox.showinfo("Success", "Message encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def decode_gui():
    image_path = entry_image.get()
    if not image_path:
        messagebox.showerror("Error", "Select an image to decode.")
        return
    try:
        message = decode_text(image_path)
        text_msg.delete("1.0", tk.END)
        text_msg.insert(tk.END, message)
        if "No hidden message found." in message:
            messagebox.showwarning("Warning", message)
        else:
            messagebox.showinfo("Decoded", "Message successfully extracted.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    entry_image.delete(0, tk.END)
    text_msg.delete("1.0", tk.END)

root = tk.Tk()
root.title("CyberSteganography")
root.geometry("500x450")

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
tk.Button(frame, text="Clear", command=clear_fields, bg="gray", fg="white").pack(pady=5)

root.mainloop()
