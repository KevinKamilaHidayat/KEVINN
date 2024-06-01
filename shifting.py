import tkinter as tk
from tkinter import filedialog, messagebox, Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\hs\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = tk.Tk()

window.geometry("1000x800")
window.configure(bg="#FFFFFF")

canvas = tk.Canvas(
    window,
    bg="#FFFFFF",
    height=800,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    324.0,
    545.0,
    image=entry_image_1
)

entry_1 = tk.Text(
    bd=0,
    bg="#B1B1B1",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=210.0,
    y=526.0,
    width=228.0,
    height=36.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    499.0,
    188.0,
    image=image_image_1
)

def text_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def embed_message(img, message):
    pixels_before = np.array(img)
    hist_before, _ = np.histogram(pixels_before.flatten(), bins=256, range=(0, 256))
    print("Histogram Before Shifting:")
    print(hist_before)

    binary_message = text_to_binary(message) + '00000000' 
    pixels = np.array(img)
    height, width, channels = pixels.shape

    hist, bin_edges = np.histogram(pixels.flatten(), bins=256, range=(0, 256))

   
    P = np.argmax(hist)
    Z = np.where(hist == 0)[0][0] if np.any(hist == 0) else 255

  
    if P < Z:
        pixels[pixels > P] += 1
    else:
        pixels[pixels < P] -= 1

    pixels_after = np.array(img)
    hist_after, _ = np.histogram(pixels_after.flatten(), bins=256, range=(0, 256))
    print("Histogram After Shifting:")
    print(hist_after)

    index = 0
    for y in range(height):
        for x in range(width):
            for c in range(channels):
                if index < len(binary_message):
                    pixel_value = pixels[y, x, c]
                    if pixel_value == P:
                        pixels[y, x, c] = P + int(binary_message[index])
                        index += 1

    embedded_img = Image.fromarray(pixels)

  
    pixels_embedded = np.array(embedded_img)
    hist_embedded, _ = np.histogram(pixels_embedded.flatten(), bins=256, range=(0, 256))
    print("Histogram After Embedding Message:")
    print(hist_embedded)


    plt.plot(hist_before, color='red')
    plt.title('Histogram befire shifting ')
    plt.xlabel('Intensitas Piksel')
    plt.ylabel('Frekuensi')
    plt.show()

    plt.plot(hist_after, color='green')
    plt.title('Histogram after shifting ')
    plt.xlabel('Intensitas Piksel')
    plt.ylabel('Frekuensi')
    plt.show()

    plt.plot(hist_embedded, color='blue')
    plt.title('Histogram After Embedding Message')
    plt.xlabel('Intensitas Piksel')
    plt.ylabel('Frekuensi')
    plt.show()
    

    return embedded_img

def extract_message(img):
    pixels = np.array(img)
    height, width, channels = pixels.shape

    hist, bin_edges = np.histogram(pixels.flatten(), bins=256, range=(0, 256))
    P = np.argmax(hist)

    binary_message = ''
    for y in range(height):
        for x in range(width):
            for c in range(channels):
                if pixels[y, x, c] == P or pixels[y, x, c] == P + 1:
                    binary_message += str(pixels[y, x, c] - P)

 
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte:
            char = chr(int(byte, 2))
            if char == '\x00':
                break
            message += char

    return message

def load_image():
    global img
    file_path = filedialog.askopenfilename()
    img = Image.open(file_path)
    img_array = np.array(img)  
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(499.0, 188.0, image=img_tk)

def embed():
    global img, embedded_img
    message = entry_1.get("1.0", "end-1c").strip()
    if img and message:
        embedded_img = embed_message(img, message)
        embedded_img.show()
    else:
        messagebox.showerror("Error", "Harap pilih gambar dan masukkan pesan.")

def extract():
    global img
    if img:
        message = extract_message(img)
        messagebox.showinfo("Extracted Message", "Extracted message: " + message)

def save_image():
    global embedded_img
    if embedded_img:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            embedded_img.save(file_path)
            print("Image saved to", file_path)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = tk.Button(
    image=button_image_1,
    command=load_image,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_1.place(
    x=52.0,
    y=527.0,
    width=125.99999237060547,
    height=37.0
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )
button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_2 = tk.Button(
    image=button_image_2,
    command=embed,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_2.place(
    x=470.0,
    y=526.0,
    width=163.0,
    height=37.0
)
button_image_hover_2 = PhotoImage(
    file=relative_to_assets("button_hover_3.png"))

def button_2_hover(e):
    button_2.config(
        image=button_image_hover_2
    )
def button_2_leave(e):
    button_2.config(
        image=button_image_2
    )

button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)


button_image_3 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_3 = tk.Button(
    image=button_image_3,
    command=extract,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_3.place(
    x=646.0,
    y=526.0,
    width=163.0,
    height=37.0
)
button_image_hover_3 = PhotoImage(
    file=relative_to_assets("button_hover_4.png"))

def button_3_hover(e):
    button_3.config(
        image=button_image_hover_3
    )
def button_3_leave(e):
    button_3.config(
        image=button_image_3
    )

button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)



button_image_4 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_4 = tk.Button(
    image=button_image_4,
    command=save_image,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_4.place(
    x=822.0,
    y=526.0,
    width=125.99999237060547,
    height=37.0
)
button_image_hover_4 = PhotoImage(
    file=relative_to_assets("button_hover_2.png"))

def button_4_hover(e):
    button_4.config(
        image=button_image_hover_4
    )
def button_4_leave(e):
    button_4.config(
        image=button_image_4
    )

button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

canvas.create_text(
    200.0,
    506.0,
    anchor="nw",
    text="Input secret message:",
    fill="#000000",
    font=("OpenSansRoman Regular", 10 * -1)
)


image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    504.0,
    371.0,
    image=image_image_2
)

window.resizable(False, False)
window.mainloop()
