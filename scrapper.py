from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

driver = Firefox()

driver.get('https://www.allrecipes.com/recipes/362/desserts/cookies/')
driver.maximize_window()

try: 
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@id='onetrust-reject-all-handler']"))
    )
    element.click()
except:
    print("Couldn't find the element")
    driver.quit()



# Cookies
# tax-sc__recirc-list_1-0
page_source = driver.page_source
driver.quit()
# print(driver.page_source)
# all_cookies = driver.find_elements(By.XPATH, "//button[@id='tax-sc__recirc-list_1-0']")

# for cookie in all_cookies:
#     print(cookie.text)


# driver.close()

soup = BeautifulSoup(page_source, 'html.parser')

print(soup.prettify())