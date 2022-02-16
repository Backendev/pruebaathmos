from singleton import Singleton
import pandas as pd
class Data(metaclass=Singleton):
    __data = None
    def __init__(self):
        self.__data = pd.read_json('users.json',orient="index")
        self.__data.reset_index(inplace=True)
        self.__data = self.__data.rename(columns = {'index':'id'})
    @property
    def data(self):
        return self.__data


    def get_data(self):
        self.__data = pd.read_json('users.json',orient ='index')
        self.__data.reset_index(inplace=True)
        self.__data = self.__data.rename(columns = {'index':'id'})
        
    def get_users(self):
        return self.__data
    def generate_id(self):
        last_item = self.__data.iloc[-1,:].id
        new_id = int(last_item) +1
        return new_id
    def new_user(self,user,idu):
        new_user = {
            'id':idu,
            'name':user.name,
            'lastname':user.lastname,
            'age':user.age,
            'email':user.email
        }
        return new_user
    def create_user(self,user):
        search_email = self.__data.query("email == '"+str(user.email)+"'")
        if len(search_email) == 0:
            new_id = self.generate_id()
            new_user = self.new_user(user,new_id)
            self.__data = self.__data.append(
                new_user, ignore_index=True)
            self.__data = self.__data.set_index('id')
            self.__data.to_json('users.json',orient="index",indent=4)
            self.get_data()
            return new_user
        else:
            return False
    
    def create_query(self,name=None,lastname=None,age=None,email=None,idu=None):
        query = ""
        search = {}
        if name != None:
            search['name'] = name
        if lastname != None:
            search['lastname'] = lastname
        if age != None:
            search['age'] = age
        if email != None:
            search['email'] = email
        if idu != None:
            search['id'] = idu
        print(search)
        print(len(search))
        count = 0
        inter = ""
        if len(search) > 0:
            for k,v in search.items():
                count += 1
                if count > 1 and count < len(search):
                    inter = " & "
                query += inter+str(k) + "=='"+str(v)+"'"
            return query
        else:
            return False

        

    def search_user(self,name=None,lastname=None,age=None,email=None,idu=None):
        query = self.create_query(name,lastname,age,email,idu)
        if query != None:
            result = self.__data.query(query)
            print(len(result))
        else:
            print("Sin Resultados")