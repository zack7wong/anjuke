from openpyxl import Workbook
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaiduResultPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['百度收录量', '搜狗收录量', '百度权重_站长', '建站时间', '百度权重_爱站', '360综合权重', '360收录量', '网站标题', '网站url','百度快照日期'])  # 设置表头
        self.driver = webdriver.PhantomJS()
        self.driver.get('http://www.link114.cn/')
        self.wait = WebDriverWait(self.driver, 15)
        # print(111, '选框')
        try:
            # 360收录量
            if self.driver.find_element_by_xpath("//*[@id='chk_so360_sl']").is_selected() is not True:
                # 判断360收录量是否选中
                # print(111)
                self.driver.find_element_by_xpath("//span[contains(text(),'360收录量')]").click()
                # print(222)
                # print(self.driver.find_element_by_xpath("//*[@id='chk_so360_sl']").is_selected())

            # 百度综合权重 - Chinaz数据源
            if self.driver.find_element_by_xpath("//*[@id='chk_baidu_qz_zz']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(@title,'百度综合权重 - Chinaz数据源')]")
                element.click()

            # 百度综合权重 - 爱站数据源  chk_baidu_qz_ai
            if self.driver.find_element_by_xpath("//*[@id='chk_baidu_qz_ai']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(@title,'百度综合权重 - 爱站数据源')]")
                element.click()

            # 360综合权重
            if self.driver.find_element_by_xpath("//*[@id='chk_so360_qz_zz']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(@title,'360综合权重')]")
                element.click()

            # 360收录量 chk_so360_sl
            if self.driver.find_element_by_xpath("//*[@id='chk_so360_sl']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(text(),'360收录量')]")
                element.click()
            # 搜狗收录量;
            if self.driver.find_element_by_xpath("//*[@id='chk_sogou_sl']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(text(),'搜狗收录量')]")
                element.click()
            # 建站时间
            if self.driver.find_element_by_xpath("//*[@id='chk_createdtime']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(text(),'建站时间')]")
                element.click()

            # 网站标题
            if self.driver.find_element_by_xpath("//*[@id='chk_title']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(text(),'网站标题')]")
                element.click()

            # 百度快照日期
            if self.driver.find_element_by_xpath("//*[@id='chk_baidu_kz']").is_selected() is not True:
                element = self.driver.find_element_by_xpath("//span[contains(text(),'百度快照日期')]")
                element.click()

        except Exception as e:
            print(e)
        # print(111, '完成选择')

    def process_item(self, item, spider):

        self.driver.find_element_by_xpath('//span[@id="clear"]').click()
        # 填入待查询网址
        # print(item['real_url'],'<<<待查询网址')
        self.driver.find_element_by_id("ip_websites").send_keys(item['real_url'])
        # 提交网址
        self.driver.find_element_by_id("tj").click()
        time.sleep(6)

        # 获取数据
        print('提取数据')
        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='baidu_sl']")
        # item['百度收录量'] = element.get_attribute("value")

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='baidu_sl']")))
        item['百度收录量'] = dragger.get_attribute("value")

        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='sogou_sl']")
        # item['搜狗收录量'] = element.get_attribute("value")

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='sogou_sl']")))
        item['搜狗收录量'] = dragger.get_attribute("value")


        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='baidu_qz_zz']")
        # item['百度权重_站长'] = element.get_attribute("value")

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='baidu_qz_zz']")))
        item['百度权重_站长'] = dragger.get_attribute("value")

        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='createdtime']")
        # item['建站时间'] = element.get_attribute("value")
        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='createdtime']")))
        item['建站时间'] = dragger.get_attribute("value")

        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='baidu_qz_ai']")
        # item['百度权重_爱站'] = element.get_attribute("value")

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='baidu_qz_ai']")))
        item['百度权重_爱站'] = dragger.get_attribute("value")

        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='so360_qz_zz']")
        # item['360综合权重'] = element.get_attribute("value")

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='so360_qz_zz']")))
        item['360综合权重'] = dragger.get_attribute("value")
        #
        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='so360_sl']")
        # item['360收录量'] = element.get_attribute("value")

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='so360_sl']")))
        item['360收录量'] = dragger.get_attribute("value")

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='title']")))
        item['网站标题'] = dragger.text

        dragger = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//td[@classname='baidu_kz']")))
        item['百度快照日期'] = dragger.text

        # element = self.driver.find_element_by_xpath("//tbody//td[@classname='baidu_kz']")
        # item['百度快照日期'] = element.get_attribute("value")

        print(item,'<<')
        line = [item['百度收录量'], item['搜狗收录量'], item['百度权重_站长'],
                item['建站时间'],item['百度权重_爱站'], item['360综合权重'],
                item['360收录量'], item['网站标题'],item['real_url'],item['百度快照日期']]

        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('/home/python/Desktop/a.xlsx')
        print("                     save ok!")

        return item



    def __del__(self):

        self.driver.quit()


