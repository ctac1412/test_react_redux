from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class Browser(object):

    def __init__(self,browser="",state=[],fgisUser={'login': '89168142181', 'password': 'Mlm28021991', 'role': '//*[@id="o0"]', 'method': 'phone'}):
        """Constructor"""
        self.state = state
        self.browser = self.initBrowser()
        self.fgisUser = fgisUser

    def initBrowser(self):
        self.addLogItem("Start init browser")
        fp = self.getFirefoxProfile("10.90.0.47","80")
        self.addLogItem("Get profile")
        self.addLogItem("Init browser")
        driver = webdriver.Firefox(firefox_profile=fp,executable_path=r'C:\Users\Dep\Desktop\selenium\geckodriver.exe')
        # driver.get("https://stage-2-docs.advance-docs.ru")
        self.addLogItem("Browser init")
        return driver

    def closeBrowser(self):
        self.addLogItem("Close browser")
        self.browser.close()

    def getFirefoxProfile(self,PROXY_HOST,PROXY_PORT):
    
        fp = webdriver.FirefoxProfile()
        # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
     
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http",PROXY_HOST)
        fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
        fp.set_preference("general.useragent.override","whater_useragent")
        fp.update_preferences()       
        return fp

    def addLogItem(self,msg="Message?"):
        self.state.append(msg )

    def readLog(self):
        return self.state

    def getUrl(self,url):
        self.addLogItem("Get " + url)
        
        self.browser.get(url)

    def loginFgis(self):
        import time
        try:
            self.addLogItem("Go to fsa")
            self.getUrl("http://10.250.4.13/fsa_cabinet_v2.0/")
            self.addLogItem("Login")
            go = WebDriverWait(self.browser, 60).until(
                EC.element_to_be_clickable((By.XPATH , '/html/body/div[1]/form/div/div[2]/div/a/div'))
            )
            go.click()
            time.sleep(1)
            self.addLogItem(self.fgisUser)
            if self.fgisUser["method"] == "phone":
                login = WebDriverWait(self.browser, 60).until(
                EC.element_to_be_clickable((By.XPATH , '//*[@id="mobileOrEmail"]'))
                )
                login.click()
                login.send_keys("89168142181" )
                password = self.browser.find_element_by_xpath('//*[@id="password"]')
                password.click()
                password.send_keys(self.fgisUser["password"] )
            self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[1]/form/div[1]/div[3]/div[3]/div[2]/button').click()
            self.browser.find_element_by_xpath(self.fgisUser["role"] ).click()
            exit_button = WebDriverWait(self.browser, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME , "exit"))
            )
            self.addLogItem("Login accept. Can Logout")
            
            pass
        except Exception as o:

            self.addLogItem(o)
            pass

    def isloginFgis(self):
            return  self.browser.execute_script("""
            return fetch("http://10.250.4.13/fsa_decl_v2.0",{
            method : 'GET'
            }).then((response)=>{
            return response.text()
            }).then(text=>{         
                let parser = new DOMParser()
                let index = parser.parseFromString(text, "text/html");
                if (index.querySelector('#authform')) {return true};                
                return false
            });
            """) 
    def copyCoockie(self):
        cookies = self.browser.get_cookies()
        s = requests.Session()
        
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        

        return s
        
    def test(self):
                    # cookies = [{u'domain': u'academics.vit.ac.in',
            # u'name': u'ASPSESSIONIDAEQDTQRB',
            # u'value': u'ADGIJGJDDGLFIIOCEZJHJCGC',
            # u'expiry': None, u'path': u'/',
            # u'secure': True}]
        print ("Test")
        
            # cookies = driver.get_cookies()
            # s = requests.Session()
            # for cookie in cookies:
            #     s.cookies.set(cookie['name'], cookie['value'])

        # self.browser.execute_script("""
        #             fetch("http://10.250.4.13/fsa_decl_v2.0/api/tnVed/?node=40815&_=1529529238888",{
        #             method : 'GET',
        #             credentials: 'include'
        #             }).then((response)=>{
        #             console.log(response)
        #             });
        #                     """)

    def logoutFgis(self):
        self.addLogItem("Logout")
        self.browser.execute_script("document.querySelector('.exit').click()")
        self.addLogItem("Logout accept.")
