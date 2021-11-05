import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 自动刷新时间为120s
t=450
url = 'http://10.20.18.54:8080/'
# # 显示浏览器界面
driver = webdriver.Chrome('chromedriver.exe')

# 不显示浏览器界面
option=webdriver.ChromeOptions()
# option.add_argument('headless') # 设置option
# driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=option)

cookie = {
    'name': 'AIOHTTP_SESSION',
    'value':"gAAAAABhe9O-BZnXhiE7Zfc2Fai2ovxoZ3_AOuyqxbYrtjqR9pKg3K03S8bEOMi4AvcFrqI2zMGajgxipDKL-liYOTMAQD1dsptOMRhf9mszQkgHnxIEDiNafnzbKAgXnKwm1nPDEkO6YqVZffVMwS-NMZN9G3_ssg=="
}
cookie2 = {
    'name': 'io',
    'value':'d984ae4a6fec41cd81bc863e53a831db'
}
i = 1


def choose(seletor):
    try:
        choice = wait.until(EC.element_to_be_clickable((By.XPATH, seletor)))
        return choice
    except TimeoutException:
        print("Time out!")
        return None
    except Exception:
        print("Not found!")
        return None


while True:
    try:
        driver.get(url=url)
        wait = WebDriverWait(driver, 3)
        driver.add_cookie(cookie)
        driver.add_cookie(cookie2)
        driver.get(url)

        while True:
            btn = choose('/html/body/div[3]/div[1]/div/div/div[1]/div[1]/button')
            cnt = 0
            if not btn:
                try:
                    btn2 = choose('/html/body/div[3]/div[2]/div/div/div[3]/button')
                    btn2.click()
                except Exception:
                    alert = driver.switch_to.alert
                    time.sleep(5)
                    cnt += 1
                    alert_content = alert.text
                    print(alert_content)
                    alert.accept()
                    if cnt > 40: break
                    pass
                continue
            btn.click()
            print(time.localtime(time.time()))
            print('第{}次test'.format(i))
            print('score: ' + driver.find_element_by_xpath(
                '/html/body/div[3]/div[1]/div/div/div[2]/div[3]/table/tbody/tr[14]/td[3]/p').text)
            i += 1
            time.sleep(t)
    except Exception:
        continue
