
import xbmc,xbmcgui,xbmcaddon,xbmcvfs,xbmcplugin
from xbmcgui import ListItem
from routing import Plugin
from Stalker_Client import PlayerSTB
import os,json,requests
from os.path import exists
try:
    from urllib import quote,unquote  # Python 2.X
except ImportError:
    from urllib.parse import quote,unquote  # Python 3
dialog = xbmcgui.Dialog()
plugin = Plugin()
addon = xbmcaddon.Addon()
Dropbox=addon.getSetting('Dropbox')
if Dropbox=="true":
    Dropbox=True
else:
    Dropbox=False
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
#"00:1A:79:04:15:1E"
#"mag.cdn-ky.com"
Player=None
try:
    addon_dir=xbmc.translatePath(addon.getAddonInfo("path")).decode('utf-8')
except:
    addon_dir=xbmc.translatePath(addon.getAddonInfo("path"))
DNS=None
Mac=None
New_URL=[]
dropbox_file = os.path.join(profile, 'Dropbox.json')

        
        
def CreateLink(url,title="",streamtype="HLS",thumb="#",Headers="|User-Agent=Lavf/57.73.100"):
    url=quote(url+"&title="+title+"&StreamType="+streamtype+"&thumb="+thumb+"&Headers="+Headers)
    return url
def create_SourceFile(source_file=None,data=None):
    print(source_file)
    #try:
    os.mkdir(profile)
    with open(source_file,"w+") as f:
        json_string = json.dumps(data)
        f.write(json_string)
def write_SourceFile(source_file,data):
    data=json.dumps(data)
    with open(source_file,"w+") as f:
        f.write(data)
def read_SourceFile(source_file):
    with open(source_file,"r+") as f:
        data=f.read()
        return data
def append_SourceFile(source_file,dataAppend):
    data=read_SourceFile(source_file)
    if len(data)==0:
        write_SourceFile(source_file,dataAppend)
    else:
        data=json.loads(data)
        if dataAppend in data:
            print("test333333:",data)
            dialog.notification('Stalker Portal', 'DNS Exist alreday!',os.path.join(addon_dir, 'icon.png'), 1500)
        elif dataAppend=="":
            dialog.notification('Stalker Portal', 'Cant Add',os.path.join(addon_dir, 'icon.png'), 1500)
        else:
            dialog.notification('Stalker Portal', 'DNS and Mac Enterted!',os.path.join(addon_dir, 'icon.png'), 1500)
            data["URL"].append(dataAppend)
            write_SourceFile(source_file,data)
            print("appendTest",data)
            dialog.notification(addon.getAddonInfo('name'), 'Dropbox URl added',os.path.join(addon_dir, 'icon.png'), 1500)


@plugin.route("/Path/<path:url>")
def Path(url):
    url=unquote(url)
    url=url.split("?DNS=")
    DNS=url[0]
    Mac=url[1]
    list_items=[]
    player=PlayerSTB(DNS,Mac)
    player.Get_Profile()
    works=False
    try:
        get_categories_name_ID=player.get_categories_name_ID()
        works+=True
    except:
        dialog.notification('Stalker Portal', 'DNS OR Mac Are Not valid!',os.path.join(addon_dir, 'icon.png'), 1500)
    if works:
        for x in get_categories_name_ID:
            title=x[0].encode('utf-8')
            ID=x[1]
            fanart="#"
            cat=quote("?ID="+ID+"&Mac="+Mac+"&DNS="+DNS)
            url = plugin.url_for(list_channels,cat)
            #print("URL:",url)
            li = xbmcgui.ListItem(title)
            li.setArt({'thumb': fanart})
            list_items.append((url, li, True))
        xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
        xbmcplugin.addDirectoryItems(plugin.handle, list_items)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)





def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    raise Exception("This Data is not JSON",myjson)
    return False
  return True
@plugin.route("/Dropbox/<path:url>")
def Dropbox(url):
    list_items=[]
    url=unquote(url)
    data=requests.get(url).json()
    for x in data:
        title=x["DNS"]
        url=quote(x["DNS"]+"?DNS="+x["Mac"])
        url=plugin.url_for(Path,url)
        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': "#"})
        list_items.append((url, li, True))
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)




def addFolder(data,thumb="#"):
    list_items=[]
    for x in data:
        title=x["DNS"]
        url=quote(x["DNS"]+"?DNS="+x["Mac"])
        url=plugin.url_for(Path,url)
        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': thumb})
        list_items.append((url, li, True))
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)




@plugin.route("/")
def root():
    list_items=[]
    file_exists2 = exists(dropbox_file)
    if not file_exists2:
        
        data={"URL":[]}
        create_SourceFile(dropbox_file,data)
    else:
        data=read_SourceFile(dropbox_file)
        if Dropbox:
            print("DATA:",len(data))
            if len(data)>10 and is_json(data):
                data=json.loads(data)
                urls=data["URL"]
                if isinstance(urls,str):
                    print("URLS",urls)
                    data=requests.get(urls).json()
                    addFolder(data)
                elif isinstance(urls,list):
                    if len(urls)==1:
                        print(urls[0])
                        url=urls[0]
                        data=requests.get(url).json()
                        addFolder(data)
                    else:
                        if urls:
                            for url in urls:
                                title=url.split(".json")[0].split("/")[-1:][0]
                                country="india"
                                if country in title or country.upper in title or country.lower() in title:
                                    print("Country::::::::",title)
                                li = xbmcgui.ListItem(title)
                                li.setArt({'thumb': "#"})
                                url=quote(url)
                                url=plugin.url_for(Dropbox,url)
                                list_items.append((url, li, True))
                            xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
                            xbmcplugin.addDirectoryItems(plugin.handle, list_items)
                            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
                        else:
                            dialog.notification(addon.getAddonInfo('name'), 'Add the URL to the File',os.path.join(addon_dir, 'icon.png'), 1500)
            else:
                if len(data)==0:
                    dialog.notification(addon.getAddonInfo('name'), 'Add the URL to the File',os.path.join(addon_dir, 'icon.png'), 1500)
                else:
                    data=requests.get(url).json()
                    addFolder(data)
        else:
            dialog.notification(addon.getAddonInfo('name'), 'Dropbox is Not Enable',os.path.join(addon_dir, 'icon.png'), 1500)
            
@plugin.route("/mode/<mode>")    
def mode(mode):
    if mode==3 or mode=="3":
        append_SourceFile(dropbox_file,str(addon.getSetting('new_URL')))
        

@plugin.route("/play_URl/<path:link>")
def play_URl(link,streamtype="HDS"):
    progress = xbmcgui.DialogProgress()
    try:
        from httplib import HTTPConnection
    except:
        from http.client import HTTPConnection
    print("URL_Playing:",link)
    link=unquote(link)
    Mac=link.split("?name=")[1].split("&")[2].split("=")[1]
    DNS=link.split("?name=")[1].split("&")[1].split("=")[1]
    title=link.split("?name=")[1].split("&")
    link=link.split("?name=")[0]
    player=PlayerSTB(DNS,Mac)
    player.Get_Profile()
    link=player.play_VLC(link)
    print(title)
    name=title[0]
    iconImage="DefaultVideo.png"
    listitem = xbmcgui.ListItem(name,path=link)
    
    listitem.setInfo('video', {'Title': name})
    try:
        if streamtype==None or streamtype=='' or streamtype in ['HDS'  'HLS','HLSRETRY']:
            listitem.setMimeType("flv-application/octet-stream");
            listitem.setContentLookup(False)
            progress.create('Starting local proxy')
        elif streamtype in ('TSDOWNLOADER'):
            listitem.setMimeType("video/mp2t");
            listitem.setContentLookup(False)
            progress.create('Starting local proxy')
        elif streamtype in ['HLSREDIR']:
            listitem.setMimeType("application/vnd.apple.mpegurl");
            listitem.setContentLookup(False)
            
    except: print('error while setting setMimeType, so ignoring it ')
    progress.create('Starting local proxy')
    xbmc.Player( ).play(link, listitem)


@plugin.route("/list_channels/<path:cat>")
def list_channels(cat):
    list_items=[]

    cat=unquote(cat).split("&")
    DNS=cat[2].split("=")[1]
    Mac=cat[1].split("=")[1]
    cat=cat[0].split("=")[1]
    player=PlayerSTB(DNS,Mac)
    player.Get_Profile()
    channel_url=player.get_name_url(cat)
    for x in channel_url:
        title=x[0]

        link=quote(x[1]+"?name="+str(title)+"&DNS="+DNS+"&Mac="+Mac)
        url=plugin.url_for(play_URl,link)
        li = xbmcgui.ListItem(title)
        li.setArt({'thumb': "#"})
        list_items.append((url, li, False))
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)






if __name__ == "__main__":
    plugin.run(sys.argv)