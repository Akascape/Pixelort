"""
PIXELORT by Akascape
A pixel sorting application

Author: Akash Bora
License: MIT Copyright 2023
"""

import tkinter
import customtkinter
from tkdial import Dial
import os
import sys
import webbrowser
from PIL import Image, ImageTk, UnidentifiedImageError
from pixelsort import pixelsort
from tkinterdnd2 import TkinterDnD, DND_ALL
from CTkMessagebox import CTkMessagebox
from CTkToolTip import *
from CTkMenuBar import *
import threading
import requests
import random

from lib.draw_mask import DrawMask
from lib.spinbox import *

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme(random.choice(["dark-blue","blue","green"]))

class CTk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class App(CTk):

    HEIGHT = 530
    WIDTH = 950
    CURRENT_VERSION = 0.1
    
    def __init__(self):
        super().__init__()
        self.title("Pixelort")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.menubar = CTkMenuBar(self)
        self.DIRPATH = os.getcwd()
        self.icopath = ImageTk.PhotoImage(file=self.resource(os.path.join("assets","logo.png")))
        self.wm_iconbitmap()
        self.iconphoto(False, self.icopath)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<space>", lambda e: self.start())
        self.bind("<Escape>", lambda e: self.turn_of())
        # MENUBAR
        self.button_file = self.menubar.add_cascade("File")
        self.dropdown1 = CustomDropdownMenu(widget=self.button_file, width=100, corner_radius=5)
        self.dropdown1.add_option(option="Import", command=self.open_image)
        self.dropdown1.add_separator()
        self.submenu = self.dropdown1.add_submenu("Export", corner_radius=5)
        self.submenu.add_option(option="PNG", command=lambda: self.export("png"))
        self.submenu.add_option(option="JPG", command=lambda: self.export("jpg"))
        self.button_edit = self.menubar.add_cascade("Mask")
        self.dropdown2 = CustomDropdownMenu(widget=self.button_edit, width=100, corner_radius=5)
        self.dropdown2.add_option(option="Draw Mask", command=self.draw_mask)
        self.dropdown2.add_separator()
        self.dropdown2.add_option(option="Import Mask", command=self.add_mask)
        self.dropdown2.add_separator()
        self.dropdown2.add_option(option="Remove Mask", command=self.remove_mask)
        self.button_settings = self.menubar.add_cascade("Options")
        self.dropdown3 = CustomDropdownMenu(widget=self.button_settings, width=100, corner_radius=5)
        self.dropdown3.add_option(option="Toggle Theme", command=self.change_theme)
        self.dropdown3.add_option(option="Reset Settings", command=self.default_settings)
        self.button_about = self.menubar.add_cascade("Help")
        self.dropdown4 = CustomDropdownMenu(widget=self.button_about, width=100, corner_radius=5)
        self.dropdown4.add_option(option="About", command=self.about)
        self.dropdown4.add_separator()
        self.dropdown4.add_option(option="Check for Updates", command=self.check_for_update)
        self.dropdown4.add_separator()
        self.dropdown4.add_option(option="Documentation", command=self.open_docs)
        self.bind("<FocusOut>", lambda e: self.change_menubarcolor())
        self.bind("<FocusIn>", lambda e: self.change_menubarcolor_dark())
        
        # DEFAULTS
        self.image = ""
        self.previous = ""
        self.zoom = 1
        self.file = None
        self.img_r = None
        self.sort_func = "lightness"
        self.interval_mode = "random"
        self.sorted_image = None
        self.mask = None
        self.new = True
        self.running = False
        
        # WIDGETS
        self.image_frame = customtkinter.CTkLabel(self, corner_radius=20, width=300, text="+ \nDrag & Drop your Image", font=("",14),
                                                  fg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"])
        self.image_frame.pack(padx=(0,10), pady=10, fill="both", side="right")
        
        self.image_frame.drop_target_register(DND_ALL)
        self.image_frame.dnd_bind("<<Drop>>", self.get_path)
        
        self.image_frame.bind("<Configure>", self.resize_event)
        self.image_frame.bind("<MouseWheel>", lambda e: self.do_zoom(e.delta))
        self.image_frame.bind("<Button-4>", lambda e: self.do_zoom(120))
        self.image_frame.bind("<Button-5>", lambda e: self.do_zoom(-120))
        self.image_frame.bind("<Double-1>", lambda e: self.start())
        
        self.xy_frame = customtkinter.CTkScrollableFrame(self, corner_radius=20)
        self.xy_frame.pack(padx=10, pady=10, expand=True, fill="both", side="left")
        self.xy_frame._parent_canvas.configure(yscrollcommand=self.dynamic_scrollbar)
        
        self.label1 = customtkinter.CTkLabel(self.xy_frame, text="Choose Mode")
        self.label1.pack(anchor="w", padx=7)
        
        self.mode = customtkinter.CTkSegmentedButton(self.xy_frame, values=["Random", "Edges", "Threshold", "Waves", "Reference", "Border"],
                                                     command=self.update_settings)
        self.mode.pack(padx=(5,10), expand=True, fill="both", anchor="w")
     
        self.sub_frame = customtkinter.CTkFrame(self.xy_frame)
        self.sub_frame.pack(padx=(0,10), pady=(20,10), expand=True, fill="x", anchor="w")

        self.label_ut = customtkinter.CTkLabel(self.sub_frame, text="Upper Threshold")
        self.upper_threshold = customtkinter.CTkSlider(self.sub_frame, from_=0, to=1, command=lambda value: self.show_value(t1,value) or self.check_lower_value(value))
        t1 = CTkToolTip(self.upper_threshold, message="0.8", bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"], corner_radius=5)
        
        self.label_lt = customtkinter.CTkLabel(self.sub_frame, text="Lower Threshold")
        self.lower_threshold = customtkinter.CTkSlider(self.sub_frame, from_=0, to=1, command=lambda value: self.show_value(t2,value) or self.check_upper_value(value))
        t2 = CTkToolTip(self.lower_threshold, message="0.2", bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"], corner_radius=5)
        
        self.label_ch = customtkinter.CTkLabel(self.sub_frame, text="Character Length")
        self.chlength = CTkSpinbox(self.sub_frame, width=120)

        self.label_rd = customtkinter.CTkLabel(self.sub_frame, text="Amount")
        self.random = customtkinter.CTkSlider(self.sub_frame, from_=0, to=100, command=lambda value: self.show_value(t3,value))
        t3 = CTkToolTip(self.random, message="100.0", bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"], corner_radius=5)
        
        self.dial = Dial(self.sub_frame, start=0, end=360, color_gradient=("grey","grey"),
                         text_color=self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]), text="Angle: ",
                         bg=self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]))

        self.sub_frame2 = customtkinter.CTkFrame(self.sub_frame, fg_color="transparent")
        self.sub_frame2.columnconfigure((0,1,2,3), weight=1)
        self.sub_frame2.rowconfigure((0,1,2), weight=1)
        
        self.button1 = customtkinter.CTkButton(self.sub_frame2, text="Lightness", fg_color="transparent",
                                               border_width=2, command=lambda: self.update_func(0),
                                               text_color=["black","white"])
        self.button1.grid(row=0, column=0, columnspan=2, stick="nsew", padx=1, pady=2)

        self.button2 = customtkinter.CTkButton(self.sub_frame2, text="Hue", fg_color="transparent",
                                               border_width=2, command=lambda: self.update_func(1),
                                               text_color=["black","white"])
        self.button2.grid(row=0, column=2, columnspan=2, stick="nsew", padx=1, pady=2)
        
        self.button3 = customtkinter.CTkButton(self.sub_frame2, text="Saturation", fg_color="transparent",
                                               border_width=2, command=lambda: self.update_func(2),
                                               text_color=["black","white"])
        self.button3.grid(row=1, column=0, columnspan=2, stick="nsew", padx=1, pady=2)
        
        self.button4 = customtkinter.CTkButton(self.sub_frame2, text="Intensity", fg_color="transparent",
                                               border_width=2, command=lambda: self.update_func(3),
                                               text_color=["black","white"])
        self.button4.grid(row=1, column=2, columnspan=2, stick="nsew", padx=1, pady=2)
        
        self.button5 = customtkinter.CTkButton(self.sub_frame2, text="Minimum", fg_color="transparent",
                                               border_width=2, command=lambda: self.update_func(4),
                                               text_color=["black","white"])
        self.button5.grid(row=2, column=1, columnspan=2, stick="nsew", padx=1, pady=2)

        self.file_check = customtkinter.CTkCheckBox(self.sub_frame, text="Clean Edges")

        self.import_file = customtkinter.CTkButton(self.sub_frame, text="Import Reference Image", fg_color="transparent",
                                                   text_color=["black","white"], border_width=2, command=self.open_reference)
        self.import_file.drop_target_register(DND_ALL)
        self.import_file.dnd_bind("<<Drop>>", self.get_path_r)
        self.default_settings()

        self.render = customtkinter.CTkButton(self.xy_frame, text="Render", fg_color="transparent", border_width=2,
                                              text_color=["black","white"], command=self.start)
        self.render.pack(padx=5, pady=5, expand=True, fill="x")
        
        self.mask_label = customtkinter.CTkLabel(self.xy_frame, text="", height=1)
        self.mask_label.pack(padx=5, pady=5, expand=True, anchor="w")
        
        self.mode.set("Random")
        self.update_settings("Random")
        
    def turn_of(self):
        self.destroy()
        self.running = False
        
    def resource(self, relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    
    def show_value(self, tooltip, value):
        tooltip.configure(message=round(value,1))
        
    def about(self):
        CTkMessagebox(self, title="PIXELORT", message="Author: Akash Bora (Akascape) \nVersion: 0.1 \nMIT License \nCopyright 2023",
                      icon=self.resource(os.path.join("assets","logo.png")))
      
    def check_for_update(self):
        URL = "https://raw.githubusercontent.com/Akascape/Pixelort/VERSION.txt"
        
        try:
            response = requests.get(URL)
            version = float(response.content)
        except:
            CTkMessagebox(self, title="Unable to connect!", message="Unable to get information, please check your internet connection or visit the github repository.")
            return

        if version>App.CURRENT_VERSION:
            CTkMessagebox(self, title="Update Status", message=f"A new update v{version} is available! You can download it from our page.")
        else:
            CTkMessagebox(self, title="Update Status", message="You are on the latest version")
                
    def open_docs(self):
        webbrowser.open_new_tab("https://github.com/Akascape/Pixelort")

    def dynamic_scrollbar(self, x, y):
        if float(x)==0.0 and float(y)==1.0:
            self.xy_frame._scrollbar.configure(button_color=self.xy_frame._scrollbar.cget("bg_color"),
                                               button_hover_color=self.xy_frame._scrollbar.cget("bg_color"))
        else:
            self.xy_frame._scrollbar.configure(button_color=customtkinter.ThemeManager.theme["CTkScrollbar"]["button_color"],
                                               button_hover_color=customtkinter.ThemeManager.theme["CTkScrollbar"]["button_hover_color"])
        self.xy_frame._scrollbar.set(x,y)
        
    def change_menubarcolor(self):
        if customtkinter.get_appearance_mode()!="Dark":
            return
        self.menubar.configure(fg_color="#2b2b2b")
        
    def change_menubarcolor_dark(self):
        if customtkinter.get_appearance_mode()!="Dark":
            return
        self.menubar.configure(fg_color="black")
        
    def draw_mask(self):
        if self.file:
            dimentions = (self.img.size[0],self.img.size[1])
        else:
            dimentions = (500,500)

        if self.new:
            self.mask_window = DrawMask(self, image_file=self.file, size=dimentions, load_func=self.import_mask)
            self.new = False
        else:
            self.mask_window.deiconify()
            
    def remove_mask(self):
        self.mask = None
        self.mask_label.configure(text="")

    def import_mask(self, mask):
        self.mask = mask
        self.mask_label.configure(text="Mask in use!")
        
    def add_mask(self):
        file_m = tkinter.filedialog.askopenfilename(filetypes =[('Images', ['*.png','*.jpg','*.jpeg','*.bmp','*.webp'])
                                                                       ,('All Files', '*.*')])
        if file_m:
            try:
                Image.open(file_m)
            except UnidentifiedImageError:
                CTkMessagebox(self, title="Error Importing", message="Not a valid mask image!", icon="cancel")
                return
            self.mask = Image.open(file_m)
            self.mask_label.configure(text="Mask in use!")
        else:
            self.mask = None
            self.mask_label.configure(text="")
            
    def get_path(self, event):
        dropped_file = event.data.replace("{","").replace("}", "")
        if os.path.isfile(dropped_file):
            self.file = dropped_file
            self.load_image()
            
    def get_path_r(self, event):
        dropped_file = event.data.replace("{","").replace("}", "")
        if os.path.isfile(dropped_file):
            self.file_r = dropped_file
            self.open_reference(self.file_r)
            
    def export(self, ext):
        if not self.file: return
        save_name = self.file[:-4] + "_pixelsort." + ext
        count = 0
        while os.path.exists(save_name):
            count +=1
            save_name = self.file[:-4] + "_pixelsort" + str(count) + "." + ext
            
        save_file = tkinter.filedialog.asksaveasfilename(initialfile=os.path.basename(save_name),
                                                         filetypes=[('Image', ['*.png','*.jpg','*.jpeg','*.bmp','*.webp']),('All Files', '*.*')])
    
        if save_file:
            if not self.sorted_image:
                self.process()
            if ext=="jpg":
                self.sorted_image.convert("RGB").save(save_file)
            else:
                self.sorted_image.save(save_file)
        if os.path.exists(save_file):
            CTkMessagebox(self, title="Exported!", message="Your image is saved!", icon="check")
            
    def change_theme(self):
        if customtkinter.get_appearance_mode()=="Light":
            customtkinter.set_appearance_mode("Dark")
            self.after(100, lambda: self.menubar.configure(fg_color="black"))
        else:
            customtkinter.set_appearance_mode("Light")
            self.menubar.configure(fg_color="white")
            
        self.dial.configure(bg=self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]),
                            text_color=self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]))

    def open_reference(self, file_r=None):
        if not file_r:
            self.file_r = tkinter.filedialog.askopenfilename(filetypes =[('Images', ['*.png','*.jpg','*.jpeg','*.bmp','*.webp'])
                                                                       ,('All Files', '*.*')])
        if os.path.exists(self.file_r):

            try:
                Image.open(self.file_r)
            except UnidentifiedImageError:
                CTkMessagebox(self, title="Error Importing", message="Not a valid image file!", icon="cancel")
                return

            self.img_r = Image.open(self.file_r)   
            self.import_file.configure(text=os.path.basename(self.file_r))
        else:
            self.img_r = None
            self.import_file.configure(text="Import Reference Image")
            
    def do_zoom(self, delta):
        if self.image=="": return
        if delta>0:
            self.zoom +=1
        else:
            self.zoom -=1
        if self.zoom<=0 or self.zoom>2:
            return
        self.image.configure(size=(self.image_frame.winfo_height()*self.zoom,self.image_frame.winfo_height()*self.zoom*(self.img.size[1]/self.img.size[0])))
        
    def open_image(self):
        self.file = tkinter.filedialog.askopenfilename(filetypes =[('Images', ['*.png','*.jpg','*.jpeg','*.bmp','*.webp'])
                                                                   ,('All Files', '*.*')])
        self.load_image()
        
    def load_image(self):
        if os.path.exists(self.file):
            self.previous = self.file

            try:
                Image.open(self.file)
            except UnidentifiedImageError:
                CTkMessagebox(self, title="Error Importing", message="Not a valid image file!", icon="cancel")
                return

            self.img = Image.open(self.file)   
            self.image = customtkinter.CTkImage(self.img)
            self.image_frame.configure(text="", image=self.image)
            self.image.configure(size=(self.image_frame.winfo_reqwidth(),self.image_frame.winfo_reqheight()*(self.img.size[1]/self.img.size[0])))
            self.new = True
        else:
            if self.previous!="":
                self.file = self.previous

    def resize_event(self, event):
        if self.zoom>1: return
        if self.image!="":
            self.image.configure(size=(event.height,event.height*self.img.size[1]/self.img.size[0]))
            
    def check_upper_value(self, value):
        if value>self.upper_threshold.get():
            self.upper_threshold.set(value)

    def check_lower_value(self, value):
        if value<self.lower_threshold.get():
            self.lower_threshold.set(value)
                
    def default_settings(self):
        self.update_func(0)
        self.random.set(100)
        self.upper_threshold.set(0.8)
        self.lower_threshold.set(0.25)
        self.file_check.deselect()
        self.dial.set(0)
        self.chlength.set(50)
        
    def update_func(self, func):
        buttons = [self.button1, self.button2, self.button3, self.button4, self.button5]
        for i in buttons:
            i.configure(fg_color="transparent")
        buttons[func].configure(fg_color=self._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]))
        self.sort_func = buttons[func].cget("text").lower()
        
    def update_settings(self, mode):
        all_widgets = [self.label_ut, self.upper_threshold,
                       self.label_lt, self.lower_threshold,
                       self.label_rd, self.random, self.dial,
                       self.sub_frame2, self.file_check, self.import_file,
                       self.label_ch, self.chlength]
        for i in all_widgets:
            i.pack_forget()
        if mode=="Random":
            self.label_ch.pack(padx=5, pady=5, expand=True, anchor="w")
            self.chlength.pack(expand=True, anchor="w")
            self.interval_mode = "random"
        elif mode=="Edges":
            self.label_lt.pack(padx=5, pady=5, expand=True, anchor="w")
            self.lower_threshold.pack(expand=True, fill="x")
            self.interval_mode = "edges"
        elif mode=="Threshold":
            self.label_ut.pack(padx=5, pady=5, expand=True, anchor="w")
            self.upper_threshold.pack(expand=True, fill="x")
            self.label_lt.pack(padx=5, pady=5, expand=True, anchor="w")
            self.lower_threshold.pack(expand=True, fill="x")
            self.interval_mode = "threshold"
        elif mode=="Waves":
            self.label_ch.pack(padx=5, pady=5, expand=True, anchor="w")
            self.chlength.pack(expand=True, anchor="w")
            self.interval_mode = "waves"
        elif mode=="Reference":
            self.import_file.pack(expand=True, fill="x", pady=(5,15), padx=5)
            self.file_check.pack(anchor="w", padx=5)
            self.interval_mode = "file"
        else:
            self.interval_mode = "none"
            
        self.label_rd.pack(padx=5, pady=5, expand=True, anchor="w")
        self.random.pack(expand=True, fill="x")
        self.dial.pack(padx=5, pady=10, anchor="nw", side="left")
        self.sub_frame2.pack(padx=(5,10), expand=True, fill="x", pady=10)

    def start(self):
        threading.Thread(target=self.process).start()
   
    def process(self):
        if not self.file: return
        if not self.running:
            self.running = True
        else:
            return
        if self.interval_mode=="file":
            if not self.img_r:
                CTkMessagebox(self, title="No Reference", message="Please import a reference file", icon="warning")
                self.running = False
                return
            if self.file_check.get():
                self.interval_mode = "file-edges"
            else:
                self.interval_mode = "file"

        self.render.configure(state="Disabled", text="...")
        if self.chlength.get()<=5:
            self.chlength.set(5)
        try:
            self.update()
            self.sorted_image = pixelsort(self.img,
                                          randomness=100-self.random.get(),
                                          clength=self.chlength.get(),
                                          mask_image=self.mask,
                                          sorting_function=self.sort_func,
                                          interval_function=self.interval_mode,
                                          interval_image=self.img_r,
                                          lower_threshold=self.lower_threshold.get(),
                                          upper_threshold=self.upper_threshold.get(),
                                          angle=self.dial.get())
            
            self.image = customtkinter.CTkImage(self.sorted_image, size=(
                                                self.image_frame.winfo_height(),
                                                self.image_frame.winfo_height() * self.img.size[1] / self.img.size[0]))
            self.image_frame.configure(text="", image=self.image)

        except IndexError:
            CTkMessagebox(self, title="Size Issue", message="Reference image/mask size is not matching!", icon="cancel")
            
        except:
            if not self.running:
                return
            CTkMessagebox(self, title="Error", message="Something went wrong!", icon="cancel")
            
        self.render.configure(state="Normal", text="Render")
        self.running = False
        
    def on_closing(self):
        res = CTkMessagebox(self, title="Exit?", message="Do you want to close the program?", icon="question", options=["Yes","No","Cancel"])
        des = res.get()
        if des=="Yes":
            self.destroy()
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
