import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def main(driver, datas):
    
    # for letter in "a":
        # abcdefghijklmnopqrstuvwxyz


    site_hits = driver.find_elements(By.ID, 'site-hits')  # Replace with actual CSS selector
    # print(site_hits)
    articles = site_hits[0].find_elements(By.CLASS_NAME, 'search-results-article')
    # articles
    # datas = {}
    for article in articles:
        # print("____")
        # Find the link element within the article
        link_element = article.find_element(By.CSS_SELECTOR, 'h2.search-results-article__title a')
        link_text = link_element.text
        link_href = link_element.get_attribute('href')
        
        # Find the description element within the article
        description_element = article.find_element(By.CSS_SELECTOR, 'p.search-results-article__description')
        description_text = description_element.text
        
        
        datas[f"{link_text}"] = {}
        datas[f"{link_text}"]["source"] = link_href
        datas[f"{link_text}"]["description"] = description_text
        # else:
        #     continue
        # print("Link Text:", link_text)
        # print("Link source:", link_href)
        # print("Description:", description_text)
        # print("-----------")
        # Open the link in a new tab
        # driver.execute_script("window.open(arguments[0]);", link_href)
        
        # # Switch to the new tab
        # driver.switch_to.window(driver.window_handles[-1])
        
        link_element.click()
        
        
        try:
            nav_element = driver.find_element(By.CSS_SELECTOR, 'nav.flex.flex-wrap.gap-y-rem16px.gap-x-rem32px')
            anchor_elements = nav_element.find_elements(By.TAG_NAME, "a")
            href_values = [anchor.get_attribute('href') for anchor in anchor_elements]
            # datas = {anchor: {} for anchor in anchor_elements}
            # print(datas)
            # break
            for href in href_values:
                print(href)
                # break
                in_title = href.split("#")[1]
                datas[f"{link_text}"][in_title] = {}
                datas[f"{link_text}"][in_title]["source"] = href
                sub_titles = driver.find_elements(By.ID, in_title)
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
                        datas[f"{link_text}"][in_title][question.text] = paragraphs_text
                        break
                # break
        except Exception as e:
            print("An error occured:", e)
        # break
        # finally:
        driver.back()
        driver.implicitly_wait(10)
        # print(article)
    driver.quit()

datas = {}
for letter in "ac":
    driver = webdriver.Chrome()
    driver.get("https://my.clevelandclinic.org/health/diseases?dFR[type][0]=Diseases")
    title = driver.title
    search_input = driver.find_element(By.ID, 'search-input')
    search_input.clear()
    search_input.send_keys(letter)
    driver.implicitly_wait(5)
    main(driver, datas)

    