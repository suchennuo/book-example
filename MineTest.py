
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the Firefox driver
driver = webdriver.Chrome()

# go to the google home page
driver.get("https://www.google.com.hk")

# find the element that's name attribute is q (the google search box)
inputElement = driver.find_element_by_name("q")

# type in the search
inputElement.send_keys("Cheese!")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

# the page is ajaxy so the title is originally this:
print (driver.title)

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # You should see "cheese! - Google Search"
    print (driver.title)

finally:
    driver.quit()

import tinify
tinify.key = 'TOUYJ4N-EjvK4S8IcCt9Uef6ABxKqfBM'
tinify.proxy = "http://user:pass@192.168.0.1:8080"
source = tinify.from_file("unoptimized.jpg")
source.to_file("optimized.jpg")

#
# with open("unoptimized.jpg", 'rb') as source:
#     source_data = source.read()
#     result_data = tinify.from_buffer(source_data).to_buffer()
#
# source = tinify.from_url("https://cdn.tinypng.com/images/panda-happy.png")
# source.to_file("optimized.jpg")
#
# https://tinypng.com/developers/reference/python
#
# http://leonshi.com/2015/11/02/tinypng-compress/
#
#
# http://leonshi.com/