from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup


# Set up the WebDriver
service = Service()
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Run in headless mode
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the URL
    url = "https://www.scribd.com/document/403794990/LTO-Drivers-License-Exam-Reviewer"
    driver.get(url)
    
    print(url)
    
    # Give some extra time to ensure the page is fully loaded
    time.sleep(5)  # Adjust the sleep time if necessary

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for the scroll to complete

    # Wait for the dynamic content to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "outer_page_container"))
    )
    
    print("FOUND")

    # Find all divs with class 'outer_page' and extract their inner HTML
    inner_pages = driver.find_elements(By.CLASS_NAME, 'outer_page')

    # Create a string to hold the combined HTML content
    combined_html = ""
    
    combined_html += '<div role="document" tabindex="0" class="outer_page_container">'
    i = 1
    # Loop through each inner page, scroll to it if needed, and extract its HTML
    for page in inner_pages:
        combined_html += '<div class="outer_page only_ie6_border " style="width: 859px; height: 1117px;">'
        # Scroll to the current page
        driver.execute_script("arguments[0].scrollIntoView();", page)
        time.sleep(1)  # Wait for the scroll to complete
        try:
            # Wait for the dynamic content to load (example check for class 'newpage')
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "newpage"))
            )
            print(f"{i} | FOUND")
            i += 1
        except:
            print("Not Found")

        # Extract the inner HTML of the current page
        page_html = page.get_attribute('innerHTML')
        combined_html += page_html
        combined_html += '</div>'
        
    # Extract styles and append to combined_html
    styles = driver.find_elements(By.TAG_NAME, "style")
    
    combined_html += "<style>"
    
    for style in styles:
        style_html = style.get_attribute('innerHTML')
        combined_html += style_html

    combined_html += ".auto__doc_page_webpack_doc_page_blur_promo {display:none !important;} .text_layer {text-shadow: none !important; color: black !important;} .newpage span.a {color: black !important; z-index: 9999 !important;}img {opacity: 1 !important;}"
    combined_html += "</style>"
    combined_html += "</div>"

    # Prettify the combined HTML using BeautifulSoup
    soup = BeautifulSoup(combined_html, 'html.parser')
    pretty_html = soup.prettify()

    # Save the prettified HTML content to a file
    with open("testcontent.html", "w", encoding='utf-8') as file:
        file.write(pretty_html)

    print("Extracted HTML content saved to testcontent.html")
finally:
    # Close the WebDriver
    driver.quit()
