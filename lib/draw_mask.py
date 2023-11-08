"""
Draw Mask is a part of pixelort,
Author: Akash Bora (Akascape)
MIT Copyright 2023
"""

import tkinter
import customtkinter
from PIL import ImageTk, Image, ImageDraw
import os
import sys
from CTkToolTip import *

class DrawMask(customtkinter.CTkToplevel):
    
    def __init__(self,
                 master,
                 image_file=None,
                 size=(500,500),
                 load_func=None):
        
        super().__init__(master=master)
        
        self.title("Draw Mask")
        self.resizable(False, False)
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, master.icopath))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.size = size
        self.side_frame = customtkinter.CTkFrame(self, width=100)
        self.side_frame.pack(fill="y", side="left")
        
        self.pen_img = customtkinter.CTkImage(Image.open(master.resource(os.path.join("assets","pen.png"))))
        customtkinter.CTkLabel(self.side_frame, text="Draw").pack()
        
        self.pen_button = customtkinter.CTkButton(self.side_frame, image=self.pen_img, width=1, text="",
                                                  fg_color="transparent", border_width=2, command=self.use_pen)
        self.pen_button.pack(padx=5)

        self.eraser_img = customtkinter.CTkImage(Image.open(master.resource(os.path.join("assets","eraser.png"))))
        customtkinter.CTkLabel(self.side_frame, text="Erase").pack()
        
        self.eraser_button = customtkinter.CTkButton(self.side_frame, image=self.eraser_img, width=1, text="",
                                                    fg_color="transparent", border_width=2, command=self.use_eraser)
        self.eraser_button.pack()
        
        self.pen_width = customtkinter.CTkSlider(self.side_frame, orientation="vertical", from_=10, to=50,
                                                 command=lambda value: self.tip.configure(message=f"Brush size: {int(value)}"))
        self.pen_width.set(30)
        self.pen_width.pack(expand=True, fill="y", pady=10)
        
        self.tip = CTkToolTip(self.pen_width, message="Brush size: 30",
                       bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"],
                       corner_radius=5)
        
        self.save_logo = customtkinter.CTkImage(Image.open(master.resource(os.path.join("assets","save.png"))))
        self.save_button = customtkinter.CTkButton(self.side_frame, image=self.save_logo, width=1, text="",
                                                    fg_color="transparent", border_width=0, command=self.save)
        self.save_button.pack(pady=(0,10))
        
        CTkToolTip(self.save_button, message="save mask as file",
                   bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"],
                   corner_radius=5)
        
        self.export_logo = customtkinter.CTkImage(Image.open(master.resource(os.path.join("assets","export.png"))))
        
        self.export_button = customtkinter.CTkButton(self.side_frame, image=self.export_logo, width=1, text="",
                                                    fg_color="transparent", border_width=0, command=lambda: self.export(load_func))
        self.export_button.pack(pady=(0,10))
        
        CTkToolTip(self.export_button, message="import mask without saving",
                   bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"],
                   corner_radius=5)
        
        if size[0]>=(self.winfo_screenwidth()/2) or size[1]>=(self.winfo_screenheight()/2):
            if size[0]>size[1]:
                self.screen_size = (int(self.winfo_screenwidth()/2), int((self.winfo_screenwidth()/2)*self.size[1]/self.size[0]))
            else:
                self.screen_size = (int(self.winfo_screenheight()/2), int((self.winfo_screenheight()/2)*self.size[1]/self.size[0]))
        else:
            self.screen_size = (size[0],size[1])
            
        self.canvas = tkinter.Canvas(self, bg='white', width=self.screen_size[0], height=self.screen_size[1],
                                     relief=tkinter.FLAT, borderwidth=0, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", side="right")
        
        self.points = []
        self.lines = []
        
        self.bind("<Control-z>", lambda e: self.undo())
        
        self.bg = None
        if image_file:
            img = Image.open(image_file).resize((int(self.screen_size[0]), int(self.screen_size[1])))
            self.image = ImageTk.PhotoImage(img)
            self.bg = self.canvas.create_image(self.screen_size[0]/2, self.screen_size[1]/2, image=self.image)
            
        self.setup()
    
    def on_closing(self):
        self.withdraw()
        
    def export(self, func):
        if func:
            self.all_lines = self.canvas.find_all()
            self.points = []
            for i in self.all_lines:
                self.points.append(self.canvas.coords(i))
            self.mask = Image.new("RGB", (self.screen_size[0], self.screen_size[1]), "black")
            self.draw = ImageDraw.Draw(self.mask)
            for i in self.points:
                self.draw.line(i, "white", self.line_width)
            self.mask = self.mask.resize((self.size[0], self.size[1]))
            func(self.mask)
            del self.mask
            del self.draw
        self.withdraw()
        
    def save(self):
        save_name = "mask.png" 
        count = 0
        while os.path.exists(save_name):
            count +=1
            save_name = "mask" + str(count) + ".png"
            
        save_file = tkinter.filedialog.asksaveasfilename(initialfile=os.path.basename(save_name),
                                                         filetypes=[('Image', ['*.png','*.jpg','*.jpeg','*.bmp','*.webp']),
                                                                   ('All Files', '*.*')])
        
        self.mask = Image.new("RGB", (self.screen_size[0], self.screen_size[1]), "black")
        self.draw = ImageDraw.Draw(self.mask)
        self.all_lines = self.canvas.find_all()
        self.points = []
        for i in self.all_lines:
            self.points.append(self.canvas.coords(i))
        for i in self.points:
            self.draw.line(i, "white", self.line_width)
        if save_file:
            self.mask = self.mask.resize((self.size[0], self.size[1]))
            self.mask.save(save_file)
        del self.mask
        del self.draw
            
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = int(self.pen_width.get())
        self.canvasolor = "#ff5239"
        self.eraser_on = False
        self.active_button = self.pen_button
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', lambda _: self.use_eraser() if not self.eraser_on else self.use_pen())
        self.canvas.bind('<B3-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-3>', self.switch)
        self.activate_button(self.pen_button)
        
    def use_pen(self):
        self.activate_button(self.pen_button)
        
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)
        
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.configure(fg_color="transparent")
        some_button.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        self.active_button = some_button
        self.eraser_on = eraser_mode
        
    def undo(self):
        for i in range(50):
            if self.lines:
                last_line = self.lines.pop()
                self.canvas.delete(last_line)

    def paint(self, event):
        self.line_width = int(self.pen_width.get())
        if self.old_x and self.old_y:
            line = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                           width=self.line_width, fill=self.canvasolor,
                                           capstyle=tkinter.ROUND, smooth=True, splinesteps=36)
            if self.eraser_on:
                items = self.canvas.find_overlapping(self.old_x, self.old_y, event.x, event.y)
                for item in items:
                    if item != self.bg:
                        self.canvas.delete(item)
            
            else:
                self.lines.append(line)

        self.old_x = event.x
        self.old_y = event.y
        
    def reset(self, event):
        self.old_x, self.old_y = None, None
        
    def switch(self, event):
        self.old_x, self.old_y = None, None
        if self.eraser_on:
            self.use_pen()
        else:
            self.use_eraser()
