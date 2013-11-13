#coding=utf-8
from windows import get_icon

__author__ = 'ron975'
import math

from PIL import Image, ImageChops


def check_icon(exe, icon):
    exe_icon = get_icon(exe)
    if not exe_icon:
        return False
    exe_icon = transparency_to_white(exe_icon)
    desura_icon = transparency_to_white(Image.open(icon))
    if rmsdiff(desura_icon, exe_icon) > 20:
        return False
    return True


def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    h = ImageChops.difference(im1, im2).histogram()
    # calculate rms
    return math.sqrt(sum(h*(i**2) for i, h in enumerate(h))) / (float(im1.size[0]) * im1.size[1])


def transparency_to_white(image):
    try:
        background = Image.new('RGB', image.size, (255, 255, 255))
        background.paste(image.convert('RGB'), mask=image)
        return background.convert('RGB')
    except ValueError:
        return image.convert('RGB')

def choose_icon(game):
    """
    Decides what icon to use when inserting into Steam.
    :param game:
    :return:
    """
    icon = game.icon
    if game.icon.lower().endswith("jpeg") or game.icon.lower().endswith("jpg"):
        Image.open(game.icon).save(game.icon+".png")
        icon += ".png"
    if check_icon(game.exe, game.icon):
        icon = ""
    return icon