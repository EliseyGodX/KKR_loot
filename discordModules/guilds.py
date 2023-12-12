import Project
import DB

class Guilds:
    
    def __init__(self, id_: int, admins: list[int], 
                 language: None | str = None,
                 link: None | str = None,
                 cord: None | tuple = None,
                 project: None | str = None,
                 service: None | str = None,
                 addon: Project = None,
                 project_db: DB = None) -> None:
        self.id_ = id_
        self.guild_language = language
        self.admins = admins

        self.link = link
        self.cord = cord
        
        self.project = project
        self.service = service
        self.addon = addon
        
        self.project_db = project_db