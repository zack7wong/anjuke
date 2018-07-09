import os
from PIL import Image
# 利用image切割图片
# path = os.path.join(os.getcwd(),"x1.png")
Image.MAX_IMAGE_PIXELS = 300000000  # 提高触发警告的阈值，继而强制加载


class Cutting:
    def __init__(self):
        print('切图')
        # print(img.format)        # PNG
        # 宽 img.size[0] 高 img.size[1] #(1920, 16000)

    def cut_image(self, path):
        img = Image.open(path)
        #  png_name = url_md5 + '.png'
        md5 = path.split('.')[0]
        png_list = []
        if img.size[1] < 2000:
            png_name = path
            if int(os.path.getsize(png_name)/1000) > 30:
                png_list.append(png_name)
                return png_list
            else:
                return []
        else:
            n = img.size[1]//2000  # 多的最后一截丢弃
            if n <= 75:
                for num in range(1, n+1):
                    small_png = str(num)+'_'+md5+'.png'
                    img.crop((0, 2000*(num - 1), 1920, 2000*num)).save(small_png)
                    if int(os.path.getsize(small_png)/1000) > 30:
                        png_list.append(small_png)
                    else:
                        os.remove(small_png)
                return png_list
            else:
                print('图片太大')
                return []




if __name__ == '__main__':
    cutting = Cutting()
    l =cutting.cut_image('123.png')
    print(l)


