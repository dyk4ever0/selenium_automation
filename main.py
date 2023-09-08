from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import os

app = Flask(__name__)

def fetch_email(name, employee_id):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://www.bearworld.co.kr/share/page/user-portal-main")

    driver.find_element(By.ID, "j_username").send_keys("dyk43e")
    driver.find_element(By.ID, "j_password").send_keys("Qlalf13!")
    driver.find_element(By.CSS_SELECTOR, "input.loginBtn").click()

    wait = WebDriverWait(driver, 10)
    org_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "조직도")))
    org_link.click()

    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.ID, "keyword").send_keys(employee_id)
    driver.find_element(By.ID, "keyword").send_keys(Keys.ENTER)
    time.sleep(10)

    found = False
    elements = driver.find_elements(By.CSS_SELECTOR, ".userName.tooltip")
    for element in elements:
        if name in element.text:
            element.click()
            found = True
            break

    if not found:
        return '-'

    time.sleep(5)

    try:
        email_script = driver.find_element(By.CSS_SELECTOR, ".email").get_attribute("onclick")
        email_address = email_script.split("'")[3]
        return email_address
    except:
        return '-'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/fetch_email", methods=["POST"])
def get_email():
    data = request.json
    name = data.get("name")
    employee_id = data.get("employee_id")

    email_address = fetch_email(name, employee_id)

    return jsonify({"email_address": email_address})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
