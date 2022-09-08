import tkinter as tk
from tkinter import ttk
from tkinter import LEFT
from tkinter import filedialog
from tkinter import Toplevel, Label, Scale, Button, HORIZONTAL, RIGHT
from tkinter import Frame, Canvas, CENTER, ROUND
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import pygame as pg
import numpy as np
import cv2


class Main(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # pg.init()
        # pg.mixer.music.load('Still With You.wav')
        # pg.mixer.music.play(-1)
        # pg.mixer.music.set_volume(.1)

        self.filename = ""
        self.original_image = None
        self.original2_image = None
        self.rotated_image = None
        self.is_image_selected = False
        self.is_draw_state = False
        self.is_crop_state = False
        self.is_hist_state = False

        self.flip_frame = None
        self.rotate_frame = None
        self.resize_frame = None
        self.translate_frame = None
        self.color_frame = None
        self.adjust_frame = None
        self.filter_frame = None
        self.MergeSplit_frame = None
        self.segment_frame = None
        self.save_as_type_frame = None

        def center(e):
            w = int(self.winfo_width() / 3.5)  # get root width and scale it ( in pixels )
            s = 'IMAGE EDITOR'.rjust(w // 2)
            self.title(s)

        self.bind("<Configure>", center)  # called when window resized
        # self.title("Image Editor")
        self.iconphoto(False, tk.PhotoImage(file='icon.png'))
        # self.configure(bg="blue")
        load = Image.open('bg.jpg')
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        background_label = tk.Label(self, image=render)
        background_label.image = render
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.editbar1 = EditBar1(master=self)
        self.editbar2 = EditBar2(master=self)
        separator = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        separator2 = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        self.image_viewer = ImageViewer(master=self)

        separator.pack(fill=tk.X, padx=20, pady=5)
        self.editbar1.pack(pady=5)
        separator1.pack(fill=tk.X, padx=240, pady=5)
        self.editbar2.pack(pady=5)
        separator2.pack(fill=tk.X, padx=20, pady=5)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)


class EditBar1(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.new_button = Button(self, text="New", bg='#cce7e8', fg='#000000')
        self.new2_button = Button(self, text="2nd Image", bg='#cce7e8', fg='#000000')
        self.save_button = Button(self, text="Save", bg='#cce7e8', fg='#000000')
        self.save_as_button = Button(self, text="Save As", bg='#cce7e8', fg='#000000')
        self.save_as_type_button = Button(self, text="Save As Types", bg='#cce7e8', fg='#000000')
        self.clear_button = Button(self, text="Clear", bg='#cce7e8', fg='#000000')

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.new2_button.bind("<ButtonRelease>", self.new2_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.save_as_type_button.bind("<ButtonRelease>", self.save_as_type_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        self.new_button.pack(side=LEFT)
        self.new2_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.save_as_button.pack(side=LEFT)
        self.save_as_type_button.pack(side=LEFT)
        self.clear_button.pack()

    def new_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            if self.master.is_draw_state:
                self.master.image_viewer.deactivate_draw()
            if self.master.is_crop_state:
                self.master.image_viewer.deactivate_crop()
            if self.master.is_hist_state:
                self.master.image_viewer.deactivate_hist()

            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)

            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True

    def new2_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new2_button:
            if self.master.is_draw_state:
                self.master.image_viewer.deactivate_draw()
            if self.master.is_crop_state:
                self.master.image_viewer.deactivate_crop()
            if self.master.is_hist_state:
                self.master.image_viewer.deactivate_hist()

            filename = filedialog.askopenfilename()
            image2 = cv2.imread(filename)

            if image2 is not None:
                self.master.filename = filename
                self.master.original2_image = image2.copy()
                self.master.processed2_image = image2.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True

    def save_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)

    def save_as_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                original_file_type = self.master.filename.split('.')[-1]
                filename = filedialog.asksaveasfilename()
                filename = filename + "." + original_file_type

                save_image = self.master.processed_image
                cv2.imwrite(filename, save_image)

                self.master.filename = filename

    def save_as_type_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_type_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.save_as_type_frame = TypeFrame(master=self.master)
                self.master.save_as_type_frame.grab_set()

    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.processed_image = self.master.original_image.copy()
                self.master.image_viewer.show_image()
                self.master.processed2_image = self.master.original2_image.copy()
                self.master.image_viewer.show_image()


class EditBar2(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        self.draw_button = Button(self, text="Draw", bg='#cce7e8', fg='#000000')
        self.crop_button = Button(self, text="Crop", bg='#cce7e8', fg='#000000')
        self.hist_button = Button(self, text="Hist", bg='#cce7e8', fg='#000000')
        self.flip_button = Button(self, text="Flip", bg='#cce7e8', fg='#000000')
        self.rotate_button = Button(self, text="Rotate", bg='#cce7e8', fg='#000000')
        self.resize_button = Button(self, text="Resize", bg='#cce7e8', fg='#000000')
        self.translate_button = Button(self, text="Translate", bg='#cce7e8', fg='#000000')
        self.color_button = Button(self, text="Color", bg='#cce7e8', fg='#000000')
        self.adjust_button = Button(self, text="Adjust", bg='#cce7e8', fg='#000000')
        self.filter_button = Button(self, text="Filter", bg='#cce7e8', fg='#000000')
        self.MergeSplit_button = Button(self, text="Merge/Split", bg='#cce7e8', fg='#000000')
        self.segment_button = Button(self, text="Image Segmentation", bg='#cce7e8', fg='#000000')

        self.draw_button.bind("<ButtonRelease>", self.draw_button_released)
        self.crop_button.bind("<ButtonRelease>", self.crop_button_released)
        self.hist_button.bind("<ButtonRelease>", self.hist_button_released)
        self.flip_button.bind("<ButtonRelease>", self.flip_button_released)
        self.rotate_button.bind("<ButtonRelease>", self.rotate_button_released)
        self.resize_button.bind("<ButtonRelease>", self.resize_button_released)
        self.translate_button.bind("<ButtonRelease>", self.translate_button_released)
        self.color_button.bind("<ButtonRelease>", self.color_button_released)
        self.adjust_button.bind("<ButtonRelease>", self.adjust_button_released)
        self.filter_button.bind("<ButtonRelease>", self.filter_button_released)
        self.MergeSplit_button.bind("<ButtonRelease>", self.MergeSplit_button_released)
        self.segment_button.bind("<ButtonRelease>", self.segment_button_released)

        self.draw_button.pack(side=LEFT)
        self.crop_button.pack(side=LEFT)
        self.hist_button.pack(side=LEFT)
        self.flip_button.pack(side=LEFT)
        self.rotate_button.pack(side=LEFT)
        self.resize_button.pack(side=LEFT)
        self.translate_button.pack(side=LEFT)
        self.color_button.pack(side=LEFT)
        self.adjust_button.pack(side=LEFT)
        self.filter_button.pack(side=LEFT)
        self.MergeSplit_button.pack(side=LEFT)
        self.segment_button.pack(side=LEFT)

    def draw_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.draw_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()
                else:
                    self.master.image_viewer.activate_draw()

    def crop_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()
                else:
                    self.master.image_viewer.activate_crop()

    def flip_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.flip_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.flip_frame = FlipFrame(master=self.master)
                self.master.flip_frame.grab_set()

    def rotate_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.rotate_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.rotate_frame = RotateFrame(master=self.master)
                self.master.rotate_frame.grab_set()

    def resize_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.resize_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.resize_frame = ResizeFrame(master=self.master)
                self.master.resize_frame.grab_set()

    def translate_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.translate_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.translate_frame = TranslateFrame(master=self.master)
                self.master.translate_frame.grab_set()

    def color_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.color_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.color_frame = ColorFrame(master=self.master)
                self.master.color_frame.grab_set()

    def hist_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.hist_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()
                else:
                    self.master.image_viewer.activate_hist()

    def adjust_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.adjust_frame = AdjustFrame(master=self.master)
                self.master.adjust_frame.grab_set()

    def filter_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.filter_frame = FilterFrame(master=self.master)
                self.master.filter_frame.grab_set()

    def MergeSplit_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.MergeSplit_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.MergeSplit_frame = MergeSplitFrame(master=self.master)
                self.master.MergeSplit_frame.grab_set()

    def segment_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.segment_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_hist_state:
                    self.master.image_viewer.deactivate_hist()

                self.master.segment_frame = SegmentFrame(master=self.master)
                self.master.segment_frame.grab_set()


class TypeFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None

        self.bmp_button = Button(master=self, text="Bitmaps Type")
        self.jpeg_button = Button(master=self, text="JPEG Type")
        self.tiff_button = Button(master=self, text="TIFF Type")
        self.png_button = Button(master=self, text="PNG Type")
        self.cancel_button = Button(master=self, text="Cancel")

        self.bmp_button.bind("<ButtonRelease>", self.bmp_button_released)
        self.jpeg_button.bind("<ButtonRelease>", self.jpeg_button_released)
        self.tiff_button.bind("<ButtonRelease>", self.tiff_button_released)
        self.png_button.bind("<ButtonRelease>", self.png_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.bmp_button.pack()
        self.jpeg_button.pack()
        self.tiff_button.pack()
        self.png_button.pack()
        self.cancel_button.pack(side=RIGHT)

    def bmp_button_released(self, event):
        self.bmp()

    def jpeg_button_released(self, event):
        self.jpeg()

    def tiff_button_released(self, event):
        self.tiff()

    def png_button_released(self, event):
        self.png()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def bmp(self):
        type_filename = filedialog.asksaveasfilename()
        type_filename = type_filename + ".bmp"

        save_image = self.master.processed_image
        cv2.imwrite(type_filename, save_image)

        self.master.filename = type_filename

    def jpeg(self):
        type_filename = filedialog.asksaveasfilename()
        type_filename = type_filename + ".jpeg"

        save_image = self.master.processed_image
        cv2.imwrite(type_filename, save_image)

        self.master.filename = type_filename

    def tiff(self):
        type_filename = filedialog.asksaveasfilename()
        type_filename = type_filename + ".tiff"

        save_image = self.master.processed_image
        cv2.imwrite(type_filename, save_image)

        self.master.filename = type_filename

    def png(self):
        type_filename = filedialog.asksaveasfilename()
        type_filename = type_filename + ".png"

        save_image = self.master.processed_image
        cv2.imwrite(type_filename, save_image)

        self.master.filename = type_filename

    def close(self):
        self.destroy()


class RotateFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.rotate_value = 0
        self.previous_rotate_value = 0

        self.original_image = self.master.processed_image
        self.rotated_image = self.master.processed_image

        self.rotate_label = Label(self, text="Rotate")
        self.rotate_scale = Scale(self, from_=0, to_=360, length=250, resolution=0.1, orient=HORIZONTAL)

        self.rotate_button = Button(master=self, text="Rotate")
        self.preview_button = Button(master=self, text="Preview")
        self.cancel_button = Button(master=self, text="Cancel")

        self.rotate_button.bind("<ButtonRelease>", self.rotate_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.rotate_scale.set(0)

        self.rotate_label.pack()
        self.rotate_scale.pack()
        self.rotate_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.preview_button.pack()

    def rotate_button_released(self, event):
        self.master.processed_image = self.rotated_image
        self.close()

    def show_button_released(self, event):
        scale = 1
        rotate = self.rotate_scale.get()
        self.center = (self.original_image.shape[1] / 2, self.original_image.shape[0] / 2)
        M = cv2.getRotationMatrix2D(self.center, rotate, scale)
        self.rotated_image = cv2.warpAffine(self.original_image, M,
                                            (self.original_image.shape[1], self.original_image.shape[0]))
        self.show_image(self.rotated_image)

    def cancel_button_released(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()


class ResizeFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.width_value = 0
        self.previous_width_value = 0
        self.height_value = 0
        self.previous_height_value = 0

        self.original_image = self.master.processed_image
        self.resized_image = self.master.processed_image

        self.width_label = Label(self, text="Width")
        self.width_scale = Scale(self, from_=1, to_=100, length=250, resolution=0.1, orient=HORIZONTAL)
        self.height_label = Label(self, text="Height")
        self.height_scale = Scale(self, from_=1, to_=100, length=250, resolution=0.1, orient=HORIZONTAL)

        self.resize_button = Button(master=self, text="Resize")
        self.preview_button = Button(master=self, text="Preview")
        self.cancel_button = Button(master=self, text="Cancel")

        self.resize_button.bind("<ButtonRelease>", self.resize_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.width_scale.set(100)
        self.height_scale.set(100)

        self.width_label.pack()
        self.width_scale.pack()
        self.height_label.pack()
        self.height_scale.pack()
        self.resize_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.preview_button.pack()

    def resize_button_released(self, event):
        self.master.processed_image = self.resized_image
        self.close()

    def show_button_released(self, event):
        width = self.width_scale.get()
        height = self.height_scale.get()
        self.width = int(self.original_image.shape[1] * width / 100)
        self.height = int(self.original_image.shape[0] * height / 100)
        dim = (self.width, self.height)
        self.resized_image = cv2.resize(self.original_image, dim)
        self.show_image(self.resized_image)

    def cancel_button_released(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()


class TranslateFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.tx_value = 0
        self.previous_tx_value = 0
        self.ty_value = 0
        self.previous_ty_value = 0

        self.original_image = self.master.processed_image
        self.translated_image = self.master.processed_image

        self.tx_label = Label(self, text="Translate x")
        self.tx_scale = Scale(self, from_=-(self.original_image.shape[1] / 2), to_=self.original_image.shape[1] / 2,
                              length=250, resolution=0.1, orient=HORIZONTAL)
        self.ty_label = Label(self, text="Translate y")
        self.ty_scale = Scale(self, from_=-(self.original_image.shape[0] / 2), to_=self.original_image.shape[0] / 2,
                              length=250, resolution=0.1, orient=HORIZONTAL)

        self.translate_button = Button(master=self, text="Translate")
        self.preview_button = Button(master=self, text="Preview")
        self.cancel_button = Button(master=self, text="Cancel")

        self.translate_button.bind("<ButtonRelease>", self.translate_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.tx_scale.set(0)
        self.ty_scale.set(0)

        self.tx_label.pack()
        self.tx_scale.pack()
        self.ty_label.pack()
        self.ty_scale.pack()
        self.translate_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.preview_button.pack()

    def translate_button_released(self, event):
        self.master.processed_image = self.translated_image
        self.close()

    def show_button_released(self, event):
        tx = self.tx_scale.get()
        ty = self.ty_scale.get()
        translationMatrix = np.float32([[1.0, 0.0, tx], [0.0, 1.0, ty]])
        self.translated_image = cv2.warpAffine(self.original_image, translationMatrix,
                                               (self.original_image.shape[1], self.original_image.shape[0]))
        self.show_image(self.translated_image)

    def cancel_button_released(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()


class ColorFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = self.master.processed_image

        self.black_white_button = Button(master=self, text="Black White")
        self.hsv_button = Button(master=self, text="HSV")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.black_white_button.bind("<ButtonRelease>", self.black_white_released)
        self.hsv_button.bind("<ButtonRelease>", self.hsv_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.black_white_button.pack()
        self.hsv_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    def black_white_released(self, event):
        self.black_white()
        self.show_image(self.filtered_image)

    def hsv_button_released(self, event):
        self.hsv()
        self.show_image(self.filtered_image)

    def apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def black_white(self):
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2BGR)

    def hsv(self):
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2HSV)

    def close(self):
        self.destroy()


class FlipFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.flipped_image = self.master.processed_image

        self.flipx_button = Button(master=self, text="FlipX")
        self.flipy_button = Button(master=self, text="FlipY")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.flipx_button.bind("<ButtonRelease>", self.flipx_button_released)
        self.flipy_button.bind("<ButtonRelease>", self.flipy_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.flipx_button.pack()
        self.flipy_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    def flipx_button_released(self, event):
        self.flipx()
        self.show_image(self.flipped_image)

    def flipy_button_released(self, event):
        self.flipy()
        self.show_image(self.flipped_image)

    def apply_button_released(self, event):
        self.master.processed_image = self.flipped_image
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def flipx(self):
        self.flipVertical = cv2.flip(self.master.processed_image, 0)
        self.flipped_image = self.flipVertical

    def flipy(self):
        self.flipHorizontal = cv2.flip(self.master.processed_image, 1)
        self.flipped_image = self.flipHorizontal

    def close(self):
        self.destroy()


class AdjustFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.brightness_value = 0
        self.previous_brightness_value = 0

        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image

        self.brightness_label = Label(self, text="Brightness")
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1,
                                      orient=HORIZONTAL)
        self.r_label = Label(self, text="R")
        self.r_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.g_label = Label(self, text="G")
        self.g_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.b_label = Label(self, text="B")
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.b_label = Label(self, text="B")
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.apply_button = Button(self, text="Apply")
        self.preview_button = Button(self, text="Preview")
        self.cancel_button = Button(self, text="Cancel")

        self.brightness_scale.set(1)

        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_release)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.r_label.pack()
        self.r_scale.pack()
        self.g_label.pack()
        self.g_scale.pack()
        self.b_label.pack()
        self.b_scale.pack()
        self.cancel_button.pack(side=RIGHT)
        self.preview_button.pack(side=RIGHT)
        self.apply_button.pack()

    def apply_button_released(self, event):
        self.master.processed_image = self.processing_image
        self.close()

    def show_button_release(self, event):
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())
        b, g, r = cv2.split(self.processing_image)

        for b_value in b:
            cv2.add(b_value, self.b_scale.get(), b_value)
        for g_value in g:
            cv2.add(g_value, self.g_scale.get(), g_value)
        for r_value in r:
            cv2.add(r_value, self.r_scale.get(), r_value)

        self.processing_image = cv2.merge((b, g, r))
        self.show_image(self.processing_image)

    def cancel_button_released(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()


class FilterFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None

        self.negative_button = Button(master=self, text="Negative")
        self.sepia_button = Button(master=self, text="Sepia")
        self.emboss_button = Button(master=self, text="Emboss")
        self.gaussian_blur_button = Button(master=self, text="Gaussian Blur")
        self.median_blur_button = Button(master=self, text="Median Blur")
        self.bilateral_button = Button(master=self, text="Bilateral Blur")
        self.average_button = Button(master=self, text="Average Blur")
        self.boxFilter_button = Button(master=self, text="Box Filter Blur")
        self.sharpen1_button = Button(master=self, text="Sharpen 1")
        self.sharpen2_button = Button(master=self, text="Sharpen 2")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.negative_button.bind("<ButtonRelease>", self.negative_button_released)
        self.sepia_button.bind("<ButtonRelease>", self.sepia_button_released)
        self.emboss_button.bind("<ButtonRelease>", self.emboss_button_released)
        self.gaussian_blur_button.bind("<ButtonRelease>", self.gaussian_blur_button_released)
        self.median_blur_button.bind("<ButtonRelease>", self.median_blur_button_released)
        self.bilateral_button.bind("<ButtonRelease>", self.bilateral_button_released)
        self.average_button.bind("<ButtonRelease>", self.average_button_released)
        self.boxFilter_button.bind("<ButtonRelease>", self.boxFilter_button_released)
        self.sharpen1_button.bind("<ButtonRelease>", self.sharpen1_button_released)
        self.sharpen2_button.bind("<ButtonRelease>", self.sharpen2_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.negative_button.pack()
        self.sepia_button.pack()
        self.emboss_button.pack()
        self.gaussian_blur_button.pack()
        self.median_blur_button.pack()
        self.bilateral_button.pack()
        self.average_button.pack()
        self.boxFilter_button.pack()
        self.sharpen1_button.pack()
        self.sharpen2_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    def sharpen1_button_released(self, event):
        self.sharpen1_blur()
        self.show_image()

    def sharpen2_button_released(self, event):
        self.sharpen2_blur()
        self.show_image()

    def bilateral_button_released(self, event):
        self.bilateral_blur()
        self.show_image()

    def average_button_released(self, event):
        self.average_blur()
        self.show_image()

    def boxFilter_button_released(self, event):
        self.boxFilter_blur()
        self.show_image()

    def sepia_button_released(self, event):
        self.sepia()
        self.show_image()

    def emboss_button_released(self, event):
        self.emboss()
        self.show_image()

    def negative_button_released(self, event):
        self.negative()
        self.show_image()

    def gaussian_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def median_blur_button_released(self, event):
        self.median_blur()
        self.show_image()

    def apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def show_image(self):
        self.master.image_viewer.show_image(img=self.filtered_image)

    def negative(self):
        self.filtered_image = cv2.bitwise_not(self.original_image)

    def sepia(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def emboss(self):
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def gaussian_blur(self):
        self.filtered_image = cv2.GaussianBlur(self.original_image, (5, 5), 3)

    def median_blur(self):
        self.filtered_image = cv2.medianBlur(self.original_image, 5)

    def bilateral_blur(self):
        self.filtered_image = cv2.bilateralFilter(self.original_image, 9, 75, 75)

    def average_blur(self):
        self.filtered_image = cv2.blur(self.original_image, (5, 5))

    def boxFilter_blur(self):
        self.filtered_image = cv2.boxFilter(self.original_image, 0, (7, 7))

    def sharpen1_blur(self):
        kernel_sharpening = np.array(
            [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, 25, -1, -1], [-1, -1, -1, -1, -1],
             [-1, -1, -1, -1, -1]])
        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel_sharpening)

    def sharpen2_blur(self):
        kernel_sharpening = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel_sharpening)

    def close(self):
        self.destroy()


class MergeSplitFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.original2_image = self.master.processed2_image
        self.edited_image = None

        self.mergeh_button = Button(master=self, text="Merge Horizontal")
        self.mergev_button = Button(master=self, text="Merge Vertical")
        self.splith_button = Button(master=self, text="Split Horizontal")
        self.splitv_button = Button(master=self, text="Split Vertical")
        self.splitImage_button = Button(master=self, text="Split")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.mergeh_button.bind("<ButtonRelease>", self.mergeh_button_released)
        self.mergev_button.bind("<ButtonRelease>", self.mergev_button_released)
        self.splith_button.bind("<ButtonRelease>", self.splith_button_released)
        self.splitv_button.bind("<ButtonRelease>", self.splitv_button_released)
        self.splitImage_button.bind("<ButtonRelease>", self.splitImage_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.mergeh_button.pack()
        self.mergev_button.pack()
        self.splith_button.pack()
        self.splitv_button.pack()
        self.splitImage_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    def mergeh_button_released(self, event):
        self.mergeh()
        self.show_image(self.edited_image)

    def mergev_button_released(self, event):
        self.mergev()
        self.show_image(self.edited_image)

    def splith_button_released(self, event):
        self.splith()
        self.show_image(self.edited_image)

    def splitv_button_released(self, event):
        self.splitv()
        self.show_image(self.edited_image)

    def splitImage_button_released(self, event):
        self.splitImage()
        self.show_image(self.edited_image)

    def apply_button_released(self, event):
        self.master.processed_image = self.edited_image
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def mergeh(self, interpolation=cv2.INTER_CUBIC):
        img1 = self.original_image
        img2 = self.original2_image
        img_list = [img1, img2]
        h_min = min(img.shape[0]
                    for img in img_list)

        # image resizing
        im_list_hresize = [
            cv2.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min), interpolation=interpolation) for img
            in
            img_list]

        self.edited_image = cv2.hconcat(im_list_hresize)

    def mergev(self, interpolation=cv2.INTER_CUBIC):
        img1 = self.original_image
        img2 = self.original2_image
        img_list = [img1, img2]

        w_min = min(img.shape[1]
                    for img in img_list)

        # resizing images
        im_list_vresize = [
            cv2.resize(img, (w_min, int(img.shape[0] * w_min / img.shape[1])), interpolation=interpolation) for img in
            img_list]

        self.edited_image = cv2.vconcat(im_list_vresize)

    def splith(self):
        width = self.original_image.shape[1]
        height = self.original_image.shape[0]

        x = slice(0, width, 1)

        y1 = slice(0, int(height / 2), 1)
        y2 = slice(int(height / 2), height, 1)

        # ..........................................................
        cv2.imshow("split horizontal 1", self.original_image[y1, x])
        cv2.moveWindow("split horizontal 1", 800, 0)

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_image = self.original_image[y1, x]
        cv2.imwrite(filename, save_image)
        self.master.filename = filename

        # ..........................................................
        cv2.imshow("split horizontal 2", self.original_image[y2, x])
        cv2.moveWindow("split horizontal 2", 800, int(height / 2), )

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type

        save_image = self.original_image[y2, x]
        cv2.imwrite(filename, save_image)

        self.master.filename = filename

    def splitv(self):
        width = self.original_image.shape[1]
        height = self.original_image.shape[0]

        y = slice(0, height, 1)

        x1 = slice(0, int(width / 2), 1)
        x2 = slice(int(width / 2), width, 1)

        # ........................................................
        cv2.imshow("split vertical 1", self.original_image[y, x1])
        cv2.moveWindow("split vertical 1", 800, 0)

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_image = self.original_image[y, x1]
        cv2.imwrite(filename, save_image)
        self.master.filename = filename

        # ........................................................
        cv2.imshow("split vertical 2", self.original_image[y, x2])
        cv2.moveWindow("split vertical 2", int(width / 2)+800, 0)

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_image = self.original_image[y, x2]
        cv2.imwrite(filename, save_image)
        self.master.filename = filename

    def splitImage(self):
        width = self.original_image.shape[1]
        height = self.original_image.shape[0]

        x = slice(0, width, 1)
        y = slice(0, height, 1)

        x1 = slice(0, int(width / 2), 1)
        y1 = slice(0, int(height / 2), 1)
        x2 = slice(int(width / 2), width, 1)
        y2 = slice(int(height / 2), height, 1)

        # .........................................................
        cv2.imshow("Split lower left", self.original_image[y2, x1])
        cv2.moveWindow("Split lower left", 800, int(height / 2))

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_image = self.original_image[y2, x1]
        cv2.imwrite(filename, save_image)
        self.master.filename = filename

        # .........................................................
        cv2.imshow("split lower right", self.original_image[y2, x2])
        cv2.moveWindow("split lower right", int(width / 2)+800, int(height / 2))

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_image = self.original_image[y2, x2]
        cv2.imwrite(filename, save_image)
        self.master.filename = filename

        # .........................................................
        cv2.imshow("split upper left", self.original_image[y1, x1])
        cv2.moveWindow("split upper left", 800, 0)

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_image = self.original_image[y1, x1]
        cv2.imwrite(filename, save_image)
        self.master.filename = filename

        # .........................................................
        cv2.imshow("split upper right", self.original_image[y1, x2])
        cv2.moveWindow("split upper right", int(width / 2)+800, 0)

        original_file_type = self.master.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + original_file_type
        save_image = self.original_image[y1, x2]
        cv2.imwrite(filename, save_image)
        self.master.filename = filename

    def close(self):
        self.destroy()


class SegmentFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None

        self.canny_button = Button(master=self, text="Canny")
        self.laplacian_button = Button(master=self, text="Laplacian")
        self.sobel_button = Button(master=self, text="Sobel")
        self.prewitt_button = Button(master=self, text="Prewitt")
        self.threshold_button = Button(master=self, text="Thresholding")
        self.cluster_button = Button(master=self, text="Clustering")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.canny_button.bind("<ButtonRelease>", self.canny_button_released)
        self.laplacian_button.bind("<ButtonRelease>", self.laplacian_button_released)
        self.sobel_button.bind("<ButtonRelease>", self.sobel_button_released)
        self.prewitt_button.bind("<ButtonRelease>", self.prewitt_button_released)
        self.threshold_button.bind("<ButtonRelease>", self.threshold_button_released)
        self.cluster_button.bind("<ButtonRelease>", self.cluster_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.canny_button.pack()
        self.laplacian_button.pack()
        self.sobel_button.pack()
        self.prewitt_button.pack()
        self.threshold_button.pack()
        self.cluster_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    def canny_button_released(self, event):
        self.canny()
        self.show_image()

    def laplacian_button_released(self, event):
        self.laplacian()
        self.show_image()

    def sobel_button_released(self, event):
        self.sobel()
        self.show_image()

    def prewitt_button_released(self, event):
        self.prewitt()
        self.show_image()

    def threshold_button_released(self, event):
        self.threshold()
        self.show_image()

    def cluster_button_released(self, event):
        self.cluster()
        self.show_image()

    def apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def show_image(self):
        self.master.image_viewer.show_image(img=self.filtered_image)

    def canny(self):
        self.gray_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGRA2GRAY)
        self.filtered_image = cv2.Canny(self.gray_img, 30, 200)

    def laplacian(self):
        self.gray_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGRA2GRAY)
        lap = cv2.Laplacian(self.gray_img, cv2.CV_64F)
        self.filtered_image = np.uint8(np.absolute(lap))

    def sobel(self):
        self.gray_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGRA2GRAY)
        sobelX = cv2.Sobel(self.gray_img, cv2.CV_64F, 1, 0)
        sobelY = cv2.Sobel(self.gray_img, cv2.CV_64F, 0, 1)

        sobelX = np.uint8(np.absolute(sobelX))
        sobelY = np.uint8(np.absolute(sobelY))

        self.filtered_image = cv2.bitwise_or(sobelX, sobelY)

    def prewitt(self):
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        img_prewittx = cv2.filter2D(self.original_image, -1, kernelx)
        img_prewitty = cv2.filter2D(self.original_image, -1, kernely)
        self.filtered_image = cv2.bitwise_or(img_prewittx, img_prewitty)

    def threshold(self):
        self.gray_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGRA2GRAY)
        retval, threshold = cv2.threshold(self.gray_img, 62, 255, cv2.THRESH_BINARY)
        self.filtered_image = threshold

    def cluster(self):
        img = self.original_image
        Z = img.reshape((-1, 3))

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 8
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img.shape))

        self.filtered_image = res2

    def close(self):
        self.destroy()


class ImageViewer(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg='#6ac7e6', width=800, height=500)

        self.shown_image = None
        self.x = 0
        self.y = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.draw_ids = list()
        self.rectangle_id = 0
        self.ratio = 0

        # self.canvas = Canvas(self, bg='#6ac7e6', width=600, height=400)
        # self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas = Canvas(self, bg='#6ac7e6', width=800, height=500)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas2 = Canvas(self, bg='#6ac7e6', width=200, height=200)
        self.canvas2.place(relx=0.87, rely=0.8, anchor=CENTER)
        self.canvas3 = Canvas(self, bg='#6ac7e6', width=200, height=200)
        self.canvas3.place(relx=0.13, rely=0.8, anchor=CENTER)

    def show_image(self, img=None):
        self.clear_canvas()

        if img is None:
            image3 = self.master.original_image.copy()
            image = self.master.processed_image.copy()
            image2 = self.master.processed2_image.copy()
        else:
            image3 = self.master.original_image.copy()
            image = img
            image2 = self.master.processed2_image.copy()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
        height2, width2, channels2 = image2.shape
        ratio2 = height2 / width2

        image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2RGB)
        height3, width3, channels3 = image3.shape
        ratio3 = height3 / width3

        new_width = width
        new_height = height
        new_width2 = width2
        new_height2 = height2
        new_width3 = width3
        new_height3 = height3

        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))

        if height2 > 200 or width2 > 200:
            if ratio2 < 1:
                new_width2 = 200
                new_height2 = int(new_width2 * ratio2)
            else:
                new_height2 = 200
                new_width2 = int(new_height2 * (width2 / height2))

        if height3 > 200 or width3 > 200:
            if ratio3 < 1:
                new_width3 = 200
                new_height3 = int(new_width3 * ratio3)
            else:
                new_height3 = 200
                new_width3 = int(new_height3 * (width3 / height3))

        self.shown_image = cv2.resize(image, (new_width, new_height))
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))
        self.shown2_image = cv2.resize(image2, (new_width2, new_height2))
        self.shown2_image = ImageTk.PhotoImage(Image.fromarray(self.shown2_image))
        self.shown3_image = cv2.resize(image3, (new_width3, new_height3))
        self.shown3_image = ImageTk.PhotoImage(Image.fromarray(self.shown3_image))

        self.ratio = height / new_height
        self.ratio2 = height2 / new_height2
        self.ratio3 = height3 / new_height3

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)
        self.canvas2.config(width=new_width2, height=new_height2)
        self.canvas2.create_image(new_width2 / 2, new_height2 / 2, anchor=CENTER, image=self.shown2_image)
        self.canvas3.config(width=new_width3, height=new_height3)
        self.canvas3.create_image(new_width3 / 2, new_height3 / 2, anchor=CENTER, image=self.shown3_image)

    def activate_draw(self):
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.master.is_draw_state = True

    def activate_crop(self):
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

        self.master.is_crop_state = True

    def deactivate_draw(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")

        self.master.is_draw_state = False

    def deactivate_crop(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")

        self.master.is_crop_state = False

    def start_draw(self, event):
        self.x = event.x
        self.y = event.y

    def draw(self, event):
        self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,
                                                     fill="black", capstyle=ROUND, smooth=True))

        cv2.line(self.master.processed_image, (int(self.x * self.ratio), int(self.y * self.ratio)),
                 (int(event.x * self.ratio), int(event.y * self.ratio)),
                 (0, 0, 255), thickness=int(self.ratio * 2),
                 lineType=8)

        self.x = event.x
        self.y = event.y

    def start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        self.crop_end_x = event.x
        self.crop_end_y = event.y

        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y,
                                                         self.crop_end_x, self.crop_end_y, width=1)

    def end_crop(self, event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)

        self.master.processed_image = self.master.processed_image[y, x]

        self.show_image()

    def activate_hist(self):
        R, G, B = cv2.split(self.master.processed_image)
        output1_R = cv2.equalizeHist(R)
        output1_G = cv2.equalizeHist(G)
        output1_B = cv2.equalizeHist(B)
        equ = cv2.merge((output1_R, output1_G, output1_B))
        plt.figure(num='Image Histogram')
        hist = cv2.calcHist(equ, [0], None, [256], [0, 256])
        plt.plot(hist)
        plt.hist(self.master.processed_image.flatten(), 256, [0, 256], )
        # plt.title('Image Histogram')
        plt.show()

    def deactivate_hist(self):
        pass

    def clear_canvas(self):
        self.canvas.delete("all")

    def clear_draw(self):
        self.canvas.delete(self.draw_ids)


root = Main()
root.mainloop()
