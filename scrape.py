import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def search_input(letter):
    
    search_input = driver.find_element(By.ID, 'search-input')
    search_input.clear()
    search_input.send_keys(letter)
    
driver = webdriver.Chrome()
driver.get("https://my.clevelandclinic.org/health/diseases?dFR[type][0]=Diseases")
title = driver.title
datas = {}
for letter in "a":
    # abcdefghijklmnopqrstuvwxyz
    print(letter)
    search_input(letter)
    
    site_hits = driver.find_elements(By.ID, 'site-hits')  # Replace with actual CSS selector
    # print(site_hits)
    articles = site_hits[0].find_elements(By.CLASS_NAME, 'search-results-article')
    print(articles)
    for article in articles:
        print("____")
        # Find the link element within the article
        link_element = article.find_element(By.CSS_SELECTOR, 'h2.search-results-article__title a')
        link_text = link_element.text
        link_href = link_element.get_attribute('href')
        
        # Find the description element within the article
        description_element = article.find_element(By.CSS_SELECTOR, 'p.search-results-article__description')
        description_text = description_element.text
        
        # Print the extracted details
        datas["Name"] = link_text
        datas["Url"] = link_href
        datas["description"] = description_text
        
        print("Link Text:", link_text)
        print("Link URL:", link_href)
        print("Description:", description_text)
        print("-----------")
        # Open the link in a new tab
        # driver.execute_script("window.open(arguments[0]);", link_href)
        
        # # Switch to the new tab
        # driver.switch_to.window(driver.window_handles[-1])
        
        link_element.click()
        
        
        try:
            nav_element = driver.find_element(By.CSS_SELECTOR, 'nav.flex.flex-wrap.gap-y-rem16px.gap-x-rem32px')
            anchor_elements = nav_element.find_elements(By.TAG_NAME, "a")
            href_values = [anchor.get_attribute('href') for anchor in anchor_elements]
            datas = {anchor: {} for anchor in anchor_elements}
            print(datas)
            # break
            for href in href_values:
                print(href)
                # break
                sub_titles = driver.find_elements(By.ID, href.split("#")[1])
                for sub_title in sub_titles:
                    questions = sub_title.find_elements(By.TAG_NAME, "h3")
                # print(check[0].text)
                    for question in questions:
                        
                        print(question.text)
                        sibling = question.find_element(By.XPATH, 'following-sibling::*[1]')
                        # break
                        paragraphs = []
                        while sibling and sibling.tag_name != "h3":
                            if sibling.tag_name == "p":
                                paragraphs.append(sibling.text)
                            try:
                            # Move to the next sibling
                                sibling = sibling.find_element(By.XPATH, 'following-sibling::*[1]')
                            except:
                            # If there are no more siblings, break the loop
                                break
                        paragraphs_text = '\n\n'.join(paragraphs)
                        print(paragraphs_text)
                # break
        except Exception as e:
            print("An error occured:", e)

        # finally:
        driver.back()
        driver.implicitly_wait(10)
        print(article)
# driver.quit()