import data
from selenium import webdriver
#from selenium.webdriver import Keys
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
    request_taxi_button = (By.XPATH, "//button[contains(., 'Pedir un taxi')]")
    comfort_rate = (By.CSS_SELECTOR, "div.tcard-icon img[alt='Comfort']")
    comfort_reqs = (By.CLASS_NAME,"r-sw-label")
    phone_field = (By.CSS_SELECTOR, ".np-button") #phone field in main list
    phone_number_input =(By.ID, "phone")
    phone_next_button = (By.XPATH, "//button[contains(., 'Siguiente')]")
    phone_code_field = (By.ID, "code") #probar a ver si no da error con codigo de tarjeta
    confirm_phone_code = (By.XPATH, "//button[contains(., 'Confirmar')]")
    payment_field = (By.CLASS_NAME, "pp-button")

    def __init__(self, driver):
        self.driver = driver

    def wait_for_home_page(self): #Waits 3 sec until Comfort is visible in the list
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.from_field))

    def set_from(self, from_address): #Fills from field
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address): #Fills to field
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self): #Gets value in from field
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self): #Gets value in to field
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address): #Fills from and to fields
        self.set_from(from_address)
        self.set_to(to_address)

    def click_request_taxi_button(self): #Clicks the request taxi button
        self.driver.find_element(*self.request_taxi_button).click()

    def wait_for_request_taxi_button(self): #Waits until taxi button is visible
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.request_taxi_button))

    def wait_for_load_comfort_rate(self): #Waits 3 sec until Comfort is displayed in the list
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.comfort_rate))

    def click_comfort_rate(self): #Selects comfort rate from the list
        self.driver.find_element(*self.comfort_rate).click()

    def verify_comfort_is_selected(self): #Verifies comfort rate is selected by checking a requirement
        return self.driver.find_elements(By.XPATH, *self.comfort_reqs).text()

    def set_phone_number(self): #Sets and validates phone number
        self.driver.find_element(*self.phone_field).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_number_input))
        self.driver.find_element(*self.phone_number_input).send_keys(data.phone_number)
        self.driver.find_element(*self.phone_next_button).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_code_field))
        code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.phone_code_field).send_keys(code)
        self.driver.find_element(*self.confirm_phone_code).click()

    def get_phone_number(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_field))
        return self.driver.find_element(*self.phone_field).text()



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):   #Test to set address from and address to in Urban Routes form
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_rate(self): #Test to request a taxi and select Comfort rate
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        routes_page.wait_for_request_taxi_button()
        routes_page.click_request_taxi_button()
        routes_page.wait_for_load_comfort_rate()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_home_page()
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        routes_page.wait_for_request_taxi_button()
        routes_page.click_request_taxi_button()
        routes_page.wait_for_load_comfort_rate()
        routes_page.click_comfort_rate()
        assert "Manta y pañuelos" or "Cortina acústica" in routes_page.verify_comfort_is_selected()
        routes_page.set_phone_number()
        phone_number = routes_page.get_phone_number()
        assert phone_number == data.phone_number #Verifies the phone number was added successfully




    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
