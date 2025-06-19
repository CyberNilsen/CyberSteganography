# CyberSteganography

CyberSteganography is a Python-based steganography app that allows users to securely hide secret messages inside images. Developed by **CyberNilsen**, the app offers optional password encryption to protect your hidden data. Designed to be user-friendly with drag & drop support and real-time image previews. Currently supports PNG, BMP, JPG, and JPEG formats.

![SteelSeriesGG_IXuld3nXeI](https://github.com/user-attachments/assets/769108c7-422a-47f2-8406-f047147b6c7c)

## 🚀 Features

- 🕵️ **Hide Secret Messages in Images**  
  Embed text messages invisibly within image files using steganography.

- 🔐 **Optional Password Encryption**  
  Protect your hidden messages with a password for extra security.

- 📂 **Drag & Drop Support**  
  Simply drag image files onto the app to load them instantly.

- 🖼️ **Image Preview & Size Info**  
  Preview your loaded image and see max message size limits.

- 💡 **Encode & Decode Messages Easily**  
  Intuitive interface with separate buttons to encode or decode.

## 🛠️ Technologies

- **Python 3**: Core language powering the app.
- **Pillow (PIL)**: For image processing and preview.
- **Tkinter / TkinterDnD2**: Graphical user interface and drag & drop support.
- **Steganography Logic**: Custom encoding and decoding of messages in images.

## 🧪 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/CyberNilsen/CyberSteganography.git
   ```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python main.py
```

## 💡 Usage
Launch the CyberSteganography app.

- Load an image via the browse button or drag & drop.

- Enter your secret message and optional password.

- Click Encode Message to hide the message inside the image.

- To extract a hidden message, load the image and click Decode Message.

- Use the Clear Message button to reset the text area.

📜 License

This project is licensed under the [MIT License](LICENSE).


##⭐ If you find this project useful, please star the repo and share it with your friends!
