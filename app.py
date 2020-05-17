# import tkinter as tk
from tkinter import StringVar, Label, Button, Tk, Entry, PhotoImage, W, Canvas, font
import io
import base64
from urllib.request import urlopen, urlcleanup
import numpy
import time
import requests
import clipboard
import json
import os
from PIL import Image
import sys

w = requests.get(
    "https://raw.githubusercontent.com/TMShader/head_to_tellraw/master/version")
# v = open(os.path.join(sys._MEIPASS, "version"), "r")
v = open(os.path.normcase("version"), "r")

web = w.text[:-1]
ver = v.read()

if str(web) > str(ver):
    master = Tk()

    myFont = font.Font(size=16)

    image_url = "https://crafatar.com/avatars/8e437b09425747dba1ef50f5eeef7cfa?size=100&overlay"
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodebytes(image_byt)
    photo = PhotoImage(data=image_b64)

    master.resizable(False, False)
    master.title("Head to 1.16+ Tellraw")
    master.iconphoto(False, PhotoImage(data=image_b64))

    Label(master, font=myFont, text="Update avaible, please update the tool!").grid(
        row=0, column=0)
    Label(master, font=myFont, text="Your version: v" + ver + "\nCurrent version: v" + web).grid(
        row=1, column=0)
    Button(master, font=myFont, text='Ok', command=lambda: sys.exit()).grid(
        row=2, column=1, sticky=W, pady=4)

    master.mainloop()
elif str(web) < str(ver):
    master = Tk()

    myFont = font.Font(size=16)

    image_url = "https://crafatar.com/avatars/8e437b09425747dba1ef50f5eeef7cfa?size=100&overlay"
    image_byt = urlopen(image_url).read()
    image_b64 = base64.encodebytes(image_byt)
    photo = PhotoImage(data=image_b64)

    master.resizable(False, False)
    master.title("Head to 1.16+ Tellraw")
    master.iconphoto(False, PhotoImage(data=image_b64))

    Label(master, font=myFont, text="Are you from the future? ;)").grid(
        row=0, column=0)
    Label(master, font=myFont, text="Your version: v" + ver + "\nCurrent version: v" + web).grid(
        row=1, column=0)
    Button(master, font=myFont, text='Yes ;)', command=lambda: master.destroy()).grid(
        row=2, column=1, sticky=W, pady=4)

    master.mainloop()


v.close()

master = Tk()

myFont = font.Font(size=16)

# -----------------------------------------------------------


def download(uname, message):
    with open('head.png', 'wb') as handle:
        uuid_raw = json.loads(requests.get(
            "https://api.mojang.com/users/profiles/minecraft/" + uname).text)
        uuid = uuid_raw["id"]
        response = requests.get(
            "https://crafatar.com/avatars/" + uuid + "?size=80&overlay")

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
    os.remove("head.png")

# -----------------------------------------------------------------


# master = Tk()

image_url = "https://crafatar.com/avatars/8e437b09425747dba1ef50f5eeef7cfa?size=100&overlay"
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
            uuid = data["id"]
            image_url = "https://crafatar.com/avatars/" + uuid + "?size=100&overlay"
            image_byt = urlopen(image_url).read()
            image_b64 = base64.encodebytes(image_byt)
            photo = PhotoImage(data=image_b64)
            lb = Label(master)
            lb.grid(row=0, column=0)
            lb.image = photo
            lb.configure(image=photo)
            sv.set(data["name"])
            lbl.configure(text="User found!")
            cmb.configure(state="normal")
        else:
            lbl.configure(text="User not found!")
            cmb.configure(state="disabled")
    else:
        cmb.configure(state="disabled")
        lbl.configure(text="Username required!")
    # cv = Canvas(bg='white', width=100, height=100)
    # cv.grid(row=0, column=0, sticky=W, pady=4)
    # img = cv.create_image(0, 0, image=photo, anchor='nw')
    # print(sv.get())


sv = StringVar()
# sv.trace("w", lambda name, index, mode, sv=sv: run(sv, lb))

Label(master, font=myFont, text=" Minecraft Username: ").grid(
    row=0, column=1)

succ = Label(master, font=myFont, text="")
succ.grid(row=2, column=1)

e1 = Entry(master, font=myFont, textvariable=sv)

e1.grid(row=0, column=2)

headBut = Button(master, font=myFont, text='Get Head',
                 command=lambda: run(sv, lb, commBut, succ))
headBut.grid(row=1, column=2, sticky=W, pady=4)

commBut = Button(master, font=myFont, state="disabled", text='Get Command Block',
                 command=lambda: download(sv.get(), succ))
commBut.grid(row=2, column=2, sticky=W, pady=4)


master.mainloop()
