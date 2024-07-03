from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(service=service, options=options)

url = 'https://www.geckoterminal.com/ru/ton/pools/EQCaY8Ifl2S6lRBMBJeY35LIuMXPc8JfItWG4tl7lBGrSoR2'

try:
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.price-display')))  # Adjust the selector as needed

    if price_element:
        print('Price:', price_element.text)
    else:
        print('Price element not found. Please check the page structure.')

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
