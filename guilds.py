
class Guilds:
    
    def __init__(self, id_: int, admins: list[int], language = 'empty') -> None:
        self.id_ = id_
        self.guild_language = language
        self.admins = admins