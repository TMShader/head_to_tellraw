# import tkinter as tk
from tkinter import StringVar, Label, Button, Tk, Entry, PhotoImage, W, Canvas
import io
import base64
from urllib.request import urlopen
import numpy
import time
import requests
import clipboard
import json
from PIL import Image

# -----------------------------------------------------------


def download(uname, message):
    with open('head.png', 'wb') as handle:
        response = requests.get(
            "https://minotar.net/avatar/" + uname + "/80", stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    head = Image.open('head.png')
    head = head.load()

    command = '/give @p minecraft:command_block{display:{Name:"{\\"text\\":\\"' + uname + \
        '\\",\\"italic\\":false}]"}, BlockEntityTag: {CustomName: "{\\"text\\": \\"' + \
        uname + '\\"}", Command: "tellraw @a [\\" \\"'

    generate(head, command, message)


def generate(image, prefix, message):
    full = prefix
    for y in range(0, 8):
        for x in range(0, 8):
            color = '#%02x%02x%02x' % image[x * 10, y * 10]
            if x == 7 and y != 7:
                full = full + \
                    ',{\\"text\\":\\"\\\\u2588\\\\n\\",\\"color\\":\\"' + color + '\\"}'
            else:
                full = full + \
                    ',{\\"text\\":\\"\\\\u2588\\",\\"color\\":\\"' + color + '\\"}'
            # print('#%02x%02x%02x' % image[x * 10, y * 10])
        # full = full + ',{\\"text\\":\\" \\n \\"}'

    full = full + ']"}}'

    clipboard.copy(full)
    message.configure(text="Copied to clipboard!")

# -----------------------------------------------------------------


master = Tk()

image_url = "https://minotar.net/avatar/TMShader/100"
image_byt = urlopen(image_url).read()
image_b64 = base64.encodebytes(image_byt)
photo = PhotoImage(data=image_b64)

master.resizable(False, False)
master.title("Head to 1.16+ Tellraw")
master.iconphoto(False, PhotoImage(data=image_b64))

lb = Label(master)
lb.grid(row=0, column=0)
lb.image = photo
lb.configure(image=photo)
# cv = Canvas(bg='white', width=100, height=100)
# cv.grid(row=0, column=0, sticky=W, pady=4)
# img = cv.create_image(0, 0, image=photo, anchor='nw')


def run(sv, img, cmb, lbl):
    result = requests.get(
        "https://api.mojang.com/users/profiles/minecraft/" + sv.get())
    if sv.get() != "":
        if result.text:
            data = json.loads(result.text)
            image_url = "https://minotar.net/avatar/" + sv.get() + "/100"
            image_byt = urlopen(image_url).read()
            image_b64 = base64.encodebytes(image_byt)
            photo = PhotoImage(data=image_b64)
            lb = Label(master)
            lb.grid(row=0, column=0)
            lb.image = photo
            lb.configure(image=photo)
            sv.set(data["name"])
            lbl.configure(text="User found! Name: " + data["name"])
            cmb.configure(state="normal")
        else:
            lbl.configure(text="User not found!")
            cmb.configure(state="disabled")
    else:
        cmb.configure(state="disabled")
        lbl.configure(text="You didn't enter a username!")
    # cv = Canvas(bg='white', width=100, height=100)
    # cv.grid(row=0, column=0, sticky=W, pady=4)
    # img = cv.create_image(0, 0, image=photo, anchor='nw')
    # print(sv.get())


sv = StringVar()
# sv.trace("w", lambda name, index, mode, sv=sv: run(sv, lb))

Label(master, text="Minecraft Username (Case Insensitive)").grid(row=0, column=1)

succ = Label(master, text="")
succ.grid(row=2, column=1)

e1 = Entry(master, textvariable=sv)

e1.grid(row=0, column=2)

headBut = Button(master, text='Get Head',
                 command=lambda: run(sv, lb, commBut, succ))
headBut.grid(row=1, column=2, sticky=W, pady=4)

commBut = Button(master, state="disabled", text='Get Command Block',
                 command=lambda: download(sv.get(), succ))
commBut.grid(row=2, column=2, sticky=W, pady=4)


master.mainloop()
