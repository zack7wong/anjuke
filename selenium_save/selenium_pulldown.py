import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()

driver.set_window_size(1920, 1080)
driver.set_page_load_timeout(0.00200)

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
except TimeoutException:
    driver.execute_script('window.stop()')
    print('超时,wiindow stop')
# driver.save_screenshot('1231.png')
finally:
    driver.quit()