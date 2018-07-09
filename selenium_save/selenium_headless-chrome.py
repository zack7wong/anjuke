#chrome 无头浏览器需要60以上版本
from selenium import webdriver
desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()

options = webdriver.ChromeOptions() # 创建chrome参数对象
options.add_argument('headless')   # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
# options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(chrome_options=options,desired_capabilities=desired_capabilities)# 创建chrome无界面对象
driver.get('https://www.cnblogs.com/')
driver.save_screenshot('cn.png')

# print(driver.page_source)
print("--finish--")
driver.quit()