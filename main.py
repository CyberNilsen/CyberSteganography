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
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.bmp *.jpg *.jpeg")])
    if filepath:
        load_image(filepath)


def load_image(filepath):
    entry_image.delete(0, tk.END)
    entry_image.insert(0, filepath)
    show_image_preview(filepath)
    update_max_size_label(filepath)
    update_message_length()
    validate_inputs()


def show_image_preview(path):
    try:
        img = Image.open(path)
        img.thumbnail((200, 200), Image.LANCZOS)
        preview = ImageTk.PhotoImage(img)
        image_label.config(image=preview, text="")
        image_label.image = preview
        status_label.config(text=f"Loaded image: {os.path.basename(path)}", foreground="green")
    except Exception:
        image_label.config(image='', text="Could not preview image", fg="red")
        status_label.config(text="Could not preview image", foreground="red")


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
        messagebox.showwarning(
            "Too Long!",
            f"Message too large for selected image!\nMax: {max_bits // 8} bytes\nNeeded: {needed_bits // 8} bytes"
        )
        return

    out_path = save_image()
    if out_path:
        try:
            status_label.config(text="Encoding...")
            root.update_idletasks()
            encode_text(image_path, message, out_path, password if password else None)
            messagebox.showinfo("Success", "Message encoded successfully!")
            status_label.config(text="Encoding completed!", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="Encoding failed.", foreground="red")


def decode_gui():
    image_path = entry_image.get()
    password = entry_password.get().strip()
    if not image_path:
        messagebox.showerror("Error", "Select an image to decode.")
        return
    try:
        status_label.config(text="Decoding...")
        root.update_idletasks()
        message = decode_text(image_path, password if password else None)
        text_msg.delete("1.0", tk.END)
        text_msg.insert(tk.END, message)
        messagebox.showinfo("Decoded", "Message successfully extracted.")
        status_label.config(text="Decoding completed!", foreground="green")
        update_message_length()
        validate_inputs()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Decoding failed.", foreground="red")


def clear_message():
    text_msg.delete("1.0", tk.END)
    update_message_length()
    validate_inputs()


def update_max_size_label(image_path):
    try:
        max_bytes = to_bin_length(image_path) // 8
        max_size_var.set(f"Max message size: {max_bytes} bytes (~{max_bytes} chars)")
    except Exception:
        max_size_var.set("Max message size: N/A")
        current_length_var.set("")


def update_message_length(*args):
    message = text_msg.get("1.0", tk.END).rstrip('\n')
    char_len = len(message)
    byte_len = len(''.join(format(ord(i), '08b') for i in message + "##END##")) // 8
    current_length_var.set(f"Current message length: {char_len} chars, {byte_len} bytes")
    validate_inputs()


def validate_inputs(*args):
    image_path = entry_image.get().strip()
    message = text_msg.get("1.0", tk.END).strip()
    btn_encode.config(state="normal" if image_path and message else "disabled")
    btn_decode.config(state="normal" if image_path else "disabled")
    btn_clear.config(state="normal" if message else "disabled")


def on_drop(event):
    data = event.data
    if data.startswith('{') and data.endswith('}'):
        data = data[1:-1]
    file_path = data.strip()
    if os.path.isfile(file_path):
        load_image(file_path)


def show_about():
    about_text = (
        "CyberSteganography v1.0\n"
        "Developed by CyberNilsen © 2025\n\n"
        "Hide secret messages inside images using steganography.\n"
        "Supports optional password encryption.\n\n"
        "Supported image formats: PNG, BMP, JPG, JPEG.\n\n"
        "Drag & drop image files anywhere to load.\n"
        "Use the buttons to encode or decode messages."
    )
    messagebox.showinfo("About CyberSteganography", about_text)


def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')


root = TkApp()
root.title("🕵️ CyberSteganography")
root.geometry("800x760") 
root.configure(bg="#f5f7fa")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))

container = ttk.Frame(root, padding=12)
container.pack(fill="both", expand=True)

frame_path = ttk.Frame(container)
frame_path.pack(fill="x", pady=(0, 6))

ttk.Label(frame_path, text="Image File:").grid(row=0, column=0, sticky="w")
entry_image = ttk.Entry(frame_path, width=60)
entry_image.grid(row=1, column=0, sticky="ew", pady=4, padx=(0, 5))
ttk.Button(frame_path, text="📂 Browse", command=select_image).grid(row=1, column=1)
frame_path.columnconfigure(0, weight=1)

if dragdrop_available:
    entry_image.drop_target_register(DND_FILES)
    entry_image.dnd_bind("<<Drop>>", on_drop)

if dragdrop_available:
    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", on_drop)

ttk.Label(container, text="Image Preview:").pack(anchor="w", pady=(6, 2))
image_frame = ttk.Frame(container, width=200, height=200)
image_frame.pack(pady=4)
image_frame.pack_propagate(False)

image_label = tk.Label(image_frame, text="No image loaded", bg="#e0e0e0", relief="sunken")
image_label.pack(fill="both", expand=True)

max_size_var = tk.StringVar(value="Max message size: N/A")
max_size_label = ttk.Label(container, textvariable=max_size_var)
max_size_label.pack(anchor="w", pady=(0, 2))

current_length_var = tk.StringVar(value="")
current_length_label = ttk.Label(container, textvariable=current_length_var, foreground="gray")
current_length_label.pack(anchor="w", pady=(0, 8))

ttk.Label(container, text="Password (optional):").pack(anchor="w", pady=(10, 2)) 
entry_password = ttk.Entry(container, show="*", width=35)
entry_password.pack(pady=4, anchor="w")

ttk.Label(container, text="Message to Encode / Decoded Message:").pack(anchor="w", pady=(10, 2)) 
text_frame = ttk.Frame(container)
text_frame.pack(fill="both", expand=True, pady=4)

text_msg = tk.Text(text_frame, height=6, wrap="word", font=("Segoe UI", 10))
text_msg.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_msg.yview)
scrollbar.pack(side="right", fill="y")

text_msg.config(yscrollcommand=scrollbar.set)

button_section = ttk.Frame(container)
button_section.pack(pady=0, fill="x")

btn_encode = ttk.Button(button_section, text="🔐 Encode Message", command=encode_gui)
btn_encode.pack(fill="x", pady=3) 

btn_decode = ttk.Button(button_section, text="🕵️ Decode Message", command=decode_gui)
btn_decode.pack(fill="x")

btn_clear = ttk.Button(button_section, text="Clear Message", command=clear_message)
btn_clear.pack(fill="x", pady=(4, 0))  

status_label = ttk.Label(container, text="", foreground="green", font=("Segoe UI", 9))
status_label.pack(fill="x", pady=(0, 0))

footer = ttk.Frame(container)
footer.pack(fill="x", pady=(0, 0))

ttk.Label(footer, text="CyberSteganography © 2025 | by CyberNilsen", foreground="gray", anchor="center", font=("Segoe UI", 9)).pack()

menubar = tk.Menu(root)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)

text_msg.bind("<<Modified>>", update_message_length)
entry_image.bind("<KeyRelease>", validate_inputs)
entry_password.bind("<KeyRelease>", validate_inputs)

center_window(root)
root.mainloop()
