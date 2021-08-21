"""
#import uuid
#from hashlib import md5
#from base64 import b64encode, b64decode, urlsafe_b64encode
#from itertools import chain
#from resources.modules.req_class import reqe
#from urllib.request import urlretrieve
#import string
#import random
#from class_Iptv import *
#import time
#from Session import CachedSession
#from Handler import run_link
#import io
"""
import xbmc,xbmcgui,xbmcaddon,xbmcvfs,xbmcplugin
from xbmcgui import ListItem
from routing import Plugin
import shutil
#import urllib.request, urllib.parse, urllib.error
try:
    import urllib
except:
    import urllib2


import json,os,sys,datetime,requests,ast
from datetime import timedelta
import requests_cache
addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo("name")
dialog = xbmcgui.Dialog()
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
user_agent = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)'
USER_DATA_DIR = xbmc.translatePath(addon.getAddonInfo('profile'))
CACHE_TIME = int(addon.getSetting('cache_time'))
CACHE_FILE = os.path.join(USER_DATA_DIR, 'cache')
expire_after = timedelta(hours=CACHE_TIME)
debug = addon.getSetting('debug')
ServerOn = addon.getSetting('ServerOn')
#print("DEBUG_STATUS",debug)
#sew = requests_cache.CachedSession(CACHE_FILE, allowable_methods='GET', expire_after=expire_after, old_data_on_error=True)
#sew.headers.update({'User-Agent': user_agent})

addon_version = addon.getAddonInfo('version')
#from urllib.request import urlretrieve

global gLSProDynamicCodeNumber
gLSProDynamicCodeNumber=0
class LSP():
    def __init__(self):
        self.pluginName="plugin://plugin.video.Herocraft7/"
        self.home=home = xbmc.translatePath(addon.getAddonInfo('path'))
        self.icon=icon = os.path.join(home, 'icon.png')
        self.source_file=source_file = os.path.join(profile, 'source_file.json')
        self.new_url_source=new_url_source =addon.getSetting('new_url_source')
        self.new_file_source=new_file_source =addon.getSetting('new_file_source')
        self.functions_dir=os.path.join(profile, 'Regex_Folder')
        self.mode=None
        self.catagorylist=["Movies","TV Shows"]
        #self.functions_dir=functions_dir = os.path.join(profile, 'my_folder')
        #functions_dir='my_folder'+self.profile
        try:
            self.sew = requests_cache.CachedSession(CACHE_FILE, allowable_methods='GET', expire_after=expire_after, old_data_on_error=True)
            self.sew.headers.update({'User-Agent': user_agent})
        except:
            self.addon_log("Error Code: 1")
        if not os.path.exists(profile):
            os.mkdir(profile)
        if os.path.exists(source_file)==True:
            self.SOURCES = open(source_file).read()
        else: SOURCES = []
        print("SETTINGS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",new_url_source,new_file_source)
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
        #self.string=string
        if bool(debug):
            print("DEBUG:"+str(debug))
            print(string,args)
    @plugin.route("/mulitlinks/<path:link>")
    def mulitlinks(link):
        #print("eeeeeeeeeeeeeeeeeeeee",link,sys.argv)
        link=ast.literal_eval(urllib.parse.unquote(link))
        print(link)
        if len(link) > 1:
            selected=[]
            ret = dialog.select("Choose Stream", link)
            link=link[ret]
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
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)



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
    #    print 'doEvalFunction'
        #try:
        print("doEvalFunction::::",fun_call,type(fun_call))
        global gLSProDynamicCodeNumber
        gLSProDynamicCodeNumber=gLSProDynamicCodeNumber+1
        ret_val=''
        #print('doooodoo')
        if self.functions_dir not in sys.path:
            sys.path.append(self.functions_dir)
        try:
            os.mkdir(self.functions_dir)
        except:pass
        filename='LSProdynamicCode%s.py'%str(gLSProDynamicCodeNumber)
        filenamewithpath=os.path.join(self.functions_dir,filename)
        #print(filenamewithpath)
        f=open(filenamewithpath,"w")
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(fun_call);
        f.close()
        #print('before do')
        LSProdynamicCode = self.import_by_string(filename.split('.')[0],filenamewithpath)
        try:### ERROR IN REGEX Handler
            ret_val=LSProdynamicCode.GetLSProData(page_data,Cookie_Jar,m)
        except Exception as e:
            xbmc.log("Error trying to format string for log")
            #self.addon_log("Error on Regex 4")
        return ret_val
        #print('after',ret_val)



    def raw_string(self,s):
        return s.encode('latin1', 'backslashreplace').decode('unicode-escape')
    def doregex(self,name,expres,page,link):
        #from RegexParser import Regex_Parser
        #parserRegex=Regex_Parser()
        expres=expres['__cdata']
        expres=urllib.parse.unquote(expres)
        expres=self.raw_string(expres)
        #expres=r'{}'.format(expres) 
        print("REGEX!_DEBUG:",expres)
        
        val=self.doEvalFunction(expres,page,'','')
        #print("LINK",val)
        link=link.replace("$doregex[" + name + "]", val)
        #print("DONE",val,link)
        #item_list.append([title,val,thumbnail])
        return link

#=======================================================================================================================



    def GetPage(self,m,data):
        pass
    def reset(self):
        if 'addon_data' in os.getcwd():
            try:
                os.remove("source_file")
                shutil.rmtree(self.functions_dir)
                return True
            except:
                pass
        else:
            path=xbmc.translatePath("special://userdata/addon_data/plugin.video.Herocraft7")
            os.chdir(path)
            os.remove("source_file")
            #self.functions_dir.rmdir()
            #shutil.rmtree(path+"/Regex_Folder")
            
        
    
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
            try:
                path=xbmc.translatePath("special://userdata/addon_data/plugin.video.Herocraft7")
                os.chdir(path)
                os.remove("cache.sqlite")
                self.addon_log("Your Cash File has Been Removed")
            except:
                self.addon_log("Your Cash File has Not Been Removed")
                xbmc.executebuiltin("XBMC.Notification('Notification','Your Cash File has Not Been Removed!!!!!!!!!!!!!!!!!!',time=19000)")
                #print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    
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
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        try:
            if requests.get(url,headers=headers).status_code==200:
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
                print(source_url)
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
    
    
    
    def Parse_RAW(self,k,url):
        if 'items' in k and 'RAW' not in k:
            print("ITEMS PARSER")
            for x in k['items']:
                title=x['title']
                thumbnail=x['thumbnail']
                link=x['link']
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
        
    def Parse_Task(self,k,url,type="tasks"):
        for x in k[type]:
            title=x['title']
            print(title)
            link=x['link']
            thumbnail=x['thumbnail']
            
            
            if '$doregex' in link:
                regexs=x['regex']
                name=regexs['name']
                
                expres=regexs['expres']
                page=regexs['page']
                
                if expres and '__cdata' in expres:
                    link=LSP().doregex(name,expres,page,link)
                    title=title+"[REGEX]"
                    #print("DOREGEX",title,regexs)
                else:
                    #print("NO PYTHON")
                    self.pf("NO PYTHON")
                
                #link=self.doregex(title,link,regexs)
                    title=title+"[REGEX]"
            liz=xbmcgui.ListItem(title)
            liz.setArt({"thumb": thumbnail})
            #print("DEBUG:ERROR",title,type(link),link)
            if isinstance(link,list):
                if len(link)>1:
                    self.pf("link is list")
                    #print("link is list")
                    link=urllib.parse.quote(str(link))
                    link=self.pluginName+"/mulitlinks/"+link
                else:
                    self.pf("ONE LINK FOUND:",link)
                    #print("ONE LINK FOUND:",link)
                    link=link[0]
            #####Multilink
            ok=xbmcplugin.addDirectoryItem(plugin.handle,url=link,listitem=liz,isFolder=False)
        xbmcplugin.endOfDirectory(plugin.handle)            
    def addon_log(self ,string,image=""):
            __addon__ = xbmcaddon.Addon()
            __addonname__ = __addon__.getAddonInfo('name')
            #print("ICONNNNNNNNNNNNNNN",self.icon)
            time = 5000 #in miliseconds
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,string, time, self.icon))
            
            
    def Startup(self):
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        print("new_file_source",self.source_file)
        #print("DEBUG_STATUS",self.debug)
        url=["http://herocraft7.ddns.net/archive/Source%20File%20JSON/source_file.json","http://tiny.cc/Source_F"]
        if bool(self.checkURL(url[0])) and ServerOn:
            #self.addon_log("works! 1"+ServerOn+"bool:"+str(bool(self.checkURL(url[1]))))
            res=requests.session().get(url[0],headers=headers).text
        elif self.checkURL(url[1]):
            #self.addon_log("works! 222"+ServerOn+"bool:"+str(bool(self.checkURL(url[0]))))
            res=requests.session().get(url[1],headers=headers).text
        else:
            self.addon_log("does not work!")
        
        
        #res=requests.session().get(url[0],headers=headers).text
        if  not os.path.exists(self.source_file):
            try:
                with open(self.source_file,'w') as f:
                    f.write(res)
            except:
                self.addon_log("Error Code: 1.1")
                try:
                    urllib.urlretrieve(url[0], source_file)
                except:
                    #self.addon_log("Error Code: 1.2")
                    try:
                        urllib.urlretrieve(url[1], source_file)
                    except:
                        self.addon_log("Error Code: 1.2")
            
            
            # print(self.source_file)
            # try:
                # try:
                    # print("TESTING")
                    # print()
                    
                    # urllib.urlretrieve(url[0], source_file)
                # except:
                    
                    # res=json.loads(res)
                    # print("ADD",res)
                    # #f=open(self.source_file,'w')
                    # with open(self.source_file,'w') as f:
                        # f.write(res)
            # except:
                # self.addon_log("Error Code: 1.1")
                
    def Read_SourceFile(self):
        with open(self.source_file,'r') as f:
            info=f.read()
        info=json.loads(info)
        return info
        
        
    def GetData(self,cat):
        self.pf("CATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT    %s %s" %(cat,type(cat)))
        #print("CATTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT    %s %s" %(cat,type(cat)))
        if cat=="remove" or cat=="0":
            nameStr=""
            keyboard = xbmc.Keyboard(nameStr,'Displayed Name, to Remove?')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            title = keyboard.getText()
            self.rmSource(title)
            self.addon_log("Your Source has Been Removed (%s)" %(title))
            url=""
        
        if cat=="refresh" or cat=='1':
            ret = dialog.yesno('Kodi', 'Do you want to clear the cache')
            print("DIALOG",ret)
            if ret>0: 
                xbmc.executebuiltin("XBMC.Notification('Warning','Your Cash File has been Removed',time=16000)")
                ok=self.refresh()
                if ok:
                    self.addon_log("Your Cash File has Been Removed")
                else:
                    self.addon_log("Your Cash File has Not been Removed!!")
            
            elif ret==0:
                resetYN = dialog.yesno('Kodi', 'Do you want to remove the Source File')
                if resetYN>0:
                    xbmc.executebuiltin("XBMC.Notification('Warning','Your Souce File has been Removed',time=16000)")
                    ok=self.reset()
                    if ok:
                       self.addon_log("Your Source File has Been Removed")

                
                    
                url=""
            else:
                url=""
        else:
            url=self.getitem(cat)
            if 'http://' in url or 'https://' in url:
                r=self.sew.get(url).content
                k=json.loads(r)
                if 'tasks' in k:
                    print("JSON Has tasks: 1111")
                    self.Parse_Task(k,url)
                    print("JSON Has tasks:")
                    #print("JSON:",k)
                elif 'items' in k:
                    self.Parse_RAW(k,url)
                    try:
                        if (k["name"] in self.catagorylist):
                            self.Parse_Task(k,url,"tasks")
                            
                    except:pass
                    
                    self.Parse_Task(k,url,"items")
                    print(k)
                elif 'RAW' in k:
                    print("JSON Has RAW:")
                    #print(k)
                    self.Parse_RAW(k,url)
                    print("Json Has RAW:")
                elif 'channels' in k:
                    print("Json Has channels:")
            
            
            
            
LSP().pf("TESTING DEBUG PRINT FUCNTION")
@plugin.route("/cust_list/<path:items>")
def cust_list(items=None):
    items=urllib.parse.unquote(items)
    items=ast.literal_eval(items)
    total=len(items)
    for x in items:
        title=x['title']
        link=x['link']
        thumbnail=x['thumbnail']
        
        print("Playlist!",link)
        if "$doregex" in link:
            print("Regex has Item")
            regexs=x['regex']
            name=regexs['name']
            expres=regexs['expres']
            page=regexs['page']
            print(expres)
            if expres and '__cdata' in expres:
                link=LSP().doregex(name,expres,page,link)
                title=title+"[REGEX]"
            else:
                print("ELSEDDD",expres)
        liz=xbmcgui.ListItem(title)
        liz.setArt({"thumb": thumbnail})
        ok=xbmcplugin.addDirectoryItem(plugin.handle,url=link,listitem=liz,totalItems=total,isFolder=False)
    xbmcplugin.endOfDirectory(plugin.handle)
    print('EOFError',type(items),items)

            

@plugin.route("/list_channels/<cat>")
def list_channels(cat=None):
    #LSP.pf("pppppppppppppppppppppppppp",cat)
    print("pppppppppppppppppppppppppp",cat)
    e=LSP().GetData(cat)

#def add(title,thumbnail,li)    
@plugin.route("/")
def root():
    list_items=[]
    #print("PROFILE",profile)
    info=LSP().Read_SourceFile()
    showcontext="source"
    contextMenu =[]
    Length=len(info)
    scr=ast.literal_eval(str(LSP().SOURCES))
    for x in range(0,Length):
        title=info[x]['title']
        url=info[x]['url']
        s=requests.Session()
        if url=="#":
            fanart=info[x]['fanart']
            ID=x
            LSP().ON(title,ID,fanart)
        if url.startswith("http://") or url.startswith("https://"):
            if (s.get(url).status_code==200):
                fanart=info[x]['fanart']
                ID=x
                LSP().ON(title,ID,fanart)
        
       # print("SOURCES",ID)
        if scr[ID]['title'] in title:
            print("testing %s     %s"%(scr[ID]['title'],title))
            LSP().pf("YEST",scr[ID]['title'],title)
            #print("YEST",scr[ID]['title'],title)
            #print(contextMenu[-1:],title)
            #contextMenu.append(('Remove from Sources','XBMC.RunPlugin(%s?mode=8&name=%s)' %(sys.argv[0], urllib.parse.quote_plus(title))))
            
        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': fanart})
        url = plugin.url_for(list_channels,cat=ID)
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
    print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",mode,title)
    if int(mode)==7:
        print("ADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,New source added.,5000,"+LSP().icon+")")
        LSP().addSource(LSP().new_url_source)
    elif int(mode)==10:
        LSP().
    elif mode==19:
        addon_log("Genesiscommonresolvers")
        playsetresolved (urlsolver(url),name,iconimage,True)


LSP().Startup()
if __name__ == "__main__":
    plugin.run(sys.argv)
