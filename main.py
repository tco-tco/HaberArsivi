from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from database import createDB, createTable, insertValue
from userInfo import ilListe, dbName

import time

dbName=dbName
createDB(dbName)    

for ilAdi in ilListe:
    createTable(ilAdi,dbName)
    driver = webdriver.Chrome()
    driver.get(f"https://{ilAdi}.tarimorman.gov.tr/HaberArsivi")
    driver.implicitly_wait(60)
    driver.execute_script("window.open()")
    driver.implicitly_wait(60)
### İlgili haber sayfasındaki url listesini tek tek gezip ilgili veriyi toplar ve database'e kaydeder.
    def dataScrape():
        arsivList=driver.find_elements(By.CLASS_NAME, "arsivDetayLink")
        driver.implicitly_wait(60)
        urlList=[i.get_attribute("href") for i in arsivList]

        for url in urlList:
            driver.switch_to.window(driver.window_handles[1])   
            driver.implicitly_wait(60)

            driver.get(f"{url}")
            driver.implicitly_wait(60)
            urlSplitList=str(url).split("/")
            indexHaber=urlSplitList.index("Haber")
            haberNo=urlSplitList[indexHaber+1]
            print(int(haberNo))
            hata=""
            try:
                title=driver.find_element(By.XPATH,"//h1[@class='page-title black']").text 
                driver.implicitly_wait(60)
                #print(title)
                #hata=""
            except NoSuchElementException as NSEE:
                ##print(NSEE)
                hata="sayfa hata verdi"
                
                #print(hata)
                #print(url)
            
            if hata=="sayfa hata verdi":
                insertValue(ilAdi, None, None, None, None, url, haberNo, None, hata, dbName)
                print(f"{hata}-1")
                continue
            else:
                title=driver.find_element(By.XPATH,"//h1[@class='page-title black']").text 
                driver.implicitly_wait(60)
                date=driver.find_element(By.XPATH,"//span[@class='itemDateCreated']").text
                driver.implicitly_wait(60)
                date=date.rstrip("/")
                #print(date)
                pageView=driver.find_element(By.XPATH,"//span[@class='itemAuthor']").text
                driver.implicitly_wait(60)
                #print(pageView)
                pageView=str(pageView.rstrip("/"))
                pageView=pageView.split(":")[1]
                #print(int (pageView))
                text=driver.find_element(By.CSS_SELECTOR,('[class*="ExternalClass"]')).text
                text=text.strip()
                #print(text)
                image=driver.find_element(By.XPATH,"//span[@class='hoverBorderWrapper']/img")
                image_url=image.get_attribute('src')
                time.sleep(0)
                driver.switch_to.window(driver.window_handles[0])   # yeni pencere/sekme
                driver.implicitly_wait(60)

            insertValue(ilAdi, title, date, pageView, text, url, haberNo, image_url, hata, dbName)
    
    count=0 # işlem yapılan sayfa sayısı için sayaç başlangıcı
    while True:
        buttons=driver.find_elements(By.XPATH,"//span[@class='btn-group pager-buttons']//input")
        driver.implicitly_wait(60)

        dataScrape()

        count+=1
        #print(count)

        for pageNum in range(1,len(buttons)+1):
            pageButton=driver.find_element(By.XPATH,f"//span[@class='btn-group pager-buttons']//input[{pageNum}]")
            driver.implicitly_wait(60)
            ##print(pageButton.get_attribute("value"))
            if pageButton.get_attribute("value")=="<<":
                #print("<< var")
                #print("pass")
                continue
            elif pageButton.get_attribute("value")==">>":
                #print(">> var")
                #print("pass")
                continue
            else:
                pageButton.click()
                #print("sayfa değişti")
                dataScrape()

                count+=1
                #print(count)
            time.sleep(1)


        buttons=driver.find_elements(By.XPATH,"//span[@class='btn-group pager-buttons']//input")
        driver.implicitly_wait(60)
        pageList=[button.get_attribute("value") for button in buttons]

        if pageList[-1]==">>":
            driver.find_element(By.XPATH,f"//span[@class='btn-group pager-buttons']//input[{len(buttons)}]").click()
            driver.implicitly_wait(60)
            #print("sayfa grubu değişti")
            time.sleep(1)
        else:
            break
    print(count)    # double check için işlem yapılan sayfa sayısını sayar
