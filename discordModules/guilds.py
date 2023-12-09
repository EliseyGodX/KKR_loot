
class Guilds:
    
    def __init__(self, id_: int, admins: list[int], 
                 language: None | str = None,
                 link: None | str = None,
                 cord: None | tuple = None) -> None:
        self.id_ = id_
        self.guild_language = language
        self.admins = admins
        self.link = link
        self.cord = cord