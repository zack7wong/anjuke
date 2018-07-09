from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.huihui.cn/login")

driver.maximize_window() # 最大化窗口
# driver.set_window_size(500,600)#设定固定大小
# broserwser.implicitly_wait(10)  #隐式等待100秒
frame = driver.find_element_by_id("x-URS-iframe")
driver.switch_to.frame(frame)
# driver.switch_to.frame(0)
driver.find_element_by_name("email").clear()
driver.find_element_by_name("email").send_keys("zbuhui@126.com")
driver.find_element_by_name("password").send_keys("yx102030")
driver.find_element_by_id("dologin").click()
assert "No results found." not in driver.page_source
driver.implicitly_wait(30)
driver.find_element_by_class_name('signup').click()
driver.implicitly_wait(50)
driver.find_element_by_class_name('lottery-btn').click()#name('node-type="signInBtn"')
# driver.get('http://www.huihui.cn/coupons/all?keyfrom=index.qiandao')
# driver.find_element_by_id('data-log="signIn.huajifen"').click()
cookies = driver.get_cookies()
driver.quit()
print(cookies)