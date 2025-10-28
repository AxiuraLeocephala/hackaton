class Singleton:
    __instance: "Singleton" = None
    __is_exist: bool = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self, *args, **kwargs):
        if self.__is_exist:
            return
        Singleton.__is_exist = True