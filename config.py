import json
import os



class Config:
    """配置文件"""
    def __init__(self, filepath: str):
        self.__config_template = {
            "expire_at": []
        }
        if not os.access(filepath, os.F_OK):
            self.file = open(filepath, "w+")
            self.__content = self.__config_template
            self.save()
        else:
            self.file = open(filepath, "r+")
            self.__content: dict = json.loads(self.file.read())

    def __del__(self):
        self.file.close()

    def save(self):
        self.file.seek(0)
        self.file.write(json.dumps(self.__content, indent=4))
        self.file.flush()

    def __getitem__(self, item):
        return self.__content.get(item, None)

    def __setitem__(self, key, value):
        self.__content[key] = value