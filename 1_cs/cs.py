from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import PIL.Image as image
import time, re, random
import urllib.request
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector


def get_merge_image(filename, location_list):
    '''
    根据位置对图片进行合并还原
    :filename:图片
    :location_list:图片位置
    '''
    pass

    im = image.open(filename)

    new_im = image.new('RGB', (260, 116))

    im_list_upper = []
    im_list_down = []

    for location in location_list:

        if location['y'] == -58:
            pass
            im_list_upper.append(im.crop((abs(location['x']), 58, abs(location['x']) + 10, 166)))
        if location['y'] == 0:
            pass

            im_list_down.append(im.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))

    new_im = image.new('RGB', (260, 116))

    x_offset = 0
    for im in im_list_upper:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    x_offset = 0
    for im in im_list_down:
        new_im.paste(im, (x_offset, 58))
        x_offset += im.size[0]

    return new_im


def get_image(driver, div):
    '''
    下载并还原图片
    :driver:webdriver
    :div:图片的div
    '''

    # 找到图片所在的div
    background_images = driver.find_elements_by_xpath(div)
    location_list = []
    imageurl = ''
    for background_image in background_images:
        location = {}

        # 在html里面解析出小图片的url地址，还有长高的数值
        location['x'] = int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                                       background_image.get_attribute('style'))[0][1])
        location['y'] = int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                                       background_image.get_attribute('style'))[0][2])
        imageurl = re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",
                              background_image.get_attribute('style'))[0][0]

        location_list.append(location)

    imageurl = imageurl.replace("webp", "jpg")

    jpgfile = BytesIO(urllib.request.urlopen(imageurl).read())
    # 重新合并图片
    image = get_merge_image(jpgfile, location_list)

    return image



def is_similar(image1, image2, x, y):
    '''
    对比RGB值
    '''
    # 获取指定位置的RGB值
    pixel1 = image1.getpixel((x, y))
    pixel2 = image2.getpixel((x, y))
    # 如果相差超过80则就认为找到了缺口的位置
    for i in range(0, 3):
        if abs(pixel1[i] - pixel2[i]) >= 80:
            return False
    return True


def get_diff_location(image1, image2):
    '''
    计算缺口的位置
    '''

    i = 0
    # 两张原始图的大小都是相同的260*116
    # 那就通过两个for循环依次对比每个像素点的RGB值
    # 如果相差超过50则就认为找到了缺口的位置
    for i in range(0, 260):
        for j in range(0, 116):
            if is_similar(image1, image2, i, j) == False:
                return i


def get_track(length):
    '''
    根据缺口的位置模拟x轴移动的轨迹
    '''
    list = []
    # 间隔通过随机范围函数来获得,每次移动一步或者两步
    x = random.randint(1, 3)

    while length - x >= 5:
        list.append(x)
        length = length - x
        x = random.randint(1, 3)
    # 最后五步都是一步步移动
    for i in range(length):
        list.append(1)
    return list


def main(keywords):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 30)

    driver.get("http://xygs.egs.gov.cn/index.jspx")
    input = wait.until(EC.presence_of_element_located((By.ID, 'searchText')))
    input.send_keys(keywords)
    time.sleep(2)
    button = driver.find_element_by_id("click")
    button.click()

    #     等待页面的上元素刷新出来
    WebDriverWait(driver, 30).until(
        lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']").is_displayed())
    WebDriverWait(driver, 30).until(
        lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_bg gt_show']").is_displayed())
    WebDriverWait(driver, 30).until(
        lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_fullbg gt_show']").is_displayed())

    #     下载图片
    image1 = get_image(driver, "//div[@class='gt_cut_bg gt_show']/div")
    image2 = get_image(driver, "//div[@class='gt_cut_fullbg gt_show']/div")

    #     计算缺口位置
    loc = get_diff_location(image1, image2)

    #     生成x的移动轨迹点
    track_list = get_track(loc)

    #     找到滑动的圆球
    element = driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
    location = element.location
    #     获得滑动圆球的高度
    y = location['y']

    #     鼠标点击元素并按住不放
    print("第一步,点击元素")
    ActionChains(driver).click_and_hold(on_element=element).perform()
    time.sleep(0.15)

    print("第二步，拖动元素")
    track_string = ""
    for track in track_list:
        track_string = track_string + "{%d,%d}," % (track, y - 445)
        #         xoffset=track+22:这里的移动位置的值是相对于滑动圆球左上角的相对值，而轨迹变量里的是圆球的中心点，所以要加上圆球长度的一半。
        #         yoffset=y-445:这里也是一样的。不过要注意的是不同的浏览器渲染出来的结果是不一样的，要保证最终的计算后的值是22，也就是圆球高度的一半
        ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=track + 22,
                                                         yoffset=y - 445).perform()
        #         间隔时间也通过随机函数来获得
        time.sleep(random.randint(10, 50) / 1000)
    print(track_string)
    #     退了5格， 圆球的位置和滑动条的左边缘有5格的距离
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y - 445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y - 445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y - 445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y - 445).perform()
    time.sleep(0.1)
    ActionChains(driver).move_to_element_with_offset(to_element=element, xoffset=21, yoffset=y - 445).perform()

    print("第三步，释放鼠标")
    #     释放鼠标
    ActionChains(driver).release(on_element=element).perform()

    # 显示等待， 到页面跳转到含有这个标签的html页面时触发
    try:
        icount = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'searchtipsu1')))
        if icount:
            print('一共搜到到{}条企业信息'.format(icount))
        else:
            print('未搜索到该关键词所包含的企业')
            time.sleep(2)
            driver.quit()
    except Exception as e:
        print('验证码失败，重启中...')
        main(k)
    # 获取页面html文件
    else:
        page_html = driver.page_source

        # 使用Scrapy的Selector包， 它是基于lxml的c语言编写的库，速度更快。注意这里Selector(text=)参数名不能省略。
        info_counts = Selector(text=page_html).xpath("//div[@id='searchtipsu1']/p/span[2]/text()").extract_first()
        print(info_counts)

        a_list = Selector(text=page_html).xpath("//div[@id='contentitem']/div")

        # 获取公司列表
        for a in a_list:
            item = {}
            item['company_id'] = a.xpath("//div[@id='contentitem']/div/@data-label").extract_first()
            item['company_urls'] = "http://xygs.egs.gov.cn/company/detail.jspx?id={}&jyzk=jyzc".format(
                item['company_id'])
            company_name = a.xpath(".//span[@class='qiyeEntName']")
            item['company_name'] = company_name.xpath("string(.)").extract_first().strip()
            print(item)

        time.sleep(3)

        driver.quit()

if __name__ == '__main__':
    main('武汉萨达')
