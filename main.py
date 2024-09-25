import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    main_request_taxi_button = (By.XPATH, "//button[contains(., 'Pedir un taxi')]") #First request button to start taxi request in main form
    main_comfort_rate = (By.CSS_SELECTOR, "div.tcard-icon img[alt='Comfort']") #Comfort rate selector in main form
    main_comfort_reqs = (By.CLASS_NAME, "r-sw-label") #Requirements selectors in main form
    main_phone_field = (By.CSS_SELECTOR, ".np-button") #Phone field in main form
    phone_number_input =(By.ID, "phone") #Phone number input in pop-up form
    phone_next_button = (By.XPATH, "//button[contains(., 'Siguiente')]") #"Siguiente" button in pop-up form
    phone_code_field = (By.ID, "code") #Code field in pop-up form
    confirm_phone_code = (By.XPATH, "//button[contains(., 'Confirmar')]") #Confirm button in pop-up form
    main_payment_field = (By.CLASS_NAME, "pp-value") #Payment field in main form
    add_card_for_payment = (By.XPATH, "//div[@class='pp-selector']/div[contains(., 'Agregar tarjeta')]") #Add card button in pop-up form
    card_number = (By.ID, "number") #Card number input in pop-up form
    card_code = (By.NAME, "code") #Card code input in pop-up form
    add_card_button = (By.XPATH, "//button[contains(., 'Agregar')]") #Add button in pop-up form
    close_payment_method = (By.XPATH, "//div[@class = 'payment-picker open']//div[@class= 'section active']/button") #Close button in pop-up form
    message_for_driver = (By.ID, "comment") #Message for driver field
    manta_selector = (By.XPATH, "//*[@class='r-sw-container'][contains(., 'Manta y pañuelos')]//*[@class='switch']") #Manta y pañuelos clickable checkbox
    manta_selector_status = (By.XPATH, "//*[@class='r-sw-container'][contains(., 'Manta y pañuelos')]//*[@type='checkbox']") #Manta y pañuelos checkbox status locator
    ice_cream_plus = (By.XPATH,"//*[@class='r-counter-container'][contains(., 'Helado')]//*[@class='counter-plus']") #Icecream plus selector
    ice_cream_value = (By.XPATH,"//*[@class='r-counter-container'][contains(., 'Helado')]//*[@class='counter-value']") #Icecream count value
    final_request_taxi_button = (By.CLASS_NAME,"smart-button-main") #Blue button to place the request for a taxi
    cancel_taxi_button = (By.CSS_SELECTOR,"img[alt='close']") #Cancel taxi button in pop-up window
    detail_order_button = (By.CSS_SELECTOR, "img[alt='burger']")
    order_number = (By.CLASS_NAME, "number")  #Order number for taxi request

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address): #Fills from field
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address): #Fills to field
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self): #Gets value in from field
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self): #Gets value in to field
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self): #Fills from and to fields
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.from_field))
        self.set_from(data.address_from)
        self.set_to(data.address_to)

    def click_request_taxi_button(self): #Waits and clicks the request taxi button
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.main_request_taxi_button))
        self.driver.find_element(*self.main_request_taxi_button).click()

    def click_comfort_rate(self): #Waits and clicks comfort rate from the list
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.main_comfort_rate))
        self.driver.find_element(*self.main_comfort_rate).click()

    def verify_comfort_is_selected(self): #Verifies comfort rate is selected by checking a requirement
        return self.driver.find_elements(By.XPATH, *self.main_comfort_reqs).text()

    def set_phone_number(self): #Sets and validates phone number
        self.driver.find_element(*self.main_phone_field).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_number_input))
        self.driver.find_element(*self.phone_number_input).send_keys(data.phone_number)
        self.driver.find_element(*self.phone_next_button).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_code_field))
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.phone_code_field).send_keys(code)
        self.driver.find_element(*self.confirm_phone_code).click()

    def get_phone_number(self): #Gets phone number in field
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.main_phone_field))
        return self.driver.find_element(*self.main_phone_field)

    def add_credit_card(self): #Adds a card as payment method
        self.driver.find_element(*self.main_payment_field).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.add_card_for_payment))
        self.driver.find_element(*self.add_card_for_payment).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.card_number))
        self.driver.find_element(*self.card_number).send_keys(data.card_number)
        self.driver.find_element(*self.card_code).send_keys(data.card_code)
        self.driver.find_element(*self.card_number).click()
        self.driver.find_element(*self.add_card_button).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.add_card_for_payment))
        self.driver.find_element(*self.close_payment_method).click()

    def get_payment_type(self): #Gets payment method selected
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.main_payment_field))
        return self.driver.find_element(*self.main_payment_field)

    def set_message_for_driver(self): #Sets message for driver
        self.driver.find_element(*self.message_for_driver).send_keys(data.message_for_driver)

    def get_message_for_driver(self): #Gets message for driver in field
        return self.driver.find_element(*self.message_for_driver).get_property('value')

    def click_manta_selector(self): #Clicks Manta y pañuelos selector
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.manta_selector))
        selector = self.driver.find_element(*self.manta_selector)
        self.driver.execute_script("arguments[0].scrollIntoView();",selector) #Scrolls window until selector is visible
        self.driver.find_element(*self.manta_selector).click()

    def get_manta_selector(self): #Gets the status of Manta y pañuelos checkbox
        manta_selector = self.driver.find_element(*self.manta_selector_status).is_selected()
        return manta_selector

    def set_2_icecream(self): #Adds 2 icecream to the request
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.ice_cream_plus))
        selector = self.driver.find_element(*self.ice_cream_plus)
        self.driver.execute_script("arguments[0].scrollIntoView();",selector)  # Scrolls window until counter is visible
        for i in range(2):
            selector.click()

    def get_icecream_value(self): #Gets the value in the icecream count
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.ice_cream_value))
        return self.driver.find_element(*self.ice_cream_value).text

    def click_request_taxi(self): #Clicks request taxi blue button
        self.driver.find_element(*self.final_request_taxi_button).click()

    def verify_taxi_request(self): #Verifies the request was placed and the user is waiting
        WebDriverWait(self.driver,3).until(expected_conditions.element_to_be_clickable(self.cancel_taxi_button))
        return True

    def get_taxi_info(self): #Confirms a taxi was requested and an order number was created
        WebDriverWait(self.driver, 40).until(expected_conditions.visibility_of_element_located(self.order_number))
        return True


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    def test_set_route(self):   #Test to set address from and address to in Urban Routes form
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort_rate(self): #Test to request a taxi and select Comfort rate
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.set_phone_number()
        phone_number = routes_page.get_phone_number().text
        assert phone_number == data.phone_number #Verifies the phone number was added successfully

    def test_add_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.add_credit_card()
        payment_method = routes_page.get_payment_type().text
        assert payment_method == "Tarjeta", "Se seleccionó pago en efectivo" #Confirms the payment method is a credit card

    def test_set_message_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.set_message_for_driver()
        msg_for_driver = routes_page.get_message_for_driver()
        assert msg_for_driver == data.message_for_driver

    def test_set_manta_selector(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.click_manta_selector()
        manta_selector_status = routes_page.get_manta_selector()
        assert manta_selector_status

    def test_set_2_icecream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.set_2_icecream()
        ice_cream_value = routes_page.get_icecream_value()
        assert ice_cream_value == "2" #Verifies 2 icecream were added

    def test_request_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.set_phone_number()
        phone_number = routes_page.get_phone_number().text
        assert phone_number == data.phone_number
        routes_page.click_request_taxi()
        modal = routes_page.verify_taxi_request()
        assert modal == True #Verifies the request for a taxi was made

    def test_get_driver_info(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route()
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.set_phone_number()
        phone_number = routes_page.get_phone_number().text
        assert phone_number == data.phone_number
        routes_page.add_credit_card()
        payment_method = routes_page.get_payment_type().text
        assert payment_method == "Tarjeta", "Se seleccionó pago en efectivo"
        routes_page.set_message_for_driver()
        msg_for_driver = routes_page.get_message_for_driver()
        assert msg_for_driver == data.message_for_driver
        routes_page.click_request_taxi()
        modal = routes_page.verify_taxi_request()
        assert modal == True
        taxi_info = routes_page.get_taxi_info()
        assert taxi_info == True #Confirms a driver is assigned to the request

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
