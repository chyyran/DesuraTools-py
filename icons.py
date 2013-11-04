#coding=utf-8
__author__ = 'ron975'
import math
import operator

from PIL import Image, ImageChops, ImageMath
import installedgames
import wx

def check_icon(exe, icon):
    app = wx.App(False) #Hacky hack is hacky.
    try:
        exe_bmp = wx.BitmapFromIcon(wx.IconFromLocation(wx.IconLocation(exe, 0))).ConvertToImage()
        exe_icon = transparency_to_white(PilImageFromWxImage(exe_bmp))
        exe_icon.save("exe_icon.png")
    except wx.PyAssertionError:
        return False
    desura_icon = transparency_to_white(Image.open(icon))
    desura_icon.save("desura_icon.png")
    if rmsdiff(desura_icon, exe_icon) > 20:
        return False


def PilImageFromWxImage(wxImage, keepTransp=True, createTransp=False, debug=False):

    """
    2 ==> 3

    Default preserves any transparency.

ERROR: EOF in multi-line string
    """

    # These can never be simultaneous.
    hasMask  = wxImage.HasMask()
    hasAlpha = wxImage.HasAlpha()
    if debug :
        print '>>>>  PilImageFromWxImage():  Input Image has Alpha'

    # Always convert a mask into an aplha layer.
    # Deal with keeping or discarding this alpha later on.
    if hasMask :    # Is always mutually exclusive with hasAlpha.

        if debug :
            print '>>>>  PilImageFromWxImage():  Converting Input Image Mask to Alpha'

        wxImage.InitAlpha()     # Covert the separate mask to a 4th alpha layer.
        hasAlpha = True

    #end if

    image_size = wxImage.GetSize()      # All images here have the same size.

    # Create an RGB pilImage and stuff it with RGB data from the wxImage.
    pilImage = Image.new( 'RGB', image_size )
    pilImage.fromstring( wxImage.GetData() )

    # May need the separated planes if an RGBA image is needed. later.
    r_pilImage, g_pilImage, b_pilImage = pilImage.split()

    if hasAlpha :

        if keepTransp : # Ignore createTransp - has no meaning

            if debug :
                print '>>>>  PilImageFromWxImage():  Keeping Transparency'

            # Must recompose the pilImage from 4 layers.
            r_pilImage, g_pilImage, b_pilImage = pilImage.split()

            # Create a Black L pilImage and stuff it with the alpha data
            #   extracted from the alpha layer of the wxImage.
            pilImage_L = Image.new( 'L', image_size )
            pilImage_L.fromstring( wxImage.GetAlphaData() )

            # Create an RGBA PIL image from the 4 layers.
            pilImage = Image.merge( 'RGBA', (r_pilImage, g_pilImage, b_pilImage, pilImage_L) )

        elif (not keepTransp) :

            # The RGB pilImage can be returned as it is now.
            if debug :
                print '>>>>  PilImageFromWxImage():  Returning an RGB PIL Image.'

        #end if

    elif (not hasAlpha) and createTransp :      # Ignore keepTransp - has no meaning

        if debug :
            print '>>>>  PilImageFromWxImage():  Creating a New Transparency Layer'

        # Create a Black L mode pilImage. The resulting image will still
        #  look the same, but will allow future transparency modification.
        pilImage_L = Image.new( 'L', image_size )

        # Create an RGBA pil image from the 4 bands.
        pilImage = Image.merge( 'RGBA', (r_pilImage, g_pilImage, b_pilImage, pilImage_L) )

    #end if

    return pilImage

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


game = installedgames.get_games()[2]
print game.exe
print game.icon
check_icon(game.exe,game.icon)