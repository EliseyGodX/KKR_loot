def language_initialization() -> dict:
    pass

class Guilds:
    
    def __init__(self, id_: int, admins: list[int], language = None) -> None:
        self.id_ = id_
        self.guild_language = language
        self.admins = admins