import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
# from selenium.common.exceptions import TimeoutException

headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
for key, value in headers1.items():
    desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)

driver.set_window_size(1920, 1080)
driver.set_page_load_timeout(0.0000200)
driver.set_script_timeout(100)
url = 'https://cnblogs.com'
try:
    driver.get(url)
    driver.execute_script("""
            (function () {
                var y = 0;
                var step = 100;
                window.scroll(0, 0);

                function f() {
                    if (y < document.body.scrollHeight) {
                        y += step;
                        window.scroll(0, y);
                        setTimeout(f, 100);
                    } else {
                        window.scroll(0, 0);
                        document.title += "scroll-done";
                    }
                }

                setTimeout(f, 1000);
            })();
        """)
    for i in range(30):
        if "scroll-done" in driver.title:
            break
        time.sleep(6)
    print('selenium save png')
# except Exception as e:
#     print(e)
except TimeoutException:
    driver.execute_script('window.stop()')
    print('超时,wiindow stop')
# driver.save_screenshot('1231.png')
# driver.quit()