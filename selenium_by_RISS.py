from selenium import webdriver
import bs4
import time
from selenium.webdriver.common.keys import Keys

#키워드 검색
driver = webdriver.Chrome(r"C:\Users\pys01\Desktop\python_c\chromedriver.exe") #webdriver 위치 (자기의 컴퓨터 위치에 맞춰 지정)
keyword = input() 
xpath = 'http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery='+keyword+'&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=0&orderBy=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=&resultKeyword=&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=bib_t&colName=bib_t&pageScale=10&isTab=Y&regnm=&dorg_storage=&language=&language_code=&query=' + keyword 
driver.get(xpath)

answer = [] #크롤링한 정보가 들어갈 리스트

check_first_page = 1 #첫 번째 페이지(1-10)에서 논문이 끝난 경우를 탐지하는 변수
for_check = 1 # 다음 페이지가 존재하지 않는 경우를 탐지하는 변수 

for j in range(3,13): #3~12 다음 페이지까지 (1~10)
    try: 
    #첫 페이지에 있는 10개의 논문 크롤링 시작
        for i in range(1,11):
            move = '/html/body/div[1]/div[2]/div[4]/div[2]/div/div[2]/div[2]/ul/li['+str(i)+']/div[2]/p[1]/a'
            driver.find_element_by_xpath(move).send_keys(Keys.CONTROL + '\n') #새 탭 열기
            driver.switch_to.window(driver.window_handles[1])

            plus = [] #논문에 넣을 정보들
            element = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[1]/div[1]/h3')
            plus.append(element.text) #이름
            element2 = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]/div/p/a')
            plus.append(element2.text) #저자
            element3 = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[1]/div[2]/div[1]/ul/li[4]/div/p')
            plus.append(element3.text) #년도

            for k in range(1,3): #초록
                try:
                    element4 = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[2]/div[1]/div/div['+str(k)+']/div[2]/p')
                except: #초록이 없으면 그냥 지나간다
                    continue
                plus.append(element4.text)       
            answer.append(plus)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
    except:
        check_first_page = 0 
        break
        
    #한 페이지 논문 다 크롤링하면 다음 페이지로
    page = '/html/body/div[1]/div[2]/div[4]/div[2]/div/div[3]/a['+str(j)+']' 
    driver.find_element_by_xpath(page).click();    

#page = '/html/body/div[1]/div[2]/div[4]/div[2]/div/div[3]/a[12]' 
#driver.find_element_by_xpath(page).click();    


#(1~10) 이랑 (11~20)부터 다음 페이지로 이동하는 크롤링 키가 다르므로 반복문을 따로 작성 -- (11~20)부터 크롤링하는 코드
if(check_first_page !=0):
    while(True):
        if(for_check !=1): #페이지가 없다는 오류 메시지를 받으면 크롤링을 멈추기
            break
        for j in range(4,14): #11~20page + 다음 페이지 누르기 --> for 문 돌리면 (21-30)으로
            try: 
                #각 페이지당 크롤링 시작(반복문 시작 시 11page니 크롤링 먼저 하고 다음 페이지로 이동)
                for i in range(1,11):
                    move = '/html/body/div[1]/div[2]/div[4]/div[2]/div/div[2]/div[2]/ul/li['+str(i)+']/div[2]/p[1]/a'
                    driver.find_element_by_xpath(move).send_keys(Keys.CONTROL + '\n') #새 탭 열기
                    driver.switch_to.window(driver.window_handles[1])

                    plus = [] #논문에 넣을 정보들
                    element = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[1]/div[1]/h3')
                    plus.append(element.text) #이름
                    element2 = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]/div/p/a')
                    plus.append(element2.text) #저자
                    element3 = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[1]/div[2]/div[1]/ul/li[4]/div/p')
                    plus.append(element3.text) #년도

                    for k in range(1,3): #초록
                        try:
                            element4 = driver.find_element_by_xpath('/html/body/div/div[4]/div[4]/div/div/div/div[2]/div[1]/div/div['+str(k)+']/div[2]/p')
                        except: #초록이 없으면 그냥 지나간다
                            continue
                        plus.append(element4.text)
        
                    answer.append(plus)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                
            except:
                for_check = 0
                break
            page = '/html/body/div[1]/div[2]/div[4]/div[2]/div/div[3]/a['+str(j)+']'
            driver.find_element_by_xpath(page).click();
            time.sleep(0.5)     

print("크롤링한 논문 개수 :",len(answer),"개\n")
for i in range(len(answer)):
    print(answer[i])






