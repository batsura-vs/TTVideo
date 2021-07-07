import cv2
from PIL import Image
import os


class MakeVideos:
    def __init__(self, filename):
        self.filename = filename

    def create(self):
        inp = Image.open(self.filename)
        inp_pix = inp.load()
        inp_width, inp_height = inp.size
        f_inp_width = round(inp_width / 3)
        inp_width = inp_width - (inp_width - f_inp_width * 3)
        im1 = Image.new('RGB', size=(round(inp_width / 3), inp_height), color='white')
        im1_pix = im1.load()

        im2 = Image.new('RGB', size=(round(inp_width / 3), inp_height), color='white')
        im2_pix = im2.load()

        im3 = Image.new('RGB', size=(round(inp_width / 3), inp_height), color='white')
        im3_pix = im3.load()

        for h in range(inp_height):
            for w in range(inp_width - 1):
                if w < f_inp_width:
                    im1_pix[w, h] = inp_pix[w, h]
                if f_inp_width * 2 > w > f_inp_width - (inp_width - f_inp_width * 3) - 1:
                    im2_pix[w - f_inp_width, h] = inp_pix[w, h]
                if w > f_inp_width * 2 - (inp_width - f_inp_width * 3) - 1:
                    im3_pix[w - f_inp_width * 2, h] = inp_pix[w, h]
        im1.save(f'3{self.filename}')
        im2.save(f'2{self.filename}')
        im3.save(f'1{self.filename}')
        ret = []
        for image in range(3, 0, -1):
            video = cv2.VideoWriter(f'{image}{self.filename}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1,
                                    (f_inp_width, inp_height))
            ret.append(f'{image}{self.filename}.mp4')
            for i in range(3):
                video.write(cv2.imread(f'{image}{self.filename}'))
            video.release()
            os.remove(f'{image}{self.filename}')
        return ret
