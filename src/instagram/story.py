from PIL import Image, ImageDraw, ImageFont
import os

class PostStory:
    def __init__(self,client,logger):
        self.cl = client
        self.logger = logger
        self.logger.info('logged in form post_story')

    def post_story(self, new_list):
        for li in new_list:
            img = Image.new(mode="RGBA", size=(720, 1280), color='black')
            draw = ImageDraw.Draw(img)
            count = 0

            if len(li) > 22:
                lines = [li[i:i+22] for i in range(0, len(li), 22)]
                text = "\n".join(lines)
                count += 1

            font_path = '../../fonts/Lora-Medium.ttf'
            abs_font_path = os.path.join(os.path.dirname(__file__), font_path)
            if count == 0:
                # font = ImageFont.truetype('fonts/Lora-Medium.ttf', 50)
                font = ImageFont.truetype(abs_font_path, 50)
            else:
                for i in range(count):
                    # font = ImageFont.truetype('fonts/Lora-Medium.ttf', 50 - (i*10))
                    font = ImageFont.truetype(abs_font_path, 50 - (i*10))

            text_bbox = draw.textbbox((0, 0), text, font=font)
            wd = text_bbox[2] - text_bbox[0]
            ht = text_bbox[3] - text_bbox[1]
            draw.text(((720-wd)/2, (1080-ht)/2), text, fill='white', font=font)

            automated_text = "Automated post"
            atmt_post_text_bbox = draw.textbbox((0, 0), automated_text, font=font)
            wd = atmt_post_text_bbox[2] - atmt_post_text_bbox[0]
            ht = atmt_post_text_bbox[3] - atmt_post_text_bbox[1]
            # font = ImageFont.truetype('fonts/Lora-Medium.ttf', 20)
            font = ImageFont.truetype(abs_font_path, 20)
            draw.text(((720-wd)*1.5, 1080-ht-30), automated_text, fill='white', font=font)

            notice_text = "NEW NOTIFICATION"
            notice_text_bbox = draw.textbbox((0, 0), notice_text, font=font)
            wd = notice_text_bbox[2] - notice_text_bbox[0]
            ht = notice_text_bbox[3] - notice_text_bbox[1]
            # font = ImageFont.truetype('fonts/Lora-Medium.ttf', 40)
            font = ImageFont.truetype(abs_font_path, 40)
            draw.text(((720-wd+50)/4, 250), notice_text, fill='white', font=font)

            img_dump_path = '../../images/dumps/insta_dump.png'
            abs_img_dump_path = os.path.join(os.path.dirname(__file__), img_dump_path)
            # img.save('images/dumps/insta_dump.png')
            img.save(abs_img_dump_path)
            # png_img = Image.open('images/dumps/insta_dump.png')
            png_img = Image.open(abs_img_dump_path)
            new_jpg_img_pth = '../../images/dumps/insta_dump.jpg'
            abs_new_jpg_img_pth = os.path.join(os.path.dirname(__file__), new_jpg_img_pth)
            # png_img.convert("RGB").save('images/dumps/insta_dump.jpg')
            png_img.convert("RGB").save(abs_new_jpg_img_pth)
            # path = 'images/dumps/insta_dump.jpg'
            # self.cl.photo_upload_to_story(path)
            self.cl.photo_upload_to_story(abs_new_jpg_img_pth)
            self.cl.delay_range = [2,5] #very very imp dont remove this if not it can post more than 30 stories in less than a second😀
            
            self.logger.info('story posted')
        return self.cl
