from PIL import Image


filename='ocr1.png'
# f1, f2 = os.path.splitext(filename)
# print(f1,f2)
image= Image.open(filename)

gray = image.convert('L')
#图像对象转化（L：8位像素，表示黑和白）
#可以参考：Python图像处理库PIL的基本概念介绍 - icamera0的博客 - CSDN博客
bw = gray.point(lambda x:0 if x<140 else 255,'1')#如果RGB数值小于140的变成1，否则是255。也就是将验证码背景变成白色，具体字符变成黑色。
bw.save('ocr2.png')