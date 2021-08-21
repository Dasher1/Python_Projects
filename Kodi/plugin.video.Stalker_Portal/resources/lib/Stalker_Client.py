import requests,json,urllib,sys,os
import tempfile,shutil
import requests_cache
try:
    from urllib import quote,unquote  # Python 2.X
except ImportError:
    from urllib.parse import quote,unquote  # Python 3
from xbmcvfs import translatePath
import xbmcaddon
addon = xbmcaddon.Addon()
USER_DATA_DIR = translatePath(addon.getAddonInfo('profile'))
CACHE_FILE = os.path.join(USER_DATA_DIR, 'cache')
def get_PHP(DNS,Username="",Password=""):
    url="http://"+DNS+"/get.php?username="+Username+"&password="+Password+"&type=m3u"
    #print(url)
    response = requests.get(url, stream=True)
    handle = open("test309.m3u", "wb")
    for chunk in response.iter_content(chunk_size=660):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
class PlayerSTB:
    def __init__(self,DNS,Mac,root="/portal.php?"):
        self.s=requests.Session()
        self.mac=Mac
        self.User_Agent="Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3"
        self.ContentType="text/javascript;charset=UTF-8"
        self.lang="en"
        self.DNS=DNS
        self.Referer=""
        self.Accept_Encoding=""
        self.Accept="text/html, */*"
        self.session = requests_cache.CachedSession(CACHE_FILE, allowable_methods='GET', expire_after=8, old_data_on_error=True)
        self.mac2=quote(Mac.encode("utf-8"))
        self.timezone="Europe%2FParis"
        self.Cookie="mac=%s; stb_lang=%s; timezone=%s;" %(self.mac2,self.lang,self.timezone)
        if not DNS.startswith("http://"):
            self.Baseurl="http://"+DNS+root
        else:
            self.Baseurl=DNS+root
        self.action=["get_profile","handshake","get_genres","get_main_info","get_categories","get_ordered_list","create_link","get_short_epg"]
        self.type=["itv","account_info","vod","series","stb"]
        self.JsHttpRequest="1-xml"
        self.token_url=self.Baseurl+"action="+self.action[1]+"&type="+self.type[4]+"&token=&mac="+Mac
        #print(self.token_url)
        try:
            if "/stalker_portal/server/load.php?" in self.token_url:
                self.token_url=self.Baseurl+"type=%s&action=%s&token=&JsHttpRequest=%s&mac=%s" %(self.type[4],self.action[1],self.JsHttpRequest,self.mac)
                print("Error: 1 in __init__",self.token)
            self.token="Bearer %s" %(self.session.get(self.token_url).json()["js"]["token"])
            
        except:self.token=""
        self.headers2={"User-Agent":"Lavf/57.73.100","Accept":"*/*","Cookie":self.Cookie,"Content-Type":self.ContentType}
        self.headers={"Host":DNS,"User-Agent":self.User_Agent,"Content-Type":self.ContentType,"Cookie":self.Cookie,"Accept-Encoding":self.Accept_Encoding,"Accept":self.Accept,"Authorization":"%s" %(self.token),"Referer":self.Referer}
    
    
    
    
    def SetTimeZone(self,timezone):
        self.timezone=quote(timezone)
    def SetUserAgent(self,User_Agent):
        self.User_Agent=User_Agent
    def SetToken(self,token):
        self.token="Bearer %s" %(token)
    def getHeader(self):
        return self.headers
    def updateHeader(self,key,value):
        self.headers.update({key:value})
        print(self.getHeader())
    def GetToken(self):
        return self.token
    def Get_Profile(self):
        get_profile=self.Baseurl+"type="+self.type[4]+"&action="+self.action[0]
        req=self.session.get(get_profile,headers=self.headers)
        return req
    def get_genres(self):
        get_genres=self.Baseurl+"type="+self.type[0]+"&action="+self.action[2]+"&JsHttpRequest=1-xml"
        #print("test",get_genres)
        req=self.session.get(get_genres,headers=self.headers)
        return req
    def get_main_info(self):
        get_main_info=self.Baseurl+"type="+self.type[1]+"&action="+self.action[3]+"&mac="+self.mac
        req=self.session.get(get_main_info,headers=self.headers)
        if req.status_code==200:
            return req
        else:
            print(get_main_info,req.text)
    def get_categories(self):
        get_categories=self.Baseurl+"type="+self.type[2]+"&action="+self.action[4]+"&JsHttpRequest="+self.JsHttpRequest+"&mac="+self.mac
        req=self.session.get(get_categories,headers=self.headers)
        return req
    def get_categories_name_ID(self):
        categories=[]
        #try:
        #print(self.get_genres())
        for x in self.get_genres().json()["js"]:
            categories.append([x["title"],x["id"]])
        return categories
    def get_categories_series(self,type=None):
        get_categories_series=self.Baseurl+"type="+self.type[3]+"&action="+self.action[4]+"&JsHttpRequest="+self.JsHttpRequest+"&mac="+self.mac
        req=self.session.get(get_categories_series,headers=self.headers)
        return req
    def get_ordered_list(self,genre=8,p=0,from_ch_id=0):
        get_ordered_list=self.Baseurl+"type="+self.type[0]+"&action="+self.action[5]+"&genre="+str(genre)+"&force_ch_link_check=&fav=0&sortby=number&hd=0&p="+str(p)+"&JsHttpRequest="+self.JsHttpRequest+"&from_ch_id="+str(from_ch_id)
        req=self.session.get(get_ordered_list,headers=self.headers)
        return req
    def get_name_url(self,genre):
        channel_url=[]
        max_page=self.get_ordered_list(genre=genre).json()["js"]["max_page_items"]
        for x in range(int(max_page)):
            for x in self.get_ordered_list(genre, p=x).json()["js"]["data"]:
                url=x["cmds"][0]["url"].replace("http : //","http://")
                channel_url.append([x["name"],url])
        return channel_url
                
    def create_link(self,cmd):
        create_link=self.Baseurl+"type="+self.type[0]+"&action="+self.action[6]+"&cmd="+cmd+"&series="+"&forced_storage=0"+"&disable_ad=0"+"&download=0"+"&force_ch_link_check=0"+"&JsHttpRequest="+self.JsHttpRequest
        if "/stalker_portal/server/load.php?" in self.Baseurl:
            create_link=create_link.replace(" ","%20").replace("forced_storage=0","forced_storage=undefined")
            
            #print(create_link)      
        req=self.session.get(create_link,headers=self.headers)
        try:
            return req.json()["js"]["cmd"].split(" ")[1]
        except:
            return req.json()["js"]["cmd"]
    def Write_jsonData(self,data,filename="test3.json",):
        with open(filename,"w") as f:
            f.write(data)
    def play_VLC(self,url):
        url=self.create_link(url)
        return url+"|User-Agent=Lavf/57.73.100 Connection=keep-alive"
        
    def play_url(self,url,Channel_name=None):
        #print(url,Channel_name)
        url=self.create_link(url)
        return url


