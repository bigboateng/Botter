import os
import ast

from Models.BoxFunction import BoxFunction


class Library(object):

    def __init__(self, destination, screen_box, directory, functions):

        self.destination = destination
        self.screen_box = screen_box
        self.directory = directory
        self.functions = functions

    @staticmethod
    def create_library(destination, screen_box, directory, functions):
        name = os.path.basename(os.path.normpath(destination))
        with open(destination+".py", 'w') as file:
            file.write("import random\n"
                       "import numpy\n"
                       "import cv2\n"
                       "import pyocr\n"
                       "import pyocr.builders\n"
                       "from PIL import Image, ImageFilter\n"
                       "from mss import mss\n")
            file.write("\n\n")
            file.write("""class {}(object):\n"""
                       """# c {{'screen_box': {}, 'directory': '{}'}}\n"""
                       """\n"""
                       """    def __init__(self):\n"""
                       """        self.img = None\n"""
                       """        tools = pyocr.get_available_tools()\n"""
                       """        if len(tools) == 0:\n"""
                       """            print('No OCR tool found')\n"""
                       """            sys.exit(1)\n"""
                       """        self.tool = tools[0]\n"""
                       """        print("Will use tool '%s'" % (self.tool.get_name()))\n""".format(name, screen_box, directory))
            file.write("\n")
            file.write("    def grab_screen(self):\n"
                       "        with mss() as sct:\n")
            if screen_box:
                file.write("            img = sct.grab({})\n".format(screen_box))
            else:
                file.write("            img = sct.shot()\n")
            file.write("        self.img = Image.frombytes('RGB', img.size, img.rgb)\n"
                       "        return self.img\n")
            file.write("\n")
            for function in functions:
                file.write("    def {}(self):\n"
                           "# f BoxFunction('{}', '{}', {}, {})\n"
                           "cropped = self.img.crop([{}, {}, {}, {}])\n".format
                    (
                        function.name,
                        function.name, function.type, function.box, function.image,
                        int(function.box[0]), int(function.box[1]), int(function.box[0] + function.box[2]), int(function.box[1] + function.box[3])
                    )
                )
            if function.type == "string":
                file.write("""        return self.tool.image_to_string(cropped, lang="eng", builder=pyocr.builders.TextBuilder())\n""")
            elif function.type == "number":
                file.write("        im = cropped.filter(ImageFilter.EDGE_ENHANCE_MORE)\n")
                file.write("        npcropped = numpy.array(im)[:, :, ::-1].copy()\n")
                file.write("        npcropped = cv2.resize(npcropped, (0,0), fx=3, fy=3)\n")
                file.write("        im = Image.fromarray(npcropped)\n")
                file.write("        im = im.convert('L')\n")
                file.write("        im = im.point(lambda x: 0 if x<100 else 255, '1')\n")
                file.write("""        return float(self.tool.image_to_string(im, lang="eng", builder=pyocr.builders.TextBuilder()))\n""")
            elif function.type == "position":
                file.write("""        image = cv2.("{}")\n""".format(function.image))
                file.write("        cropped = numpy.array(cropped)[:, :, ::-1].copy()\n")
                file.write("        \n")
                file.write("        res = cv2.matchTemplate(cropped, image, cv2.TM_CCOEFF_NORMED)\n")
                file.write("        threshold = 0.8\n")
                file.write("        loc = np.where( res >= threshold)\n")
                file.write("        return loc\n")
                file.write("\n")

            file.write("\n")

            file.write("")
            file.write("")
            file.write("")
            file.write("")

    @staticmethod
    def load_library(destination):
        directory = None
        functions = []
        with open(destination, 'r') as file:
            lines = file.readlines()
            i = 3
            while i < len(lines):
                print("line number {} has this text: {}".format(i, lines[i]))

                if len(lines[i])<4:
                    i += 1
                    continue
                else:
                    if lines[i][:3] == "# c":
                        class_data = ast.literal_eval(lines[i][4:])
                        directory = class_data["directory"]
                        print("Directory is {} . and we increased curent line to {}".format(directory, i))
                        i += 8
                    elif lines[i][:3] == "# f":
                        functions.append(eval(lines[i][4:]))
                        i += 2
                i += 1

        return directory, functions




