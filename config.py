import os
import random
class Configer():
    def __init__(self):
        try:
            with open("config.ini",'r') as f:
                lines = f.readlines()
            self.pencil_color = tuple(map(int, lines[0].strip().split(' ')))
            self.pencil_thickness = int(lines[1].strip())
            self.mode = lines[2].strip()
            self.save_dir = lines[3].strip()
            self.current_img = int(lines[4].strip())
            self.rect_type = int(lines[5].strip())
            self.type_color = [(int(i), int(j), int(k)) for i, j, k in zip(lines[6].strip().split(' ')[0::3], lines[6].strip().split(' ')[1::3], lines[6].strip().split(' ')[2::3])]
            self.type_name = lines[7].strip().split()

        except Exception:
            self.pencil_color = (0, 0, 0)
            self.pencil_thickness = 5
            self.mode = "detection"
            self.save_dir = os.getcwd()
            self.current_img = 0
            self.rect_type = 0
            self.type_color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            self.type_name = ["class1", "class2", "class3", "class4", "class5", "class6"]


    def save_config(self):
        with open("config.ini",'w') as f:
            f.write(str(self.pencil_color[0]) + ' ' + str(self.pencil_color[1]) + ' ' + str(self.pencil_color[2]) + '\n')
            f.write(str(self.pencil_thickness) + '\n')
            f.write(self.mode + '\n')
            f.write(self.save_dir + '\n')
            f.write(str(self.current_img) + '\n')
            f.write(str(self.rect_type) + '\n')
            for i in self.type_color:
                for j in i:
                    f.write(str(j) + " ")
            f.write("\n")
            for name in self.type_name:
                f.write(name + " ")
            f.write("\n")
