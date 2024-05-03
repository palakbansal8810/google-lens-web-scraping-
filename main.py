from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup
import json

class WebScraping:
    def get_webdriver(options=None):
        browsers = [
            (webdriver.Chrome, ChromeOptions),
            (webdriver.Firefox, FirefoxOptions),
            (webdriver.Edge, EdgeOptions),
            (webdriver.Safari, None), 
            (webdriver.Ie, None),  
        ]

        for browser, options_class in browsers:
            try:
                options = options_class()
                options.add_argument("--headless")

                if browser == webdriver.Chrome:
                    options.use_chromium = True


                driver = browser(options=options)
                return driver, options
            except WebDriverException:
                continue
        raise WebDriverException("No suitable web browser found")


    def scrape_product_info(image_url):
        
        product_description = ""
        product_availability = ""
        product_price = ""
        product_link = ""
        product_src1=""
        product_src2=""
        product_company=""
        
        driver, options = WebScraping.get_webdriver()

        url = f"https://lens.google.com/uploadbyurl?url={image_url}&en=in"
        driver.get(url)

        try:
            
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "accept"))).click()
        except:
            pass  

        # WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "Vd9M6")))

        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        divs = soup.find_all("div", class_="Vd9M6")

        products = []

        for div in divs:
            product = {}

            description_elem = div.find("div", class_="UAiK1e")
            if description_elem:
                product_description = description_elem.get_text(strip=True)
            
            availability_elem = div.find("span", class_="Bc59rd rR5x2d")
            if availability_elem:
                product_availability = availability_elem.get_text(strip=True)
            
            price_elem = div.find("span", class_="DdKZJb")
            if price_elem:
                product_price = price_elem.get_text(strip=True)

            product_comapny = div.find("span", class_="fjbPGe")
            if product_comapny:
                product_company = product_comapny.get_text(strip=True)

            product_src_img2 = div.find("div", class_="ksQYvb")
            if product_src_img2:
                product_src2 = product_src_img2["data-thumbnail-url"]

            product_src_img1 = div.find("img", class_="wETe9b YRoOie KRdrw")
            if product_src_img1:
                product_src1 = product_src_img1['src']
            
            nested_div = div.find_parent("div", class_="G19kAf ENn9pd")
            if nested_div:
                a_tag = nested_div.find("a")
                if a_tag:
                    product_link = a_tag["href"]

            product["Product Description"] = product_description
            product["Product Availability"] = product_availability
            product["Product Price"] = product_price
            product["Product Link"] = product_link
            product["Product Company Icon"] = product_src1
            product["Product Source Image2"] = product_src2
            product["Product Company"] = product_company

            products.append(product)

        driver.quit()

        return json.dumps(products, indent=2, ensure_ascii=False)

if __name__=='__main__':
    image_url = input("image address:\n")
    result = WebScraping.scrape_product_info(image_url)
    print(result)
