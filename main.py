import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from steg import encode_text, decode_text
import os

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    TkApp = TkinterDnD.Tk
    dragdrop_available = True
except ImportError:
    TkApp = tk.Tk
    dragdrop_available = False

def to_bin_length(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    return len(pixels) * 3

def select_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.bmp")])
    if filepath:
        load_image(filepath)

def load_image(filepath):
    entry_image.delete(0, tk.END)
    entry_image.insert(0, filepath)
    show_image_preview(filepath)

def show_image_preview(path):
    try:
        img = Image.open(path)
        img.thumbnail((200, 200), Image.LANCZOS)
        preview = ImageTk.PhotoImage(img)
        image_label.config(image=preview, text="")
        image_label.image = preview
    except Exception:
        image_label.config(image='', text="Could not preview image", fg="red")

def save_image():
    return filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])

def encode_gui():
    image_path = entry_image.get()
    message = text_msg.get("1.0", tk.END).strip()
    password = entry_password.get().strip()

    if not image_path or not message:
        messagebox.showerror("Error", "Select an image and enter a message.")
        return

    max_bits = to_bin_length(image_path)
    needed_bits = len(''.join(format(ord(i), '08b') for i in message + "##END##"))

    if needed_bits > max_bits:
        messagebox.showwarning("Too Long!", f"Message too large for selected image!\nMax: {max_bits // 8} bytes\nNeeded: {needed_bits // 8} bytes")
        return

    out_path = save_image()
    if out_path:
        try:
            encode_text(image_path, message, out_path, password if password else None)
            messagebox.showinfo("Success", "Message encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def decode_gui():
    image_path = entry_image.get()
    password = entry_password.get().strip()
    if not image_path:
        messagebox.showerror("Error", "Select an image to decode.")
        return
    try:
        message = decode_text(image_path, password if password else None)
        text_msg.delete("1.0", tk.END)
        text_msg.insert(tk.END, message)
        messagebox.showinfo("Decoded", "Message successfully extracted.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = TkApp()
root.title("🕵️ CyberSteganography")
root.geometry("600x650")
root.minsize(670, 720)
root.configure(bg="#f5f7fa")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))

container = ttk.Frame(root, padding=12)
container.pack(fill="both", expand=True)

frame_path = ttk.Frame(container)
frame_path.pack(fill="x", pady=(0, 8))

ttk.Label(frame_path, text="Image File:").grid(row=0, column=0, sticky="w")
entry_image = ttk.Entry(frame_path, width=50)
entry_image.grid(row=1, column=0, sticky="ew", pady=4, padx=(0, 5))
ttk.Button(frame_path, text="📂 Browse", command=select_image).grid(row=1, column=1)
frame_path.columnconfigure(0, weight=1)

def on_drop(event):
    file_path = event.data.strip("{}")
    if os.path.isfile(file_path):
        load_image(file_path)

if dragdrop_available:
    entry_image.drop_target_register(DND_FILES)
    entry_image.dnd_bind("<<Drop>>", on_drop)

ttk.Label(container, text="Image Preview:").pack(anchor="w", pady=(6, 2))
image_frame = ttk.Frame(container, width=200, height=200)
image_frame.pack(pady=4)
image_frame.pack_propagate(False)

image_label = tk.Label(image_frame, text="No image loaded", bg="#e0e0e0", relief="sunken")
image_label.pack(fill="both", expand=True)

ttk.Label(container, text="Password (optional):").pack(anchor="w", pady=(12, 2))
entry_password = ttk.Entry(container, show="*", width=35)
entry_password.pack(pady=4, anchor="w")

ttk.Label(container, text="Message to Encode / Decoded Message:").pack(anchor="w", pady=(12, 2))
text_frame = ttk.Frame(container)
text_frame.pack(fill="both", expand=True, pady=4)

text_msg = tk.Text(text_frame, height=8, wrap="word", font=("Segoe UI", 10))
text_msg.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_msg.yview)
scrollbar.pack(side="right", fill="y")

text_msg.config(yscrollcommand=scrollbar.set)

button_section = ttk.Frame(container)
button_section.pack(pady=12, fill="x")
ttk.Button(button_section, text="🔐 Encode Message", command=encode_gui).pack(fill="x", pady=4)
ttk.Button(button_section, text="🕵️ Decode Message", command=decode_gui).pack(fill="x")

footer = ttk.Frame(root)
footer.pack(side="bottom", fill="x", pady=8)
ttk.Label(footer, text="CyberSteganography © 2025 | by CyberNilsen", foreground="gray", anchor="center", font=("Segoe UI", 9)).pack()

root.mainloop()
