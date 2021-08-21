import requests
class Tvshows:
    def __init__(self):
        self.plugin="Tvshows_Script"
        Self.Version=1.0
        self.User_agent=""
        self.Username=""
        self.s=requests.Session()
        #self.Password=Cripto_password()
    def Get_json(self):
        json_text=s.get(url,headers,timeout=1).content
        return json.load(json_text)
    def json_parse(self,ID):
        json_dict=self.Get_json()
        tvshow_name=json_dict["Tv Show"]
        ID=json_dict["ID"]
        length_tvshow=len(json_dict["seasons"])
        seasons=json_dict["seasons"]
        self.List_Shows([json_dict,tvshow_name,ID,length_tvshow,seasons])
        
        
    def List_Shows(self, shows_list):
        json_dict=shows_list[0]
        tvshow_name=shows_list[1]
        ID=shows_list[2]
        length_tvshow=shows_list[3]
        seasons=shows_list[4]
        for x in seasons:
            title=x["title"]
            total=x["EP list"]
            link=x["externallink"]