
import xbmc,xbmcgui,xbmcaddon,xbmcvfs,xbmcplugin
from xbmcgui import ListItem
from routing import Plugin
import shutil
import json,os,sys,datetime,requests,ast
from datetime import timedelta
import requests_cache
import re
from os.path import exists
import Stalker_Client
addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo("name")
pythonV=sys.version_info[0]
if sys.version_info[0] > 2:
    import urllib
else:
    import urllib2
import Movies,Tvshows,Livetv
def BooleanCK(setting):
    t=setting[0].upper()+setting[1:len(setting)]
    return eval(t)
dialog = xbmcgui.Dialog()
profile = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
user_agent = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)'
USER_DATA_DIR = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
CACHE_TIME = int(addon.getSetting('cache_time'))
CACHE_FILE = os.path.join(USER_DATA_DIR, 'cache')
expire_after = timedelta(hours=CACHE_TIME)
debug = addon.getSetting('debug')
ServerOn = addon.getSetting('ServerOn')
Debug_reset = addon.getSetting('Debug_reset')
Upload=addon.getSetting('Upload')
DropboxUP=BooleanCK(addon.getSetting('DropboxUP'))
# if Upload=="false":
    # Upload=False
# else:
    # Upload=True


Upload=BooleanCK(Upload)
debug=BooleanCK(debug)
Debug_reset=BooleanCK(Debug_reset)
ServerOn=BooleanCK(ServerOn)
print("TESTING SETTINGS",Upload,Debug_reset)
#addon_version = addon.getAddonInfo('version')
global gLSProDynamicCodeNumber
gLSProDynamicCodeNumber=0

class LSP():
    def __init__(self):
        self.pluginName="plugin://plugin.video.Herocraft7/"
        self.home=home = xbmcvfs.translatePath(addon.getAddonInfo('path'))
        self.icon=icon = os.path.join(home, 'icon.png')
        self.source_file=source_file = os.path.join(profile, 'source_file.json')
        self.new_url_source=new_url_source =addon.getSetting('new_url_source')
        self.DNS=DNS=addon.getSetting('DNS')
        self.MAC=MAC=addon.getSetting('MAC')
        self.new_file_source=new_file_source =addon.getSetting('new_file_source')
        self.functions_dir=os.path.join(profile, 'Regex_Folder')
        self.catagorylist=["Movies","TV Shows"]
        self.BaseURL="herocraft7.ddns.net"
        self.dialog = xbmcgui.Dialog()
        try:
            self.sew = requests_cache.CachedSession(CACHE_FILE, allowable_methods='GET', expire_after=expire_after, old_data_on_error=True)
            self.sew.headers.update({'User-Agent': user_agent})
        except:
            self.addon_log("Error Code: 1")
        if not os.path.exists(profile):
            os.mkdir(profile)
        if os.path.exists(source_file)==True:
            self.SOURCES = open(source_file)
        else: SOURCES = []
        ##print("SETTINGS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",new_url_source,new_file_source)
    def ON(self,title,ID,icon):
        return None
        
    def keyboard(opt):
            nameStr=""
            keyboard = xbmc.Keyboard(nameStr,'Displayed Name, %s?'%opt)
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            newStr = keyboard.getText()
            if len(newStr) == 0:
                return
    def pf(self,string,*args):
        if bool(debug):
            print("DEBUG:"+str(debug))
            print(string,args)
    @plugin.route("/mulitlinks/<path:link>")
    def mulitlinks(link):
        try:
            expres=urllib.parse.unquote(link).split("/expres/")[1].split("/page/")[0]
            page=urllib.parse.unquote(link).split("/expres/")[1].split("/page/")[1]
            name=urllib.parse.unquote(link).split("/expres/")[0].split("/name/")[1]
            link=urllib.parse.unquote(link).split("/name/")[0]
            link=ast.literal_eval(link)
            expres=ast.literal_eval(expres)
            
        except:
            link=ast.literal_eval(urllib.parse.unquote(link))
            
        #print("multilink unpack",expres,type(expres))
        if len(link) > 1:
            selected=[]
            ret = dialog.select("Choose Stream", link)
            link=link[ret]
            try:
                link=LSP().doregex(name,expres,page,link)
            except:
                pass
            xbmc.Player().play(link)
        #pass
    def getitem(self,cat):
        if cat=="remove" or cat=="refresh":
            return ""
        else:
            info=self.Read_SourceFile()
            url=info[int(cat)]['url']
            return url
            
    def addDIR(self,title,url,fanart=''):
        list_items=[]
        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': self.icon})
        list_items.append((url, li, True))
        xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
        return xbmcplugin.addDirectoryItems(plugin.handle, list_items)



    def remove_allFile_(self):
        import os, re, os.path
        for root, dirs, files in os.walk(self.functions_dir):
            for file in files:
                os.remove(os.path.join(root, file))


#========================================================================================

    def import_by_string(self,full_name,filenamewithpath):
        try:
            
            import importlib
            return importlib.import_module(full_name, package=None)
        except:
            import imp
            return imp.load_source(full_name,filenamewithpath)


    def doEvalFunction(self,fun_call,page_data="",Cookie_Jar="",m=""):
        #print("doEvalFunction::::",fun_call,type(fun_call))
        global gLSProDynamicCodeNumber
        gLSProDynamicCodeNumber=gLSProDynamicCodeNumber+1
        ret_val=''
        if self.functions_dir not in sys.path:
            sys.path.append(self.functions_dir)
        try:
            os.mkdir(self.functions_dir)
        except:pass
        filename='LSProdynamicCode%s.py'%str(gLSProDynamicCodeNumber)
        filenamewithpath=os.path.join(self.functions_dir,filename)
        f=open(filenamewithpath,"w")
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(fun_call);
        f.close()
        ##print('before do')
        LSProdynamicCode = self.import_by_string(filename.split('.')[0],filenamewithpath)
        try:### ERROR IN REGEX Handler
            ret_val=LSProdynamicCode.GetLSProData(page_data,Cookie_Jar,m)
        except Exception as e:
            xbmc.log("Error trying to format string for log")
        return ret_val



    def raw_string(self,s):
        return s.encode('latin1', 'backslashreplace').decode('unicode-escape')
    def doregex(self,name,expres,page,link):
        expres=expres['__cdata']
        expres=urllib.parse.unquote(expres)
        expres=self.raw_string(expres)
        #print("REGEX!_DEBUG:",expres)
        val=self.doEvalFunction(expres,page,'','')
        link=link.replace("$doregex[" + name + "]", val)
        return link

#=======================================================================================================================



    def GetPage(self,m,data):
        pass
    def reset(self):
        self.refresh()
        if 'addon_data' in os.getcwd():
            try:
                os.remove(self.source_file)
                shutil.rmtree(self.functions_dir)
                return True
            except:
                try:
                    path=xbmc.translatePath("special://userdata/addon_data/plugin.video.Herocraft7")
                    os.chdir(path)
                    os.remove("source_file.json")
                    return True
                except:
                    try:
                        os.remove(self.source_file)
                    except:
                        if not os.path.isfile(self.source_file):
                            return True
        else:
            return False
            
        
    
    def refresh(self):
        if 'addon_data' in os.getcwd():
            try:
                os.remove("cache.sqlite")
                return True
            except:
                pass
        else:
            path=xbmc.translatePath("special://userdata/addon_data/plugin.video.Herocraft7")
            os.chdir(path)
            os.remove("cache.sqlite")
            xbmc.executebuiltin("XBMC.Notification('REPIDE','Your Cash File has Been Removed!!!!!!!!!!!!!!!!!!',time=19000)")
            return True
            try:
                path=xbmc.translatePath("special://userdata/addon_data/plugin.video.Herocraft7")
                os.chdir(path)
                os.remove("cache.sqlite")
                self.addon_log("Your Cash File has Been Removed")
                return True
            except:
                self.addon_log("Your Cash File has Not Been Removed")
                xbmc.executebuiltin("XBMC.Notification('Notification','Your Cash File has Not Been Removed!!!!!!!!!!!!!!!!!!',time=19000)")
    def Upload_SourceFile(self):
        import ftplib
        import dropbox
        if DropboxUP:
            app_token="sl.A1TRs9H9mR1uWHMuhh1RBg8txJ6sRZeAxE_Be853bwByVelwwynGqBKEevtvD-2FNmOhH98UDHseSLxA2dbKWSfNFsIApAW5MEHvZCtqT_OMwe7pvdIkFEdC7XxrThFdYXdbKR60axA4"
            dropbox_access_token= app_token    #Enter your own access token
            dropbox_path= "/Apps/Json_API/source_file.json"
            computer_path=self.source_file
            client = dropbox.Dropbox(dropbox_access_token)
            print("[SUCCESS] dropbox account linked")
            ok=client.files_upload(open(computer_path, "rb").read(), dropbox_path)
            if ok._path_lower_value.split("/")[3]=="source_file.json":
                self.dialog.notification('Herocraft7', 'Finished Uploading!',LSP().icon, 5000)
            print("TEST",ok._path_lower_value.split("/")[3]=="source_file.json")
            client.close()
        if Upload:
            try:
                session = ftplib.FTP('192.168.1.244','jack2','jack123456')
                session.cwd('/var/www/html/archive/Source_File_JSON/db')
                print(session.pwd())
                file = open(self.source_file,'rb')                  # file to send
                session.storbinary('STOR source_file.json', file)     # send the file
                file.close()                                    # close file and FTP
                session.quit()
                
                self.dialog.notification('Herocraft7', 'Finished Uploading!',LSP().icon, 5000)
            except:
                self.addon_log("Error: code:102, FTP file transfer Error")
            url ="http://"+self.BaseURL+"/archive/Source%20File%20JSON/db/"    # where i want to write
            files = {'file':('data.txt',open(self.source_file,'rb'))}
            r= requests.post(url,data={'upload_type':'standard','upload_to': '0'},files=files)
            print ("RRRRRRRRRRRRRRRRRRRRRRRRRRRRR",r.status_code)
            print (r.text)
        
    def rmSource(self,title):
        name=title
        sources = json.loads(open(self.source_file,"r").read())
        for index in range(len(sources)):
            if isinstance(sources[index], list):
                if sources[index][0] == name:
                    del sources[index]
                    b = open(self.source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
            else:
                if sources[index]['title'] == name:
                    del sources[index]
                    b = open(self.source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
        self.addon_log("%s Removed!"%(name),image="")
        xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,Removed source.,5000,"+self.icon+")")
        xbmc.executebuiltin("XBMC.Container.Refresh")
   
    def checkURL(self,url):
        s=requests.Session()
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        try:
            
            if s.get(url,headers=headers,timeout=1).status_code==200 and int(s.get(url,headers=headers).headers['Content-length'])>20:
                return True
        except:
            return False
    def addSource(self,url):
        if url is None:
            if not addon.getSetting("new_file_source") == "":
                source_url = addon.getSetting('new_file_source').decode('utf-8')
            elif not addon.getSetting("new_url_source") == "":
                source_url = addon.getSetting('new_url_source').decode('utf-8')
        else:
            source_url = url
            if source_url == '' or source_url is None:
                return ""
                
            if '/' in source_url:
                    nameStr = source_url.split('/')[-1].split('.')[0]
            if '\\' in source_url:
                nameStr = source_url.split('\\')[-1].split('.')[0]
            if '%' in nameStr:
                try:
                    nameStr = urllib.unquote_plus(nameStr)
                except:
                    nameStr = urllib.parse.quote_plus(nameStr)
            keyboard = xbmc.Keyboard(nameStr,'Displayed Name, Rename?')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            newStr = keyboard.getText()
            if len(newStr) == 0:
                return
            source_media = {}
            source_media['title'] = newStr
            source_media['url'] = source_url
            source_media['fanart'] = "#"
            if os.path.exists(self.source_file)==False:
                source_list = [{"title": "refresh", "url": "#", "fanart": "#","ID":"refresh"},{"title": "remove", "url": "#", "fanart": "#","ID":"remove"}]
                source_list.append(source_media)
                b = open(self.source_file,"w")
                b.write(json.dumps(source_list))
                b.close()
            else:
                #print(source_url)
                if self.checkURL(source_url):
                    sources = json.loads(open(self.source_file,"r").read())
                    sources.append(source_media)
                    b = open(self.source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    self.addon_log("Source URL added!")
                else:
                    self.addon_log("URl Not added")
        addon.setSetting('new_url_source', "")
        #addon.setSetting('new_file_source', "")
        #self.addon_log('Adding New Source: ')
    
    def regex(self,x,title,link,thumbnail):
        if '$doregex' in link:
            regexs=x['regex']
            name=regexs['name']
            expres=regexs['expres']
            page=regexs['page']
            if expres and '__cdata' in expres:
                link=LSP().doregex(name,expres,page,link)
                title=title+"[REGEX]"
                return link
            else:
                self.pf("NO PYTHON")
                title=title+"[REGEX]"
                return link
        
    def Parse_RAW(self,k,url):
        if 'items' in k and 'RAW' not in k:
            #print("ITEMS PARSER")
            for x in k['items']:
                title=x['title']
                thumbnail=x['thumbnail']
                link=x['link']
                try:
                    isfolder=x["isfolder"]
                    print("isfolder",isfolder)
                except:pass
                liz=xbmcgui.ListItem(title)
                liz.setArt({"thumb": thumbnail})
                if 'TSDOWNLOADER' in link:
                    link=link.replace('plugin.video.f4mTester','script.video.F4mProxy_Carft')
                ok=xbmcplugin.addDirectoryItem(plugin.handle,url=link,listitem=liz,isFolder=False)
                
        else:
            for x in k['RAW']:
                title=x['Country_name']
                items=x['items']
                url = plugin.url_for(cust_list, items=urllib.parse.quote(str(items)))
                self.addDIR(title,url)            
        xbmcplugin.endOfDirectory(plugin.handle)

    def Parse_Tvshows(self,k,url):
        for x in k["tasks"]:
            title=x['title']
            #print(title)
            link=x['link']
            thumbnail=x['thumbnail']
            if eval(x['isfolder']) and k["name"]=="TV Shows":
                link = plugin.url_for(Folder_Parse, url=urllib.parse.quote(str(link)))
                self.addDIR(title,link,thumbnail)
            #liz=xbmcgui.ListItem(title)
            #liz.setArt({"thumb": thumbnail})
            #ok=xbmcplugin.addDirectoryItem(plugin.handle,url=link,listitem=liz,isFolder=isfolder)
        xbmcplugin.endOfDirectory(plugin.handle)       
        #pass
    def Parse_Task(self,k,url,type="tasks"):
        
        for x in k[type]:
            title=x['title']
            #print(title)
            link=x['link']
            thumbnail=x['thumbnail']
            print(x)
            isfolder=False
            
            if '$doregex' in link:
                regexs=x['regex']
                name=regexs['name']
                expres=regexs['expres']
                page=regexs['page']
                if expres and '__cdata' in expres:
                    link=LSP().doregex(name,expres,page,link)
                    title=title+"[REGEX]"
                else:
                    self.pf("NO PYTHON")
                    title=title+"[REGEX1]"
            if isinstance(link,list):
                if len(link)>1:
                    try:
                        self.pf("link is list",link,title)
                        regexs=x['regex']
                        name=regexs['name']
                        expres=regexs['expres']
                        page=regexs['page']
                        link=urllib.parse.quote(str(link)+"/name/"+str(name)+"/expres/"+str(expres)+"/page/"+str(page))
                        link=self.pluginName+"/mulitlinks/"+link
                        title=title+"[Regex multi]"
                    except:
                        link=urllib.parse.quote(str(link))
                        link=self.pluginName+"/mulitlinks/"+link
                        
                else:
                    link=urllib.parse.quote(str(link))
                    link=self.pluginName+"/mulitlinks/"+link
            else:
                #if eval(x['isfolder']) and k["name"]=="TV Shows":
                 #   link = plugin.url_for(Folder_Parse, url=urllib.parse.quote(str(link)))
                 #   self.addDIR(title,link,thumbnail)
                print("testing data",title,link)
                self.pf("ONE LINK FOUND:",link)
                link=link
            #####Multilink
            print("jack1",link)
            liz=xbmcgui.ListItem(title)
            liz.setArt({"thumb": thumbnail})
            ok=xbmcplugin.addDirectoryItem(plugin.handle,url=link,listitem=liz,isFolder=isfolder)
        xbmcplugin.endOfDirectory(plugin.handle)        


        
    def addon_log(self ,string,image=""):
            __addon__ = xbmcaddon.Addon()
            __addonname__ = __addon__.getAddonInfo('name')
            time = 5000 #in miliseconds
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,string, time, self.icon))
            
            
    def Startup(self):
        s=requests.session()
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        url=["http://herocraft7.ddns.net/archive/Source_File_JSON/source_file.json","https://www.dropbox.com/s/zukfhrdvcpfm9oo/source_file.json?dl=1"]
        if bool(self.checkURL(url[0])) and ServerOn:
            #print(test1)
            if Debug_reset:
                self.refresh()
                self.reset()
            res=requests.session().get(url[0],headers=headers).text
            if pythonV<=2:
                urllib.urlretrieve(url[0], source_file)
            if  not os.path.exists(self.source_file):
                with open(self.source_file,'w') as f:
                    f.write(res)
        elif self.checkURL(url[1]):
            if Debug_reset:
                self.refresh()
                self.reset()
            res=requests.session().get(url[1],headers=headers).text
            if pythonV<=2:
                urllib.urlretrieve(url[1], source_file)
            if  not os.path.exists(self.source_file):
                with open(self.source_file,'w') as f:
                    f.write(res)
        else:
            self.addon_log("does not work!")
            self.pf("NO URL FOUND! ")

    def Read_SourceFile(self):
        with open(self.source_file,'r') as f:
            info=f.read()
        info=json.loads(info)
        return info
        
        
    def GetData(self,cat):
            print("TESTING",cat)
        # if cat=="remove":
            # nameStr=""
            # keyboard = xbmc.Keyboard(nameStr,'Displayed Name, to Remove?')
            # keyboard.doModal()
            # if (keyboard.isConfirmed() == False):
                # return
            # title = keyboard.getText()
            # self.rmSource(title)
            # self.addon_log("Your Source has Been Removed (%s)" %(title))
            # url=""
        
        # if cat=="refresh":
            # ret = dialog.yesno('Kodi', 'Do you want to clear the cache')
            # #print("DIALOG",ret)
            # if ret>0: 
                # xbmc.executebuiltin("XBMC.Notification('Warning','Your Cash File has been Removed',time=16000)")
                # ok=self.refresh()
                # if ok:
                    # self.addon_log("Your Cash File has Been Removed")
                # else:
                    # self.addon_log("Your Cash File has Not been Removed!!")
            
            # if ret==0:
                # resetYN = dialog.yesno('Kodi', 'Do you want to remove the Source File')
                # if resetYN>0:
                    # xbmc.executebuiltin("XBMC.Notification('Warning','Your Souce File has been Removed',time=11000)")
                    # ok=self.reset()
                    # if ok:
                       # print(ok)
                       # self.addon_log("Your Source File has Been Removed")
                    # else:
                        # self.addon_log("Your Source File has NOT Been Removed")

                
                    
                # url=""
            # else:
                # url=""
        #else:
            url=self.getitem(cat)
            print(url)
            if 'http://' in url or 'https://' in url:
                r=self.sew.get(url).content
                k=json.loads(r)
                if k["tasks"]:
                    self.Parse_Task(k,url)
                elif k["name"]=="TV Shows":
                    self.Parse_Tvshows(k,url)
                elif k["name"]=="Live Tv":
                    self.Parse_Task(k,url)
                elif k["name"]=="Movies":
                    self.Parse_Movies(k,url)
                elif k["name"]=="Raw":
                    self.Parse_RAW(k,url)
                elif "items" in k:
                    self.Parse_RAW(k,url)
                    
                print("KKK:",k)
                # if 'tasks' in k:
                    # #print("JSON Has tasks: 1111")
                    # self.Parse_Task(k,url)
                    # #print("JSON Has tasks:")
                    # ##print("JSON:",k)
                # elif "TV Shows" in k["name"]:
                    # self.Parse_Tvshows(k,url)
                # elif 'items' in k:
                    # self.Parse_RAW(k,url)
                    # try:
                        # if (k["name"] in self.catagorylist):
                            # self.Parse_Task(k,url,"tasks")
                            
                    # except:pass
                    
                    # self.Parse_Task(k,url,"items")
                    # #print(k)
                # elif 'RAW' in k:
                    # #print("JSON Has RAW:")
                    # ##print(k)
                    # self.Parse_RAW(k,url)
                    # #print("Json Has RAW:")
                # elif 'channels' in k:
                    # print("Json Has channels:")
            
            
            
            
#LSP().pf("TESTING DEBUG PRINT FUCNTION")

@plugin.route("/Folder_Parse/<path:url>")
def Folder_Parse(url):
        s=requests.Session()
        url=urllib.parse.unquote(url).split("?")
        session=eval(url[1].split("=")[1])
        url=url[0]
        
        #session=urllib.parse.unquote(url).split("?")[1]
        print("JSON_URL",session)
        r=self.sew.get(url).content
        json_text=json.loads(r)
        name=json_text["name"].replace("_"," ")
        items=json_text["tasks"]
        total=len(items)
        print("testing json2",items)
        for x in items:
            title=name+" "+x['title']
            link=x['link']
            thumbnail=x['thumbnail']
            if "$doregex" in link:
                regexs=x['regex']
                name=regexs['name']
                expres=regexs['expres']
                page=regexs['page']
                if expres and '__cdata' in expres:
                    link=LSP().doregex(name,expres,page,link)
                    title=title+"[REGEX]"
                else:
                    print("ELSEDDD",expres)
            liz=xbmcgui.ListItem(title)
            liz.setArt({"thumb": thumbnail})
            ok=xbmcplugin.addDirectoryItem(plugin.handle,url=link,listitem=liz,totalItems=total,isFolder=False)
        xbmcplugin.endOfDirectory(plugin.handle)
    #print("folder_Parse",url)


@plugin.route("/cust_list/<path:items>")
def cust_list(items=None):
    items=urllib.parse.unquote(items)
    items=ast.literal_eval(items)
    total=len(items)
    for x in items:
        title=x['title']
        link=x['link']
        thumbnail=x['thumbnail']
        if "$doregex" in link:
            regexs=x['regex']
            name=regexs['name']
            expres=regexs['expres']
            page=regexs['page']
            if expres and '__cdata' in expres:
                link=LSP().doregex(name,expres,page,link)
                title=title+"[REGEX]"
            else:
                print("ELSEDDD",expres)
        liz=xbmcgui.ListItem(title)
        liz.setArt({"thumb": thumbnail})
        ok=xbmcplugin.addDirectoryItem(plugin.handle,url=link,listitem=liz,totalItems=total,isFolder=False)
    xbmcplugin.endOfDirectory(plugin.handle)


            

@plugin.route("/list_channels/<cat>")
def list_channels(cat=None):
    e=LSP().GetData(cat)
@plugin.route("/")
def root():
    #if Upload:
        #LSP().Upload_SourceFile()
    list_items=[]
    info=LSP().Read_SourceFile()
    showcontext="source"
    contextMenu =[]
    Length=len(info)
    scr=ast.literal_eval(str(LSP().SOURCES))
    for x in range(0,Length):
        title=info[x]['title']
        url=info[x]['url']
        fanart=info[x]['fanart']
        s=requests.Session()
        if url=="#":
            fanart=info[x]['fanart']
            ID=x
            LSP().ON(title,x,fanart)
        if url.startswith("http://") or url.startswith("https://"):
            try:
                if (self.sew.get(url, timeout=0.5).status_code==200):
                    fanart=info[x]['fanart']
                    ID=x
                    LSP().ON(title,x,fanart)
            except:
                pass
                #LSP().refresh()
                #LSP().reset()
        
        if scr[x]['title'] in title:
            #print("testing %s     %s"%(scr[ID]['title'],title))
            LSP().pf("YEST",scr[x]['title'],title)
            
        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': fanart})
        url = plugin.url_for(list_channels,cat=x)
        li.addContextMenuItems(contextMenu[-1:])
        list_items.append((url, li, True))
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
    








@plugin.route("/?mode=<mode>/path:name")    
def mode_opt_args(mode,title=""):
    if mode==7:
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
    if mode==8:
        addon_log("rmSource")
        print("REMOVEEEEEEEEEEEEEEEEEEEEEEEEE")
        LSP().rmSource(title)
    
@plugin.route("/mode/<mode>")    
def mode_opt(mode,title=""):
    dialog = xbmcgui.Dialog()
    print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",mode,title)
    if int(mode)==1:pass # check Mode
    elif int(mode)==2:
        print("ADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,New source added.,5000,"+LSP().icon+")")
        LSP().addSource(LSP().new_url_source)# Add Source
    elif int(mode)==3:pass # Remove source
    elif int(mode)==4:# clear CACHE_FILE
        ok=LSP().reset()
        if ok:
            dialog = xbmcgui.Dialog()
            dialog.notification('Herocraft7', 'You Cash Reseted the Addon Data',LSP().icon, 5000)# reset
    elif int(mode)==5:pass
    elif int(mode)==6:# Stalker_Client
        #try:
        MAC_=LSP().MAC
        DNS_=LSP().DNS
        mac_validation = bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', MAC_.lower()))
        if mac_validation:
            import Stalker_Client
            PlayerSTB(DNS_,MAC_,"/stalker_portal/server/load.php?").root()
            print("works",DNS_)
        else:
            dialog.notification('Herocraft7', 'Not a valid MAC!',LSP().icon, 5000)
                
            #print(mac_validation)
            #import Stalker_Client
            
        #except:
            #dialog = xbmcgui.Dialog()
            #dialog.notification('Herocraft7', 'Stalker_Client Not Installed!',LSP().icon, 5000)
    elif int(mode)==7:pass # debug
    elif int(mode)==8:pass # run Plugin
    elif int(mode)==9: # Refresh
        path=xbmc.translatePath("special://userdata/addon_data/plugin.video.Herocraft7")
        path=path+"/cache.sqlite"
        if exists(path):
            ok=LSP().refresh()
            ok=True
            if ok:
                dialog = xbmcgui.Dialog()
                dialog.notification('Herocraft7', 'Your Cash File has been Removed',LSP().icon, 5000)
                xbmc.executebuiltin("XBMC.Notification('Warning','Your Cash File has been Removed',time=16000)")
    elif int(mode)==10: # Upload File
        LSP().Upload_SourceFile()
    #else:
        #pass
    #print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",mode,title)
    # if int(mode)==7:
        # print("ADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        # xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,New source added.,5000,"+LSP().icon+")")
        # LSP().addSource(LSP().new_url_source)
    # elif int(mode)==12:
        # print("Reset")
        # ok=LSP().reset()
        # if ok:
            # dialog = xbmcgui.Dialog()
            # dialog.notification('Herocraft7', 'You Cash Reseted the Addon Data',LSP().icon, 5000)
    #elif int(mode)==10:
        #LSP().Upload_SourceFile()
    # elif int(mode)==11:
        # path=xbmc.translatePath("special://userdata/addon_data/plugin.video.Herocraft7")
        # path=path+"/cache.sqlite"
        # if exists(path):
            # ok=LSP().refresh()
            # ok=True
            # if ok:
                # dialog = xbmcgui.Dialog()
                # dialog.notification('Herocraft7', 'Your Cash File has been Removed',LSP().icon, 5000)
                # xbmc.executebuiltin("XBMC.Notification('Warning','Your Cash File has been Removed',time=16000)")

    elif int(mode)==19:
        addon_log("Genesiscommonresolvers")
        playsetresolved (urlsolver(url),name,iconimage,True)
    
LSP().Startup()
if __name__ == "__main__":
    plugin.run(sys.argv)
