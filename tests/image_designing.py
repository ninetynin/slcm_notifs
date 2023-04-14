from PIL import Image, ImageDraw, ImageFont, ImageColor

img = Image.new(mode="RGBA", size=(720,1080), color='black')
draw = ImageDraw.Draw(img)

# First line text
text = 'REVISED TIMETABLE - SECOND SEMESTER B.TECH. IN-SEMESTER EXAMINATION - I (REMEDIAL SECTIONS)'

count = 0
if len(text) > 22:
    lines = [text[i:i+22] for i in range(0, len(text), 22)]
    text = "\n".join(lines)
    count += 1

if count == 0:
    font = ImageFont.truetype('fonts/Lora-Medium.ttf', 50)
else:
    for i in range(count):
        font = ImageFont.truetype('fonts/Lora-Medium.ttf', 50 - (i*10))

text_bbox = draw.textbbox((0, 0), text, font=font)
wd = text_bbox[2] - text_bbox[0]
ht = text_bbox[3] - text_bbox[1]
draw.text(((720-wd)/2, (1080-ht)/2), text, fill='white', font=font)

automated_post_text = 'Automated Post'
automated_post_text_bbox = draw.textbbox((0, 0), automated_post_text, font=font)
wd = automated_post_text_bbox[2] - automated_post_text_bbox[0]
ht = automated_post_text_bbox[3] - automated_post_text_bbox[1]
font = ImageFont.truetype('fonts/Lora-Medium.ttf', 20)
draw.text(((720-wd)*1.5, 1080-ht-30), automated_post_text, fill='white', font=font)

notice_text = 'NEW NOTIFICATION'
notice_text_bbox = draw.textbbox((0, 0), notice_text, font=font)
wd = notice_text_bbox[2] - notice_text_bbox[0]
ht = notice_text_bbox[3] - notice_text_bbox[1]
font = ImageFont.truetype('fonts/Lora-Medium.ttf', 40)
draw.text(((720-wd+50)/4, 250), notice_text, fill='white', font=font)

img.show()
img.save('images/dumps/insta_dump.png')
png_img = Image.open('images/dumps/insta_dump.png')
png_img.convert("RGB").save('images/dumps/insta_dump.jpg')    
path = 'images/dumps/insta_dump.jpg'
