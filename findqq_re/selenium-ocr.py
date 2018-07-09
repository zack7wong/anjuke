import time
from selenium import webdriver


url ='https://www.jianshu.com/p/7a4414082ce2'
print(str(time.strftime("%Y-%m-%d %X", time.localtime())))
driver = webdriver.PhantomJS()
print(str(time.strftime("%Y-%m-%d %X", time.localtime())))
# driver.set_window_size(1200, 900)
# driver.maximize_window()
# driver.get(url)
# print(driver.title)
# driver.close()
driver.get('http://newloveba.com/')

# js="document.documentElement.scrollTop=900"
# driver.execute_script(js)
#
# driver.execute_script("""
#         (function () {
#             var y = 0;
#             var step = 100;
#             window.scroll(0, 0);
#
#             function f() {
#                 if (y < document.body.scrollHeight) {
#                     y += step;
#                     window.scroll(0, y);
#                     setTimeout(f, 100);
#                 } else {
#                     window.scroll(0, 0);
#                     document.title += "scroll-done";
#                 }
#             }
#
#             setTimeout(f, 1000);
#         })();
#     """)
#
#

driver.save_screenshot('ocrr1.png')
driver.quit()