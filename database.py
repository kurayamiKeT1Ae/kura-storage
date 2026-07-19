import json, os, re
from datetime import datetime


class Database:

    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        return data
    
    def save(self, new_data):
        with open(self.path, 'w', encoding="utf-8") as file:
            json.dump(new_data, file, indent=4)


class Users:
    def __init__(self, json_path, folder_path):
        self.json_path = json_path
        self.db = Database(json_path)
        self.folder_path = folder_path

    def get_user_data(self, user_id):
        data = self.db.load()
        return data[user_id]
    
    def get_user(self, user_id):
        return User(user_id, self.json_path)
    
    def get_user_by_username(self, username):
        data = self.db.load()
        usernames = self.get_values_of_key(data, 'username')
        username_index = usernames.index(username)
        user_id = list(data.keys())[username_index]
        return self.get_user(user_id)


    def change_username(self, user_id, new_username):
        data = self.db.load()
        data[user_id]['username'] = new_username
        self.db.save()

    def change_password(self, user_id, new_password):
        data = self.db.load()
        data[user_id]['password'] = new_password
        self.db.save(data)

    def change_storage_limit(self, user_id, new_storage_limit):
        data = self.db.load()
        self[user_id]['storage_limit'] = new_storage_limit
        self.db.save(data)

    def add_user(self, username, password, storage_limit):
        data = self.db.load()
        user_id = str(len(data) + 1)
        data[user_id] = {
            "username": username,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "storage_limit": storage_limit
        }
        self.db.save(data)
        return User(user_id, self.json_path).make()

    def del_user(self, user_id):
        data = self.db.load()
        del data[user_id]
        self.db.save(data)

    def get_values_of_key(self, data, key):
        return [data[user_id][key] for user_id in data]

    def is_user_exists(self, username) -> User:
        data = self.db.load()
        return username in self.get_values_of_key(data, "username")

    @staticmethod
    def is_valid_username(username: str) -> bool:
        pattern = r"^[a-zA-Z][a-zA-Z0-9_-]{2,15}$"

        if re.fullmatch(pattern, username):
            return True
        return False
    
    @staticmethod
    def is_valid_password(password: str) -> bool:
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        
        if re.fullmatch(pattern, password):
            return True
        return False


    


class User:
        def __init__(self, user_id : str, path : str) -> None:
            self.parent : Users = Users(path, "database")
            self.folder : Folder = Folder(self.parent.folder_path, user_id)
            self.id : int = user_id

        @property
        def username(self) -> str:
            return self.parent.get_user_data(self.id)['username']

        @property
        def password(self) -> str:
            return self.parent.get_user_data(self.id)['password']
        
        @property
        def created_at(self) -> str:
            return self.parent.get_user_data(self.id)['created_at']

        @property
        def storage_limit(self) -> int:
            return self.parent.get_user_data(self.id)['storage_limit']
        
        @property
        def files(self) -> list[File]:
            return self.folder.get_files()
        
        @property
        def file_dir(self) -> list[str]:
            return self.folder.get_file_names()
        
        @property
        def is_valid(self) -> bool:
            return self.parent.is_valid()

        def change_username(self, new_username):
            self.parent.change_username(self.id, new_username)
            
        def change_password(self, new_password):
            self.parent.change_password(self.id, new_password)

        def change_storage_limit(self, new_storage_limit):
            self.parent.change_storage_limit(self.id, new_storage_limit)

        def make(self) -> User:
            self.folder.add_folder()
            return self



class Folder:
    def __init__(self, path, user_id):
        self.path = path
        self.user_id = user_id

    def get_files(self) -> list[File]:
        filenames =  self.get_file_names()
        return [self.get_file_by_name(filename) for filename in filenames]
    
    def get_file_names(self) -> list[str]:
        return os.listdir(f"{self.path}\\{self.user_id}")
        
    def get_file(self, filename) -> File:
        return File(f"{self.path}\\{self.user_id}\\{filename}")
    
    def make_file(self, filename, content) -> File | list[bool, str]:
        res, msg = File.is_valid_filename(filename)
        if res:
            file = File(f"{self.path}\\{filename}")
            file.edit(content)
            return file
        
        return res, msg
    
    def add_folder(self):
        os.mkdir(f"{self.path}\\{self.user_id}")
        

class File:
    def __init__(self, file_path):
        self.file_path = file_path

    @property
    def content(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    def edit(self, new_content):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

    def delete(self):
        os.remove(self.file_path)

    def change_name(self, new_name):
        os.rename(self.file_path, self.file_path)

    @staticmethod
    def is_valid_filename(filename) -> list[bool, str]:
        # Length between 3 and 16 characters
        if (len(filename.replace(" ", "")) <= 3):
            return [0, "filename is too short, has to be more than 3 characters"]
        if (len(filename.replace(" ", "")) >= 20):
            return [0, "filename is too long, has to be less than 20 characters"]
        
        # Check for only allowed characters (letters, numbers, underscores)
        if not re.match("^[a-zA-Z0-9_. ]*$", filename):
            return [0, "special character are not allowed"]

        return [True, ""]

