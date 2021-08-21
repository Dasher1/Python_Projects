import requests,json,urllib,sys,os
from urllib.parse import quote
s=requests.Session()

class PlayerSTB:
    def __init__(self,DNS,Mac,root="/portal.php?"):
        self.mac=Mac
        self.GuideAPI_url="http://guide.tv247.us/guide/{0}.json?_=1627352320510"
        self.User_Agent="Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3"
        self.ContentType="text/javascript;charset=UTF-8"
        self.lang="en"
        self.DNS=DNS
        self.Referer=""
        self.Accept_Encoding=""
        self.Accept="text/html, */*"
        self.mac2=quote(Mac)
        #self.mac2="00%3A1A%3A79%3AD8%3A15%3AB8;"
        self.timezone="Europe%2FParis"
        self.Cookie="mac=%s; stb_lang=%s; timezone=%s;" %(self.mac2,self.lang,self.timezone)
        self.Baseurl="http://"+DNS+root
        self.action=["get_profile","handshake","get_genres","get_main_info","get_categories","get_ordered_list","create_link","get_short_epg"]
        self.type=["itv","account_info","vod","series","stb"]
        self.JsHttpRequest="1-xml"
        self.token_url=self.Baseurl+"action="+self.action[1]+"&type="+self.type[4]+"&token=&mac="+Mac
        try:
            if "/stalker_portal/server/load.php?" in self.token_url:
                self.token_url=self.Baseurl+"type=%s&action=%s&token=&JsHttpRequest=%s&mac=%s" %(self.type[4],self.action[1],self.JsHttpRequest,self.mac)
            self.token="Bearer %s" %(requests.get(self.token_url).json()["js"]["token"])
            print(self.token)
        except:self.token=""
        self.headers2={"User-Agent":"Lavf/57.73.100","Accept":"*/*","Cookie":self.Cookie,"Content-Type":self.ContentType}
        self.headers={"Host":DNS,"User-Agent":self.User_Agent,"Content-Type":self.ContentType,"Cookie":self.Cookie,"Accept-Encoding":self.Accept_Encoding,"Accept":self.Accept,"Authorization":"%s" %(self.token),"Referer":self.Referer}
        
        #print(headers)
    #def HandShake(self):
     #   url=self.token_url
        #print(url,"\nhttp://zon2.tv/portal.php?action=handshake&type=stb&token=&mac=00:1A:79:09:17:8C")
    def GetToken(self):
        print(self.token_url)
        #if "/stalker_portal/server/load.php?" in self.token_url:
            #self.token_url=self.Baseurl+"type=%s&action=%s&token=&JsHttpRequest=%s&mac=%s" %(self.type[4],self.action[1],self.JsHttpRequest,self.mac)
        return self.token
    def Get_Profile(self):
        print(self.Baseurl)
        #http://zon2.tv/portal.php?action=handshake&type=stb&token=&mac=00:1A:79:09:17:8C
        #http://zon2.tv/stalker_portal/server/load.php?type=stb&action=handshake&token=&JsHttpRequest=1-xml&mac=00:1A:79:09:17:8C
        get_profile=self.Baseurl+"type="+self.type[4]+"&action="+self.action[0]
        req=s.get(get_profile,headers=self.headers)
        return req
    def get_genres(self):
        get_genres=self.Baseurl+"type="+self.type[0]+"&action="+self.action[2]+"&JsHttpRequest=1-xml"
        print(get_genres)
        req=s.get(get_genres,headers=self.headers)
        return req
    def get_main_info(self):
        get_main_info=self.Baseurl+"type="+self.type[1]+"&action="+self.action[3]+"&mac="+self.mac
        req=s.get(get_main_info,headers=self.headers)
        return req
    def get_categories(self):
        get_categories=self.Baseurl+"type="+self.type[2]+"&action="+self.action[4]+"&JsHttpRequest="+self.JsHttpRequest+"&mac="+self.mac
        req=s.get(get_categories,headers=self.headers)
        return req
    def get_categories_name_ID(self):
        for x in self.get_genres().json()["js"]:
            print(x["title"],x["id"])
        #self.get_genres().json()["js"][0]["title"]
    def get_categories_series(self,type=None):
        get_categories_series=self.Baseurl+"type="+self.type[3]+"&action="+self.action[4]+"&JsHttpRequest="+self.JsHttpRequest+"&mac="+self.mac
        req=s.get(get_categories_series,headers=self.headers)
        return req
    def get_ordered_list(self,genre=8,p=0,from_ch_id=0):
        get_ordered_list=self.Baseurl+"type="+self.type[0]+"&action="+self.action[5]+"&genre="+str(genre)+"&force_ch_link_check=&fav=0&sortby=number&hd=0&p="+str(p)+"&JsHttpRequest="+self.JsHttpRequest+"&from_ch_id="+str(from_ch_id)
        #print(get_ordered_list)
        req=s.get(get_ordered_list,headers=self.headers)
        return req
    def get_name_url(self,genre):
        max_page=self.get_ordered_list(genre=genre).json()["js"]["max_page_items"]
        for x in range(int(max_page)):
            for x in self.get_ordered_list(genre, p=x).json()["js"]["data"]:
                url=x["cmds"][0]["url"].replace("http : //","http://")
                #url=self.create_link(url)
                print(x["name"],url)
    def create_link(self,cmd):
        
            
        create_link=self.Baseurl+"type="+self.type[0]+"&action="+self.action[6]+"&cmd="+cmd+"&series="+"&forced_storage=0"+"&disable_ad=0"+"&download=0"+"&force_ch_link_check=0"+"&JsHttpRequest="+self.JsHttpRequest
        if "/stalker_portal/server/load.php?" in self.Baseurl:
            create_link=create_link.replace(" ","%20").replace("forced_storage=0","forced_storage=undefined")
            
            print(create_link)
        #http://starjktv.com:8080/portal.php?type=itv&action=get_short_epg&ch_id=7&size=10&JsHttpRequest=1-xml
        
        req=s.get(create_link,headers=self.headers)
        try:
            return req.json()["js"]["cmd"].split(" ")[1]
        except:
            return req.json()["js"]["cmd"]
    def Write_jsonData(self,data,filename="test3.json",):
        with open(filename,"w") as f:
            f.write(data)
    def get_PHP(self,Username="",Password=""):
        url="http://"+self.DNS+"/get.php?username="+Username+"&password="+Password+"&type=m3u"
        req=s.get(url,headers=self.headers2)
        return req
    def play_VLC(self,url):
        path="C:\\Program Files (x86)\\VideoLAN\\VLC\\"
        os.chdir(path)
        url=self.create_link(url)
        os.system('vlc "%s" :http-user-agent=Lavf/57.73.100' %(url))
        
    def play_url(self,url,Channel_name=None):
        #url=url.split(" ")[1]
        #print(url)
        #url=self.Baseurl+"type="+self.type[0]+"&action="+self.action[7]+"&ch_id=7&size=10&JsHttpRequest=1-xml"
        print(url,Channel_name)
        return url
        #print(s.get("http://localhost:8000",headers={"User-Agent":"Lavf/57.73.100","URL":""+url}).text)
        #req=s.get(url,headers=self.headers2).text
        #path="C:\\Program Files (x86)\\VideoLAN\\VLC\\"
        #os.chdir(path)
        #print(os.getcwd())
        #os.system("vlc.exe --http-user-agent 'Lavf/57.73.100' "+url)
        #print("",req)

    def root(self):
        #name="ABC"
        self.Get_Profile()
        #r=self.GuideAPI_url.format(name)
        #print(s.get(r).json())
        
        
        #self.GetToken()
        #self.HandShake()
        #req=self.get_main_info()
        
        
        #=============
        # self.Get_Profile()
        # self.get_categories_name_ID()
        # ID=input("Enter Channel ID:")
        # self.get_name_url(ID)
        # url=input("Enter Channel URL:")
        # self.play_VLC(url)
        #====================
        #print(self.get_genres().json()["js"][0]["title"])
        #self.get_categories()
        #print(self.get_categories_series().json()["js"])
        #self.get_name_url(0)

        #json_data=self.get_ordered_list(genre=13).text
        #with open("test3.json","w") as f:
         #   f.write(json_data)
        #print(json.dumps(self.get_ordered_list().json()))
        # for x in self.get_ordered_list(13, p=0).json()["js"]["data"]:
            # url=x["cmds"][0]["url"].replace("http : //","http://")
            # url=self.create_link(url)
            # print(x["name"],url)
        # for x in self.get_ordered_list(13, p=1).json()["js"]["data"]:
            # url=x["cmds"][0]["url"].replace("http : //","http://")
            # url=self.create_link(url)
            # print(x["name"],url)
        # for x in self.get_ordered_list(13, p=3).json()["js"]["data"]:
            # url=x["cmds"][0]["url"].replace("http : //","http://")
            # url=self.create_link(url)
            # print(x["name"],url)
        # for x in self.get_ordered_list(13, p=4).json()["js"]["data"]:
            # url=x["cmds"][0]["url"].replace("http : //","http://")
            # url=self.create_link(url)
            # print(x["name"],url)
        #print(self.get_genres().json()["js"])
        #get_ordered_list&genre=13&force_ch_link_check=&fav=0&sortby=number&hd=0&p=0&JsHttpRequest=1-xml&from_ch_id=0
        
        #for x in self.get_genres().json()["js"]:
           # print(x["id"])
        #print(self.get_categories_series().json()["js"])
        #for x in self.get_categories().json()["js"]:
            #print(x)
        #self.get_main_info()
        #print(self.get_main_info().text)
        #req=self.get_ordered_list()
        #x=13
        #Channel_name=req.json()["js"]["data"][x]["name"]
        #cmd2=req.json()["js"]["data"][x]["cmds"][0]["url"].replace("http : //","http://").replace(" ","%20")
        #cmd2=urllib.parse.quote_plus(cmd2)
        #json_data= json.dumps(req.json())
        #with open("test2.json","w") as f:
           #f.write(json_data)
        #link=self.create_link(cmd2)
        #return self.play_url(link,Channel_name)
mac=["00:1A:79:09:17:8C" ,"00:1A:79:09:84:02" ,"00:1A:79:09:17:8C"]
PlayerSTB("zon2.tv",mac[0],"/stalker_portal/server/load.php?").root()
#PlayerSTB("79.137.32.224","00:1A:79:10:11:12").root()
#PlayerSTB("solutionplay.xyz:8080","").get_PHP("techruthes","89951662")
#PlayerSTB("iptvkoln.net:8000","00:1A:79:02:4F:20").root()
#PlayerSTB("mag.cdn-ky.com","00:1A:79:04:15:1E").root()
#PlayerSTB("123iptv.de:88","00:1A:79:6A:1D:1E").root()
#PlayerSTB("starjktv.com:8080","00:1A:79:D8:15:B8").root()