import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException, TimeoutException

URL = "https://my.clevelandclinic.org/health/diseases?dFR[type][0]=Diseases"

#chis not scraped

def clean_text(text):
    replacements = {
        "\n": " ",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2014": "--",
        "\"": "'",
        # ""\": "'",
        
    }
    
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def main():
    driver = webdriver.Chrome()
    # abcdefghijklmnopqrstuvwxyz
    datas = {}
    for letter in "abcdefghijklmnopqrstuvwxyz":
        
        driver.get(URL)
        title = driver.title
        S = driver.find_elements(By.CLASS_NAME, "library-search-nav")
        button = driver.find_elements(By.CSS_SELECTOR, ".health .library-search-nav__browse-btn")
        button[0].click()
        id_ = f"0d9b9f78-214b-42f2-8f1d-da3169148f65js-{letter}" #changes frequently
        # 4446aad6-e85e-49c6-9d25-056dc3614944js-a
        # print(id_)
        
        try:
            a_vals = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.ID, id_)))
            # print(len(a_vals))
            
            a_vals[0].click()
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".l-3col--1")))
            
            links = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'index-list-link')))
            print(f"Total Disease with letter {letter}: {len(links)}")
        
        except TimeoutException as e:
            print("TimeoutException: The elements could not be found.")

        for link in links:
            disease_name = link.text
            print(f"Scraping {disease_name}...")
            datas[disease_name] = {}
            
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link)).click()
                
                nav_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'nav.flex.flex-wrap.gap-y-rem16px.gap-x-rem32px')))
                anchor_elements = nav_element.find_elements(By.TAG_NAME, "a")
                href_values = [anchor.get_attribute('href') for anchor in anchor_elements]
                
                for href in href_values:
                    # print(href)
                    in_title = href.split("#")[1]
                    datas[disease_name][in_title] = {}
                    datas[disease_name][in_title]["source"] = href
                    
                    sub_titles = driver.find_elements(By.ID, in_title)
                    for sub_title in sub_titles:
                        questions_h3 = sub_title.find_elements(By.TAG_NAME, "h3")
                        questions_h4 = sub_title.find_elements(By.TAG_NAME, "h4")
                        questions = questions_h3 + questions_h4
                        # print(questions)
                        for question in questions:
                            # print(question.text)
                            # sibling = question.find_element(By.XPATH, 'following-sibling::*[1]')
                            
                            try:
                                sibling = question.find_element(By.XPATH, 'following-sibling::*[1]')
                            except:
                                print(f"xxx  No sibling {disease_name} found")
                                break
                            
                            paragraphs = []
                            while (sibling and sibling.tag_name != "h3") or (sibling and sibling.tag_name != "h4"):
                                if sibling.tag_name == "p" or sibling.tag_name == "ul" or sibling.tag_name == "li":
                                    paragraphs.append(sibling.text)
                                elif sibling.tag_name == "h3" or sibling.tag_name == "h4":
                                    break
                                try:
                                    sibling = sibling.find_element(By.XPATH, 'following-sibling::*[1]')
                                except:
                                    break
                            
                            
                            # paragraphs_text = '\n\n'.join(paragraphs)
                            paragraphs_text = ' '.join(paragraphs)
                            # print(paragraphs_text)
                            datas[disease_name][in_title][question.text] = clean_text(paragraphs_text)
                            # break
                    # break
            except (StaleElementReferenceException, ElementNotInteractableException, TimeoutException) as e:
                print(f"An error occurred: {e}")
            
            driver.back()
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'index-list-link')))
                links = driver.find_elements(By.CLASS_NAME, 'index-list-link')  # Re-locate links after navigating back
            except TimeoutException:
                print("Timeout while waiting for elements after navigating back.")
            # break
        with open(f"dataset:v1/disease_{letter}.json", 'w') as json_file:
            json.dump(datas, json_file, indent=4)
        
        print(f"Disease {letter} dumped.")
        datas = {}
        print("___")
    driver.quit()

if __name__ == "__main__":
    main()
