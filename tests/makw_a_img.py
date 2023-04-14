from PIL import Image, ImageDraw, ImageFont, ImageColor


img = Image.new(mode="RGBA", size=(720,1080), color='black')
# img.show()


text = 'hello'

font = ImageFont.truetype('arial.ttf', 50)

ht, wd = draw.textsize(text, font=font)


img.show()