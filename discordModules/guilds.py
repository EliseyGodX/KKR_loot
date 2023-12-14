import Project
import DB

class Guilds:
    
    def __init__(self, id_: int, admins: list[int], 
                 language: None | str = None,
                 link: None | str = None,
                 cord: None | tuple = None,
                 orient: None | str = None,
                 range_: None | int = None,
                 sheet: None | dict = None,
                 project: None | str = None,
                 service: None | str = None,
                 addon: Project = None,
                 project_db: DB = None) -> None:
        
        self.id_ = id_
        self.guild_language = language
        self.admins = admins

        self.link = link
        self.cord = cord
        self.orient = orient
        self.range_ = range_
        self.sheet = sheet
        
        self.project = project
        self.service = service
        self.addon = addon
        
        self.project_db = project_db