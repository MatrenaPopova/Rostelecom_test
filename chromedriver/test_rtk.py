import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.get('https://b2c.passport.rt.ru/auth/')
    driver.maximize_window()
    yield driver
    driver.quit()


def test_auth_valid_mail(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим адрес электронной почты
    driver.find_element(By.ID, 'username').send_keys('_________@gmail.com')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('__________')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.CSS_SELECTOR, '#app > main > div > div.home > div.base-card.home__info-card > div.user-info.home__user-info > div.user-info__name-container > h2 > span.user-name__last-name').text == 'Попова'


def test_auth_with_invalid_value(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим некорректный адрес электронной почты
    driver.find_element(By.ID, 'username').send_keys('________@gmail.com')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('_______')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что система написала "Неверный логин или пароль"
    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


def test_auth_tab_changed_to_mail(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим адрес электронной почты
    driver.find_element(By.ID, 'username').send_keys('____________@gmail.com')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('__________')
    # проверяем, что система поменяла таб аутентификации с телефона на почту
    assert driver.find_element(By.CSS_SELECTOR, 'div[class*=rt-tab--active]').text == 'Почта'
    print('тест прошел')


def test_auth_tab_changed_to_login(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим логин
    driver.find_element(By.ID, 'username').send_keys('_________')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('__________')
    # проверяем, что система поменяла таб аутентификации с телефона на почту
    assert driver.find_element(By.CSS_SELECTOR, 'div[class*=rt-tab--active]').text == 'Логин'
    print('тест прошел')


def test_auth_tab_changed_to_ls(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим номер лицевого счета
    driver.find_element(By.ID, 'username').send_keys('_________')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('________')
    # проверяем, что система не поменяла таб аутентификации с телефона на лицевой счет
    slovo = driver.find_element(By.CSS_SELECTOR, 'div[class*=rt-tab--active]').text
    slovo_ls = 'Лицевой счёт'
    assert slovo == slovo_ls, f'Тест не прошел, вот что написано {slovo}'

def test_knopka_zabuli_parol(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'forgot_password').click()
    assert driver.find_element(By.CSS_SELECTOR, 'h1[class*=card-container__title]').text == 'Восстановление пароля'


def test_knopka_pomoshi_FAQ(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'faq-open').click()
    assert driver.find_element(By.CSS_SELECTOR, 'h1[class*=faq-modal__title]').text == 'Ваш безопасный ключ к сервисам Ростелекома'


def test_knopka_zaregistrirovatsia(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'kc-register').click()
    time.sleep(10)
    assert driver.find_element(By.CSS_SELECTOR, 'h1[class*=card-container__title]').text == 'Регистрация'


def test_knopka_vernutsia_nazad_vosstan_parolia(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    driver.find_element(By.ID, 'forgot_password').click()
    driver.find_element(By.ID, 'reset-back').click()
    assert driver.find_element(By.CSS_SELECTOR, 'h1[class*=card-container__title]').text == 'Авторизация'


def test_auth_valid_ls(driver):
    wdw(driver, 5).until(EC.presence_of_element_located((By.ID, 'username')))
    # переводим таб аутентификации на вход по лицевому счету
    driver.find_element(By.ID, 't-btn-tab-ls').click()
    time.sleep(2)
    # вводим номер лицевого счета
    driver.find_element(By.ID, 'username').send_keys('____________')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('____________')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.CSS_SELECTOR, 'h3[class*=card-title]').text == 'Учетные данные'


def test_auth_with_invalid_ls_value(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # переводим таб аутентификации на вход по лицевому счету
    driver.find_element(By.ID, 't-btn-tab-ls').click()
    time.sleep(2)
    # вводим некорректный номер лицевого счета
    driver.find_element(By.ID, 'username').send_keys('________')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('_______')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что система написала "Неверный логин или пароль"
    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


def test_auth_valid_phone(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим номер телефона
    driver.find_element(By.ID, 'username').send_keys('_________')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('_________')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.CSS_SELECTOR, 'h3[class*=card-title]').text == 'Учетные данные'


def test_auth_with_invalid_phone_value(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим некорректный номер телефона
    driver.find_element(By.ID, 'username').send_keys('_______')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('_________')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что система написала "Неверный логин или пароль"
    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'


def test_auth_valid_login(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим логин
    driver.find_element(By.ID, 'username').send_keys('_________')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('_______')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.CSS_SELECTOR, 'h3[class*=card-title]').text == 'Учетные данные'


def test_auth_with_invalid_login(driver):
    wdw(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    # вводим некорректный логин
    driver.find_element(By.ID, 'username').send_keys('________')
    # вводим пароль
    driver.find_element(By.ID, 'password').send_keys('_______')
    # нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, '#kc-login').click()
    # проверяем, что система написала "Неверный логин или пароль"
    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

