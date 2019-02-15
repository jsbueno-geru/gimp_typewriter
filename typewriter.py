#!/usr/bin/env python2

import random

from gimpfu import *

import gtk
import gtk.gdk


def paint(color, drawing):
    pdb.gimp_ellipse_select(image, x, y, size, vsize, CHANNEL_OP_REPLACE, True, True, 12)
    pdb.gimp_context_set_foreground(color)
    if drawing:
        pdb.gimp_edit_fill(drw, FILL_FOREGROUND)
    pdb.gimp_displays_flush()


def keychain(window, event):
    global x, y

    val = event.keyval
    name = gtk.gdk.keyval_name(val)

    if name == "Escape":
        pdb.gimp_selection_clear(image)
        gtk.mainquit()

    if name in "Left Right Down Up Escape".split():
        drawing = False
        color = (0, 0, 0)
    else:
        drawing = True
    if name == "Left":
        x -= size // 2
    if name == "Right":
        x += size // 2
    if name == "Down":
        y += size
    if name == "Up":
        y -= size

    cval = (val - 32) & 0x7
    color = bool(cval & 0x4) * 255, bool(cval & 0x2) * 255, bool(cval & 0x1) * 255

    paint(color, drawing)
    if drawing:
        x += size
        if x > image.width:
            y += vsize
            x = 0


def typewriter(par_image, par_drw):
    global image, drw
    global x, y
    global size, vsize
    size, vsize=30, 60
    x = y = 0
    image = par_image
    drw = par_drw

    w = gtk.Window()
    w.show()
    w.connect("key-press-event", keychain)
    gtk.main()


register(
        "typewriter",
        "typewriter",
        """typewriter
        """,
        "Joao S. O. Bueno",
        "Joao S. O. Bueno",
        "2019. GPL applies.",
        "Filters/typewriter",
        "*",
        [(PF_IMAGE, "Image", "Image", None), (PF_DRAWABLE, "Drawable", "Drawable", None), ],
        [],
        typewriter,
        menu="<Image>")

main()
