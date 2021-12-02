from genericpath import exists
import os
from tkinter.constants import S
from typing import Text, cast
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import image_names, ttk,filedialog, font, messagebox
from config import Configer
import tkinter.colorchooser as cc

from utils import RGB_to_Hex, clip
import time
def add_imgs():
    global bg_index, now_showing, img_changed, bg, fg, fg_switch, rectangles, rect_pos
    default_dir = r"C:/"
    current_len = img_box.size()
    files = filedialog.askopenfilenames(title = u'choose images', initialdir = (os.path.expanduser(default_dir)))
    not_supported = False
    for item in files:
        if item.endswith(".jpg") or item.endswith(".png"):
            img_box.insert(tk.END, item)
        else:
            not_supported = True
    if not_supported:
        messagebox.showwarning(title = "SB", message = "Format error, has been automatically removed!!!")

    if bg_index == -1 and current_len == 0:
        img_path = img_box.get(0)
        if img_path:
            bg_index = 0
            now_showing = (now_showing + 1) % 2
            fg_switch = (fg_switch + 1) % 2
            bg = Image.open(img_path)
            bg_list[now_showing] = ImageTk.PhotoImage(bg)
            canvas.configure(scrollregion = (0, 0, bg.size[0], bg.size[1]))
            canvas.itemconfig(bg_id, image = bg_list[now_showing])
            fg = Image.new('RGBA', (bg.size[0], bg.size[1]), (0, 0, 0, 0))
            fg_list[fg_switch] = ImageTk.PhotoImage(fg)
            canvas.itemconfig(fg_id, image = fg_list[fg_switch])
            canvas.tag_raise(fg_id)
            for item in rectangles:
                canvas.delete(item)
            rectangles = []
            rect_pos = []
            rect_box_len = rec_box.size()
            for i in range(rect_box_len)[::-1]:
                rec_box.delete(i)

def add_dir():
    global bg_index, now_showing, img_changed, bg, fg, fg_switch, rectangles, rect_pos
    default_dir = r"C:/"
    current_len = img_box.size()
    file_path = filedialog.askdirectory(title = u'choose directory', initialdir = (os.path.expanduser(default_dir)))
    has_item = False
    for item in os.listdir(file_path):
        if item.endswith(".jpg") or item.endswith(".png"):
            img_box.insert(tk.END, os.path.join(file_path, item))
            has_item = True
    if not has_item:
        messagebox.showwarning(title = "SB", message = "No supported images found!!!")
    if bg_index == -1 and current_len == 0:
        img_path = img_box.get(0)
        if img_path:
            bg_index = 0
            now_showing = (now_showing + 1) % 2
            fg_switch = (fg_switch + 1) % 2
            bg = Image.open(img_path)
            bg_list[now_showing] = ImageTk.PhotoImage(bg)
            canvas.configure(scrollregion = (0, 0, bg.size[0], bg.size[1]))
            canvas.itemconfig(bg_id, image = bg_list[now_showing])
            fg = Image.new('RGBA', (bg.size[0], bg.size[1]), (0, 0, 0, 0))
            fg_list[fg_switch] = ImageTk.PhotoImage(fg)
            canvas.itemconfig(fg_id, image = fg_list[fg_switch])
            canvas.tag_raise(fg_id)
            for item in rectangles:
                canvas.delete(item)
            rectangles = []
            rect_pos = []
            rect_box_len = rec_box.size()
            for i in range(rect_box_len)[::-1]:
                rec_box.delete(i)

def switch_mode():
    global cfg
    cfg.mode = mode[mode_var.get()]
    if cfg.mode == "detection":
        canvas.config(cursor = "crosshair")
    else:
        canvas.config(cursor = "circle")

def change_color():
    global cfg
    choose = cc.askcolor()
    cfg.pencil_color = choose[0]
    color_l.config(background = choose[1], text = choose[1])

def adjust_thickness(event):
    global cfg
    cfg.pencil_thickness = thickness_var.get()

def zoom_in():
    global bg, fg, now_showing, fg_switch, bg_index
    if bg_index == -1:
        return
    try:
        percent = int(zoom_var.get()) + 3
        if percent < 30 or percent > 500:
            raise Exception("Input must be within 30-500")
        zoom_var.set(str(percent))
        percent = percent / 100
        nw = int(bg.size[0] * percent)
        nh = int(bg.size[1] * percent)
        img = bg.resize((nw,nh))
        fg = fg.resize((nw,nh), Image.NEAREST)
        now_showing = (now_showing + 1) % 2
        fg_switch = (fg_switch + 1) % 2
        bg_list[now_showing] = ImageTk.PhotoImage(img)
        canvas.configure(scrollregion = (0, 0, nw, nh))
        canvas.itemconfig(bg_id, image = bg_list[now_showing])
        fg_list[fg_switch] = ImageTk.PhotoImage(fg)
        canvas.itemconfig(fg_id, image = fg_list[fg_switch])
        canvas.tag_raise(fg_id)
        refresh_rect(percent, show = True)
    except Exception as e:
        messagebox.showwarning(title = "SB", message = e)
        zoom_var.set("100")

def zoom_out():
    global bg, fg, now_showing, fg_switch, bg_index
    if bg_index == -1:
        return
    try:
        percent = int(zoom_var.get()) - 3
        if percent < 30 or percent > 500:
            raise Exception("Input must be within 30-500")
        zoom_var.set(str(percent))
        percent = percent / 100
        nw = int(bg.size[0] * percent)
        nh = int(bg.size[1] * percent)
        img = bg.resize((nw,nh))
        fg = fg.resize((nw,nh), Image.NEAREST)
        now_showing = (now_showing + 1) % 2
        fg_switch = (fg_switch + 1) % 2
        bg_list[now_showing] = ImageTk.PhotoImage(img)
        canvas.configure(scrollregion = (0, 0, nw, nh))
        canvas.itemconfig(bg_id, image = bg_list[now_showing])
        fg_list[fg_switch] = ImageTk.PhotoImage(fg)
        canvas.itemconfig(fg_id, image = fg_list[fg_switch])
        canvas.tag_raise(fg_id)
        refresh_rect(percent, show = True)
    except Exception as e:
        messagebox.showwarning(title = "SB", message = e)
        zoom_var.set("100")

def zoom_enter(event):
    global bg, fg, now_showing, fg_switch, bg_index
    if bg_index == -1:
        return
    try:
        percent = int(zoom_var.get())
        if percent < 30 or percent > 500:
            raise Exception("Input must be within 30-500")
        zoom_var.set(str(percent))
        percent = percent / 100
        nw = int(bg.size[0] * percent)
        nh = int(bg.size[1] * percent)
        img = bg.resize((nw,nh))
        fg = fg.resize((nw,nh), Image.NEAREST)
        now_showing = (now_showing + 1) % 2
        fg_switch = (fg_switch + 1) % 2
        bg_list[now_showing] = ImageTk.PhotoImage(img)
        canvas.configure(scrollregion = (0, 0, nw, nh))
        canvas.itemconfig(bg_id, image = bg_list[now_showing])
        fg_list[fg_switch] = ImageTk.PhotoImage(fg)
        canvas.itemconfig(fg_id, image = fg_list[fg_switch])
        refresh_rect(percent, show = True)

    except Exception as e:
        messagebox.showwarning(title = "SB", message = e)
        zoom_var.set("100")

def change_dir():
    default_dir = r"C:/"
    output_path = filedialog.askdirectory(title = u'choose directory', initialdir = (os.path.expanduser(default_dir)))
    if output_path:
        output_dir_var.set(output_path)
        dir_enter()

def dir_enter(event = None):
    output_path = output_dir_var.get()
    if os.path.exists(output_path):
        output_dir_var.set(output_path)
    else:
        messagebox.showwarning(title = "SB", message = "Directory doesnot exist, already set to default directory!!!")
        output_path = os.getcwd()
        output_dir_var.set(output_path)
    if not os.path.exists(os.path.join(output_path, "image")):
        os.makedirs(os.path.join(output_path, "image"))
    if not os.path.exists(os.path.join(output_path, "label")):
        os.makedirs(os.path.join(output_path, "label"))
    if not os.path.exists(os.path.join(output_path, "txt")):
        os.makedirs(os.path.join(output_path, "txt"))

def save(event = None):
    global bg_index, bg, fg, cfg, img_changed, lb_dict, rect_dict, rect_pos
    output_path = output_dir_var.get()
    if bg_index == -1:
        return
    if not img_changed:
        return
    if not os.path.exists(output_path):
        messagebox.showwarning(title = "SB", message = "Directory doesnot exist, already set to default directory!!!")
        output_path = os.getcwd()
        output_dir_var.set(output_path)
    if not os.path.exists(os.path.join(output_path, "image")):
        os.makedirs(os.path.join(output_path, "image"))
    if not os.path.exists(os.path.join(output_path, "label")):
        os.makedirs(os.path.join(output_path, "label"))
    if not os.path.exists(os.path.join(output_path, "txt")):
        os.makedirs(os.path.join(output_path, "txt"))

    img_name = img_box.get(bg_index)
    # img_box.itemconfig(bg_index, {'bg':'#5F94BE'})
    if img_name in lb_dict:
        img_path = img_name
        lb_path = lb_dict[img_name]
        fg_save = fg.resize((bg.size[0], bg.size[1]), Image.NEAREST)
        fg_save.save(lb_path)
    if img_name in rect_dict:
        txt_path = rect_dict[img_name]
        with open(txt_path, 'w') as f:
            for pos in rect_pos:
                f.write(str(pos[0]))
                f.write(" ")
                f.write(str(pos[1]))
                f.write(" ")
                f.write(str(pos[2]))
                f.write(" ")
                f.write(str(pos[3]))
                f.write(" ")
                f.write(str(pos[4]))
                f.write("\n")
    else:
        img_path = output_path + "/image/" + str(cfg.current_img) + ".jpg"
        lb_path = output_path + "/label/" + str(cfg.current_img) + ".png"
        txt_path = output_path + "/txt/" + str(cfg.current_img) + ".txt"

        bg.save(img_path)
        fg_save = fg.resize((bg.size[0], bg.size[1]), Image.NEAREST)
        fg_save.save(lb_path)
        print(txt_path)
        with open(txt_path, 'w') as f:
            for pos in rect_pos:
                f.write(str(pos[0]))
                f.write(" ")
                f.write(str(pos[1]))
                f.write(" ")
                f.write(str(pos[2]))
                f.write(" ")
                f.write(str(pos[3]))
                f.write(" ")
                f.write(str(pos[4]))
                f.write("\n")
        
        cfg.current_img += 1
        rect_dict[img_name] = txt_path
        lb_dict[img_name] = lb_path
    img_changed = False
    
    # to be continue

def refresh_rect(rate = 1, show = False):
    global rect_pos, rectangles
    for i in range(len(rect_pos)):
        nx1 = int(rate * rect_pos[i][0])
        ny1 = int(rate * rect_pos[i][1])
        nx2 = int(rate * rect_pos[i][2])
        ny2 = int(rate * rect_pos[i][3])
        if show:
            canvas.coords(rectangles[i], nx1, ny1, nx2, ny2)
            canvas.tag_raise(rectangles[i])


def create_point(x1, y1, x2, y2, **kwargs):
    global fg_switch, fg
    if 'alpha' in kwargs:
        fg_switch = (fg_switch + 1) % 2
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = fill + (alpha, )
        draw = ImageDraw.Draw(fg)
        draw.ellipse((x1, y1, x2, y2), fill = fill)
        fg_list[fg_switch] = ImageTk.PhotoImage(fg)
        canvas.itemconfig(fg_id, image = fg_list[fg_switch])

def paint(event):
    global bg_index, cfg, img_changed, bg
    if bg_index == -1:
        return
    current_select = rec_box.curselection()
    percent = int(zoom_var.get())
    zoom_var.set(str(percent))
    percent = percent / 100

    
    if cfg.mode == "segmentation" and cfg.pencil_color != (0, 0, 0):
        img_changed = True
        x = int(hbar.get()[0] * bg.size[0] * percent) + event.x
        y = int(vbar.get()[0] * bg.size[1] * percent) + event.y

        create_point(x - cfg.pencil_thickness, y - cfg.pencil_thickness, x + cfg.pencil_thickness, y + cfg.pencil_thickness, alpha = .5, fill = cfg.pencil_color)
    if cfg.mode == "detection":
        x_begin = int(hbar.get()[0] * bg.size[0] * percent)
        y_begin = int(vbar.get()[0] * bg.size[1] * percent)

        x = clip(event.x, 0, event.widget.winfo_width())
        y = clip(event.y, 0, event.widget.winfo_height())
    
        if len(current_select) == 1:
            
            idx = current_select[0]
            startx = int(rect_pos[idx][0] * percent)
            starty = int(rect_pos[idx][1] * percent)
            endx = x_begin + x
            endy = y_begin + y

            endx = clip(endx, 0, int(bg.size[0] * percent))
            endy = clip(endy, 0, int(bg.size[0] * percent))

            canvas.coords(rectangles[idx], startx, starty, endx, endy)
            rect_pos[idx][2] = int(endx / percent)
            rect_pos[idx][3] = int(endy / percent)

        elif len(current_select) == 0:
            
            idx = -1
            startx = int(rect_pos[idx][0] * percent)
            starty = int(rect_pos[idx][1] * percent)
            endx = x_begin + x
            endy = y_begin + y
            endx = clip(endx, 0, int(bg.size[0] * percent))
            endy = clip(endy, 0, int(bg.size[0] * percent))
            canvas.coords(rectangles[idx], startx, starty, endx, endy)
            rect_pos[idx][2] = int(endx / percent)
            rect_pos[idx][3] = int(endy / percent)

def erase(event):
    global cfg, img_changed
    if cfg.mode == 'segmentation':
        img_changed = True
        x1, y1 = (event.x - cfg.pencil_thickness), (event.y - cfg.pencil_thickness)
        x2, y2 = (event.x + cfg.pencil_thickness), (event.y + cfg.pencil_thickness)
        create_point(x1, y1, x2, y2, alpha = 0, fill = (0, 0, 0))

def switch_image(event):
    global bg_index, now_showing, fg_switch, img_changed, bg, fg, lb_dict, rect_dict, rectangles, rect_pos
    current_selection = img_box.curselection()[0]
    if current_selection == bg_index:
        return
    if img_changed:
        msg = tk.messagebox.askquestion(title = "warning", message = "The current image has not been saved, do you want to save it!")
        if msg == "yes":
            save()
        else:
            print("fnndp")
            img_changed = False
    
    for item in rectangles:
        canvas.delete(item)
    rectangles = []
    rect_pos = []
    rect_box_len = rec_box.size()
    for i in range(rect_box_len)[::-1]:
        rec_box.delete(i)

    bg_index = current_selection
    img_name = img_box.get(current_selection)
    now_showing = (now_showing + 1) % 2
    fg_switch = (fg_switch + 1) % 2
    bg = Image.open(img_name)

    try:
        percent = int(zoom_var.get())
        percent = percent / 100
        nw = int(bg.size[0] * percent)
        nh = int(bg.size[1] * percent)
        img = bg.resize((nw,nh))
    except Exception:
        messagebox.showwarning(title = "SB", message = "Input must be number only!!!")
        zoom_var.set("100")
        percent = 1
        nw = int(bg.size[0] * percent)
        nh = int(bg.size[1] * percent)
        img = bg.resize((nw,nh))

    
    bg_list[now_showing] = ImageTk.PhotoImage(img)
    canvas.configure(scrollregion = (0, 0, nw, nh))

    canvas.itemconfig(bg_id, image = bg_list[now_showing])
    if img_name in lb_dict:
        fg = Image.open(lb_dict[img_name])
        fg = fg.resize((nw, nh), Image.NEAREST)
    else:
        fg = Image.new('RGBA', (nw, nh), (0, 0, 0, 0))
    fg_list[fg_switch] = ImageTk.PhotoImage(fg)
    if img_name in rect_dict:
        with open(rect_dict[img_name], 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            line = line.split(' ')
            startx = int(line[0])
            starty = int(line[1])
            endx = int(line[2])
            endy = int(line[3])
            category = int(line[4])
            rect_pos.append([startx, starty, endx, endy, category])
            startx = int(startx * percent)
            starty = int(starty * percent)
            endx = int(endx * percent)
            endy = int(endy * percent)
            rectangles.append(canvas.create_rectangle(startx, starty, endx, endy, outline = RGB_to_Hex(cfg.type_color[category])))
            rec_box.insert(tk.END, cfg.type_name[category])

    canvas.itemconfig(fg_id, image = fg_list[fg_switch])

    canvas.tag_raise(fg_id)

def delete_select(all = False):
    global bg_index, img_changed, now_showing, fg_switch, bg, fg
    if all:
        current_select = range(img_box.size())
    else:
        current_select = img_box.curselection()
    if bg_index in current_select:
        if img_changed:
            msg = tk.messagebox.askquestion(title = "warning", message = "The current image has not been saved, do you want to save it!")
            if msg == "yes":
                save()
            else:
                print("fnndp")
                img_changed = False
        for i in current_select[::-1]:
            if i < bg_index:
                bg_index -= 1
            img_box.delete(i)
        bg_index = -1
        now_showing = (now_showing + 1) % 2

        bg = Image.new('RGBA', (512, 384), (0, 0, 0, 0))
        bg_list[now_showing] = ImageTk.PhotoImage(bg)

        canvas.configure(scrollregion = (0, 0, 512, 384))
        canvas.itemconfig(bg_id, image = bg_list[now_showing])

        bg_index = -1

        fg = Image.new('RGBA', (512, 384), (0,0,0,0))
        fg_switch = (fg_switch + 1) % 2
        fg_list[fg_switch] = ImageTk.PhotoImage(fg)
        
        canvas.itemconfig(fg_id, image = fg_list[fg_switch])
        canvas.tag_raise(fg_id)
    else:
        for i in current_select[::-1]:
            if i < bg_index:
                bg_index -= 1
            img_box.delete(i)
def delete_all():
    delete_select(all = True)
        
def popupmenu(event):
    imgbox_menu_m.post(event.x_root, event.y_root)

def on_button_press(event):
    global bg_index, img_changed, bg
    if bg_index == -1:
        return
    if cfg.mode == "detection":
        percent = int(zoom_var.get())
        zoom_var.set(str(percent))
        percent = percent / 100
        current_select = rec_box.curselection()

        x_begin = int(hbar.get()[0] * bg.size[0] * percent)
        y_begin = int(vbar.get()[0] * bg.size[1] * percent)

        x = clip(event.x, 0, event.widget.winfo_width())
        y = clip(event.y, 0, event.widget.winfo_height())
        
        if len(current_select) == 1:
            idx = current_select[0]
            
            category = int(rect_type_e.get())
            
            startx = x_begin + x
            starty = y_begin + y
            
            startx = clip(startx, 0, int(bg.size[0] * percent))
            starty = clip(starty, 0, int(bg.size[0] * percent))

            canvas.coords(rectangles[idx], startx, starty, startx + 1, starty + 1)
            
            startx = int(startx / percent)
            starty = int(starty / percent)

            rect_pos[idx] = [startx, starty, startx + 1, starty + 1, category]
            canvas.itemconfig(rectangles[idx], outline = RGB_to_Hex(cfg.type_color[category]))
            img_changed = True

        if len(current_select) == 0:
            category = int(rect_type_e.get())
            rec_box.insert(tk.END, cfg.type_name[category])
            startx = x_begin + x
            starty = y_begin + y
            startx = clip(startx, 0, int(bg.size[0] * percent))
            starty = clip(starty, 0, int(bg.size[0] * percent))
            rectangle = canvas.create_rectangle(startx, starty, startx + 1, starty + 1, outline = RGB_to_Hex(cfg.type_color[category]))

            rectangles.append(rectangle)

            startx = int(startx / percent)
            starty = int(starty / percent)

            rect_pos.append([startx, starty, startx + 1, starty + 1, category])
            
            img_changed = True


def on_button_release(event):
    global rect_pos, cfg
    if bg_index == -1:
        return
    if cfg.mode == "detection":
        for i in range(len(rect_pos))[::-1]:
            x1 = min(rect_pos[i][0], rect_pos[i][2])
            x2 = max(rect_pos[i][0], rect_pos[i][2])
            y1 = min(rect_pos[i][1], rect_pos[i][3])
            y2 = max(rect_pos[i][1], rect_pos[i][3])
            rect_pos[i][0] = x1
            rect_pos[i][1] = y1
            rect_pos[i][2] = x2
            rect_pos[i][3] = y2
            if rect_pos[i][2] == rect_pos[i][0] or rect_pos[i][3] == rect_pos[i][1]:
                canvas.delete(rectangles[i])
                del rectangles[i]
                del rect_pos[i]
                rec_box.delete(i)

def highlight_box(event):
    global rectangles, cfg
    current_select = rec_box.curselection()
    if len(current_select) == 1:
        idx = current_select[0]
        canvas.itemconfig(rectangles[idx], fill = 'blue')
        canvas.tag_raise(rectangles[idx])
        canvas.update_idletasks() 
        canvas.update()
        time.sleep(1)
        canvas.itemconfig(rectangles[idx], fill = '')

def popupmenu_rec(event):
    recbox_menu_m.post(event.x_root, event.y_root)

def delete_all_rec():
    delete_select_rec(all = True)

def delete_select_rec(all = False):
    global rectangles, rect_pos
    if all:
        current_select = range(rec_box.size())
    else:
        current_select = rec_box.curselection()
    
    for i in current_select[::-1]:
        rec_box.delete(i)
        canvas.delete(rectangles[i])
        del rectangles[i]
        del rect_pos[i]
    
def closeWindow():
    global img_changed
    if img_changed:
        msg = tk.messagebox.askquestion(title = "warning", message = "The current image has not been saved, do you want to save it!")
        if msg == "yes":
            save()
        else:
            print("fnndp")
            img_changed = False
    root.destroy()


cfg = Configer()


mode = ["detection", "segmentation"]


root = tk.Tk()
root.title("jjw_label")
root.geometry('1024x768')
rectangles = []
rect_pos = [] 

bg = Image.new('RGBA', (512, 384), (0, 0, 0, 0))
bg_list = []
bg_list.append(ImageTk.PhotoImage(bg))
bg_list.append(ImageTk.PhotoImage(bg))
bg_index = -1

fg = Image.new('RGBA', (512, 384), (0, 0, 0, 0))
fg_switch = 0
fg_list = []
fg_list.append(ImageTk.PhotoImage(fg))
fg_list.append(ImageTk.PhotoImage(fg))

now_showing = 0
img_changed = False

lb_dict = {}
rect_dict = {}


mode_var = tk.IntVar()
thickness_var = tk.IntVar()
zoom_var = tk.StringVar()
output_dir_var = tk.StringVar()
type_var = tk.StringVar()
output_dir_var.set(cfg.save_dir)
type_var.set(cfg.rect_type)

dir_enter()

mode_var.set(mode.index(cfg.mode))
thickness_var.set(cfg.pencil_thickness)

add_imgs_b = tk.Button(root, text = "Add images", command = add_imgs)
add_imgs_b.place(relwidth = 0.1, relheight = 0.05, relx = 0.01, rely=0.01)

add_dir_b = tk.Button(root, text = 'Add directory', command = add_dir)
add_dir_b.place(relwidth = 0.1, relheight = 0.05, relx = 0.01, rely=0.08)

mode_sel_l = tk.Label(root, text = "mode selection")
mode_sel_l.place(relx = 0.01, rely=0.16)
det_op_rb = tk.Radiobutton(root, text = mode[0], variable = mode_var, value = 0, command = switch_mode)
det_op_rb.place(relx = 0.01, rely=0.20)
seg_op_rb = tk.Radiobutton(root, text = mode[1], variable = mode_var, value = 1, command = switch_mode)
seg_op_rb.place(relx = 0.01, rely=0.24)

color_b = tk.Button(root, text = 'pencil color', command = change_color)
color_b.place(relwidth = 0.1, relheight = 0.05, relx = 0.01, rely=0.31)

color_l = tk.Label(root, text = RGB_to_Hex(cfg.pencil_color), bg = RGB_to_Hex(cfg.pencil_color), fg = "white")
color_l.place(relwidth = 0.1, relheight = 0.03,relx = 0.01, rely=0.37)

thick_s = tk.Scale(root, label = 'pencil thickness', from_ = 1,to = 100, resolution = 1, orient = tk.HORIZONTAL, show = 0, variable = thickness_var,command = adjust_thickness)
thick_s.place(relx = 0.01, rely=0.44)


zoom_txt_l = tk.Label(root, text = "zoom in/out")
zoom_txt_l.place(relwidth = 0.1, relheight = 0.03,relx = 0.01, rely = 0.54)
zoom_font = font.Font(size = 10)

zoom_in_b = tk.Button(root, text = '+', font = zoom_font,  command = zoom_in)
zoom_in_b.place(relwidth = 0.05, relheight = 0.05, relx = 0.035, rely=0.59)

zoom_per_e = tk.Entry(root, textvariable = zoom_var)
zoom_per_e.place(relwidth = 0.05, relheight = 0.02, relx = 0.035, rely=0.66)
zoom_per_e.insert(0,"100")

zoom_out_b = tk.Button(root, text = '-', font = zoom_font, command = zoom_out)
zoom_out_b.place(relwidth = 0.05, relheight = 0.05, relx = 0.035, rely=0.70)

output_dir_b = tk.Button(root, text = "output directory", command = change_dir)
output_dir_b.place(relwidth = 0.1, relheight = 0.05, relx = 0.01, rely=0.80)

output_dir_e = tk.Entry(root, textvariable = output_dir_var)
output_dir_e.place(relwidth = 0.1, relheight = 0.03, relx = 0.01, rely=0.85)

save_b = tk.Button(root, text = "SAVE\n hot key: s", command = save)
save_b.place(relwidth = 0.1, relheight = 0.05, relx = 0.01, rely=0.93)


splite_line = ttk.Separator(root, orient = 'vertical').place(relwidth = 0.03, relheight = 1, relx = 0.14, rely = 0.0)

canvasframe = tk.Frame(root)
canvasframe.place(relwidth = 0.7, relheight = 1, relx = 0.16, rely = 0.0)

canvas = tk.Canvas(canvasframe, cursor = 'crosshair' if cfg.mode == "detection" else 'circle')
canvas.configure(scrollregion = canvas.bbox("all"))

hbar = tk.Scrollbar(canvasframe, orient = tk.HORIZONTAL)
hbar.pack(side = tk.BOTTOM,fill = tk.X)
hbar.config(command = canvas.xview)
vbar = tk.Scrollbar(canvasframe, orient = tk.VERTICAL)
vbar.pack(side = tk.RIGHT,fill = tk.Y)
vbar.config(command = canvas.yview)

canvas.config(xscrollcommand = hbar.set, yscrollcommand = vbar.set)
canvas.pack(side = tk.LEFT,expand = True,fill = tk.BOTH)


img_txt_l = tk.Label(root, text = "image list")
img_txt_l.place(relwidth = 0.1, relheight = 0.02, relx = 0.88, rely = 0.01)

img_boxframe = tk.Frame(root)
img_boxframe.place(relwidth = 0.1, relheight = 0.4, relx = 0.88, rely = 0.05)

box_font = font.Font(size = 10)
img_box = tk.Listbox(img_boxframe, selectmode = tk.EXTENDED, font = box_font)

img_box_ybar_s = tk.Scrollbar(img_boxframe, orient = tk.VERTICAL, command = img_box.yview)
img_box_ybar_s.place(relwidth = 0.15, relheight = 1, relx = 0.85, rely = 0)
img_box.config(yscrollcommand = img_box_ybar_s.set)

img_box_xbar_s = tk.Scrollbar(img_boxframe, orient = tk.HORIZONTAL, command = img_box.xview)
img_box_xbar_s.place(relwidth = 1, relheight = 0.05, relx = 0, rely = 0.95)
img_box.config(xscrollcommand = img_box_xbar_s.set)

img_box.place(relwidth = 0.85, relheight = 0.95, relx = 0, rely = 0)


rec_txt_l = tk.Label(root, text = "rectangle list")
rec_txt_l.place(relwidth = 0.1, relheight = 0.02, relx = 0.88, rely = 0.46)

rectframe = tk.Frame(root)
rectframe.place(relwidth = 0.1, relheight = 0.4, relx = 0.88, rely = 0.50)

rec_box = tk.Listbox(rectframe, selectmode = tk.EXTENDED, font = box_font)

rec_box_ybar_s = tk.Scrollbar(rectframe, orient = tk.VERTICAL, command = rec_box.yview)
rec_box_ybar_s.place(relwidth = 0.15, relheight = 1, relx = 0.85, rely = 0)
rec_box.config(yscrollcommand = rec_box_ybar_s.set)

rec_box_xbar_s = tk.Scrollbar(rectframe, orient = tk.HORIZONTAL, command = rec_box.xview)
rec_box_xbar_s.place(relwidth = 1, relheight = 0.05, relx = 0, rely = 0.95)
rec_box.config(xscrollcommand = rec_box_xbar_s.set)

rec_box.place(relwidth = 0.85, relheight = 0.95, relx = 0, rely = 0)

type_txt_l = tk.Label(root, text = "rectangle type")
type_txt_l.place(relwidth = 0.1, relheight = 0.02, relx = 0.88, rely = 0.92)

rect_type_e = tk.Entry(root, textvariable = type_var)
rect_type_e.place(relwidth = 0.1, relheight = 0.03, relx = 0.88, rely=0.95)

bg_id = canvas.create_image(0, 0, anchor = tk.NW, image = bg_list[now_showing])
fg_id = canvas.create_image(0, 0, anchor = tk.NW, image = fg_list[fg_switch])

imgbox_menu_m = tk.Menu(root, tearoff = 0)
imgbox_menu_m.add_command(label = "Delete Select", command = delete_select)
imgbox_menu_m.add_separator()
imgbox_menu_m.add_command(label = "Delete ALL", command = delete_all)

img_box.bind("<Button-3>", popupmenu)

recbox_menu_m = tk.Menu(root, tearoff = 0)
recbox_menu_m.add_command(label = "Delete Select", command = delete_select_rec)
recbox_menu_m.add_separator()
recbox_menu_m.add_command(label = "Delete ALL", command = delete_all_rec)

rec_box.bind("<Button-3>", popupmenu_rec)


root.bind('s', save)
zoom_per_e.bind('<Return>', zoom_enter)
output_dir_e.bind('<Return>', dir_enter)
canvas.bind('<B1-Motion>', paint)
canvas.bind('<B3-Motion>', erase)

canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<ButtonRelease-1>", on_button_release)
img_box.bind('<Double-Button>', switch_image)
rec_box.bind('<Double-Button>', highlight_box)

root.protocol("WM_DELETE_WINDOW", closeWindow)
root.mainloop()
cfg.save_config()