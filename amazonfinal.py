"""
Amazon Product Optimization Project - Minsuk "Sean" Hue and Sangsoo "Andy" Lim
Completed December 30, 2022

"""

#This code takes a product that the user is searching for on Amazon, a minimum star rating, and the user's budget
#Using those parameters, this code will generate a list of products with the minimum star rating that is reasonably priced around the user's budget
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time


class Product:
    """
    The Product class to store the information about the individual product price, ASIN number (a unique product identifier), and difference (to the mean, explained later)
    It works with the "collect_page_data" function to create the Product object for each individual product
    It is also used when calculating the mean of the products to choose the most reasonably priced product from the originally large selection

    """
    def __init__(self):
        self.price = None
        self.asin = None
        self.difference = None

    def __repr__(self):
        return self.asin + ', ' + self.price
    
    def __eq__(self, other):
        return self.price == other.price

        
def collect_page_data(browser, list_products) -> list:
    """
    This function collects product name & price and returns list of Product objects
    Input: 
        browser (object), list_products (list)
    Returns:
        list_products (list): updated list with Product objects

    """

    #This code gets rid of all sponsored items with contains.
    items = browser.find_elements(By.XPATH, "//div[contains(@class, 's-result-item s-asin')]")
    items = WebDriverWait(browser,5).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 's-result-item s-asin')]")))
    for i in items:
        new_product = Product()

        #This code finds the prodct prices (whole and fraction) and adds them (string) together to get the full price
        prices = i.find_elements(By.XPATH, ".//span[@class='a-price-whole']")
        cents = i.find_elements(By.XPATH, ".//span[@class='a-price-fraction']")

        #Combines the dollars and cents
        if prices != [] and cents != []:
            total = prices[0].text + '.' + cents[0].text
        else:
            #If there are no price associated with the product (price = 0) then set the total cost of the product to be 0, which will be filtered later
            total = "0"
        new_product.price = total

        #This code finds the product ASIN number
        s = i.get_attribute("data-asin")
        new_product.asin = s
        list_products.append(new_product)

    return list_products



def main():
    """
    This main function is where the main body of the code is located
    It will first intitalize the WebBrowser and do all the necessary steps such as: 
                                                                        - Searching up the product 
                                                                        - Choosing the star rating
                                                                        - Getting all the products
                                                                        - Filtering all the products without a price or that is above the user's budget
                                                                        - Sorting all the products in lowest to highest squared difference to the mean 
                                                                        - Showing the first five results that are reasonably priced
                                                                        
    """

    #Asking the user for the product they want, the minimum star rating of the specified prodcut, and their maximum price budget
    user_product = input("What product are you searching for, please be specific?: ")
    user_star_minimum = input("What minimum star rating are you looking for (ex: 4, 3, 2, 1), just enter the number?: ")
    user_max_price = float(input("What is your maximum budget for this item?: "))


    #This code opens the "amazon.com" site, which is the site where the whole star rating/price comparison will take place
    mods = webdriver.ChromeOptions()
    #This line of code is used to make web driver to run in the background instead of pop up (Can uncomment the line below)
    #mods.add_argument('--headless')
    browser = webdriver.Chrome(options = mods, service = Service(ChromeDriverManager().install()))
    browser.maximize_window()
    browser.get("https://www.amazon.com/")
    browser.implicitly_wait(5)

    
    #This code sends the specified product name to the search bar
    browser_product_search = browser.find_element(By.XPATH, "//*[@id='twotabsearchtextbox']")
    browser_product_search.send_keys(user_product)
    time.sleep(1)

    #This code clicks on the search button after the specified product name is entered
    browser_product_click = browser.find_element(By.XPATH, "//*[@id='nav-search-submit-button']")
    browser_product_click.click()
    time.sleep(1)
    
    #This code finds and clicks given minimum rating on the sidebar of Amazon
    path = "//i[@class='a-icon a-icon-star-medium a-star-medium-%s']" % user_star_minimum
    browser_star_click = browser.find_element(By.XPATH, path)
    browser_star_click.click()
    time.sleep(1)

    #Intializing to store the Product objects
    list_products = []

    #This code uses the previously defined function of storing all Product objects and also clicks the "Next" button to get more data from more pages
    for page in range(3):
        collect_page_data(browser, list_products)
        browser_next_click = browser.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
        browser_next_click.click()
        time.sleep(3)
    
    #This code finds the mean of all the product prices by filtering out the one with no prices and the ones above the user's budget
    price_mean = 0
    zero_counter = 0
    for item in list_products:
        if item.price != '0'and float(item.price.replace(',', '')) <= user_max_price:
            price_mean = price_mean + float(item.price.replace(',', ''))
            zero_counter += 1
    price_mean = price_mean / zero_counter

   #This code finds all the squared differences of the products to the mean, which is later used to determine the most reasonably priced specified item
    for item in list_products:
        if item.price != '0' and float(item.price.replace(',', '')) <= user_max_price:
            item.difference = (price_mean - float(item.price.replace(',', '')))**2
    
    #This code sorts all of the products in the list from lowest to highest sqaured difference to the mean
    for i in range(len(list_products)):
        if list_products[i].difference != None:
            for j in range(len(list_products)):
                if list_products[j].difference != None and list_products[j].difference >= list_products[i].difference:
                    list_products[j], list_products[i] = list_products[i], list_products[j]

    #This is what the user will see after the entire code has been run through
    #The user will get the first five products (ASIN and price) that are reasonably priced, using our definition
    #The user will then be able to copy and paste the product ASIN number on Google/Amazon to see the product
    print("Your products are: (Copy and paste the ASIN numbers on Google/Amazon):\n")
    for i in range(5):
        if list_products[i].difference != None:
            print(list_products[i])

    browser.quit()


if '__main__':
    main()