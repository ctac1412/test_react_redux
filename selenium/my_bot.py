# things.py

# Let's get this party started!
import falcon
import json
import browser
import postBd
import requests
from bs4 import BeautifulSoup
import datetime, time


s = requests
# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
http_proxy  = "http://10.90.0.47:80"
# https_proxy = "https://10.10.1.11:1080"
# ftp_proxy   = "ftp://10.10.1.10:3128"
# "","80"
proxyDict = { 
              "http"  : http_proxy, 
            #   "https" : https_proxy, 
            #   "ftp"   : ftp_proxy
            }

_tnved = postBd.tnved_updater()

def is_login():
    global s
    s_resp = s.get("http://10.250.4.13/fsa_decl_v2.0",proxies=proxyDict)
    soup = BeautifulSoup(s_resp.text, 'html.parser')
    login = not bool(soup.findAll(id="authform")) 
    return login

def check_login(func):
    """
    Декоратор, проверяющий авторизацию.
    """

    def wrapper(*args, **kwargs):
        global s
        if not is_login() :
            b = browser.Browser()
            b.loginFgis()
            s = b.copyCoockie()
            b.closeBrowser()
        res = func(*args, **kwargs)
        return res
    return wrapper  

def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло
    выполнение декорируемой функции.
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__, time.clock() - t)
        return res
    return wrapper

def logging(func):
    """
    Декоратор, логирующий работу кода.
    (хорошо, он просто выводит вызовы, но тут могло быть и логирование!)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(func.__name__, args, kwargs)
        return res
    return wrapper


@check_login
def load_root():
    global s 
    global _tnved
    s_resp = s.get("http://10.250.4.13/fsa_decl_v2.0/api/tnVed",proxies=proxyDict)
    root_list = s_resp.json()   
    _tnved.truncate_to_parse()
    _tnved.insert_to_parse(root_list)
    print ("Well")
    # for r in root_list:
    #     _tnved.insert_to_parse(root_list)

# @check_login 
def parse_item(node_id):
    global s 
    global _tnved
    d = datetime.datetime.now()
    for_js = int(time.mktime(d.timetuple())) * 1000
    url  = "http://10.250.4.13/fsa_decl_v2.0/api/tnVed?node=" + str(node_id) + "&_=" + str(for_js)
    s_resp = s.get(url,proxies=proxyDict)
    res = s_resp.json()
    # print ("parse_item", res)
    _tnved.insert_to_parse(node_id,res)


class ThingsResource(object):
    @logging
    def on_get(self, req, resp):
        """Handles GET requests"""
        global s   
        res = "Well"
        try:
            b = browser.Browser()
            b.loginFgis()
            s = b.copyCoockie()
            b.closeBrowser()
            pass
        except Exception as o:
            print (o)
            res = o
            pass
        finally:
            resp.status = falcon.HTTP_200  # This is the default status
            resp.body = json.dumps(res, ensure_ascii=False) 
            pass 
     
class StatusResource(object):
    @logging
    def on_get(self, req, resp):
        """Handles GET requests"""
        global s  
        s_resp = s.get("http://10.250.4.13/fsa_decl_v2.0",proxies=proxyDict)
        soup = BeautifulSoup(s_resp.text, 'html.parser')
        login = not bool(soup.findAll(id="authform")) 
        
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"Login_status":login}, ensure_ascii=False) 

class TnvedResource(object):
    @logging
    @check_login
    def on_get(self, req, resp):
        """Handles GET requests"""
        global s 
        global _tnved 
        params  = req.params
        print (req.params)
        res = "" 
        # s_resp = s.get("http://10.250.4.13/fsa_decl_v2.0/api/tnVed",proxies=proxyDict)
        # soup = BeautifulSoup(s_resp.text, 'html.parser')
        
        # login = not bool(soup.findAll(id="authform")) 
        if _tnved:
            if "force_start" in params and bool(params["force_start"]) == True:
                print ("force_start")
                load_root()
            if "load_records" in params and bool(params["load_records"]) == True:
                print ("load_records")
                
                record = _tnved.record_next_parse()
                while record:
                    parse_item(record["id"])
                    record = _tnved.record_next_parse()
                # print ("record", record)
                    # if not record:
                    #     res = "I dont have record to parse.... hmmmm"
                    # else:
            if "get_count" in params and bool(params["get_count"]) == True:            
                res = _tnved.count_to_parse()    
                

            

            # _tnved.insert_to_parse(root_list)
            # print (_tnved.session)
            
        else:
            res = "I dont have _tnved.... hmmmm"

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(res, ensure_ascii=False) 

class TnvedStat(object):
    @logging
    def on_get(self, req, resp):
        """Handles GET requests"""
        global s 
        global _tnved 
        params  = req.params
        print (req.params)
        res = "" 
        if _tnved:
            if "get_count" in params and bool(params["get_count"]) == True:            
                res = _tnved.count_to_parse()    
        else:
            res = "I dont have _tnved.... hmmmm"

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(res, ensure_ascii=False) 

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()
status = StatusResource()
tnved = TnvedResource()
tnvedStat=TnvedStat()
# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
app.add_route('/login', status)
app.add_route('/api/tnved', tnved)
app.add_route('/api/tnved/stat', tnvedStat)
