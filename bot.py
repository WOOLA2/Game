import time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def start_bot():
    set_bot_state(True)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.mulasport.co.ls/')

    time.sleep(3)
    driver.find_element(By.NAME, 'username').send_keys('59213666')
    driver.find_element(By.NAME, 'password').send_keys('123456')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(5)

    driver.get('https://www.mulasport.co.ls/aviator')
    time.sleep(5)

    while is_bot_running():
        try:
            history = get_crash_history(driver)
            if history and float(history[0]) < 1.10:
                place_bet(driver)
                wait_for_cashout(driver)
                wait_for_next_low(driver)
        except Exception:
            pass
        time.sleep(2)

    driver.quit()

def stop_bot():
    set_bot_state(False)

def set_bot_state(state: bool):
    with open('control_state.json', 'w') as f:
        json.dump({'running': state}, f)

def is_bot_running() -> bool:
    try:
        with open('control_state.json') as f:
            return json.load(f).get('running', False)
    except:
        return False

def get_crash_history(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'crash-value')
    return [e.text.replace('x','') for e in elements[:5]]

def place_bet(driver):
    driver.find_element(By.ID, 'bet-amount').clear()
    driver.find_element(By.ID, 'bet-amount').send_keys('5')
    driver.find_element(By.ID, 'place-bet-button').click()

def wait_for_cashout(driver):
    time.sleep(3)
    driver.find_element(By.ID, 'cashout-button').click()

def wait_for_next_low(driver):
    while is_bot_running():
        history = get_crash_history(driver)
        if history and float(history[0]) < 1.10:
            break
        time.sleep(1)
