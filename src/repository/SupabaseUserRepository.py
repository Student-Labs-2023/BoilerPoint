from .usersrepository import UserRepository
from typing import List
from src.models.users import User
from supabase import Client, create_client



class SupabaseUserRepository(UserRepository):
    
    def __init__(self,client:Client, table_name:str = 'UsersData'):
        self.client = client
        self.table_name = table_name

    def get(self,id : str) -> User:
        try:
            chat_id:int = int(id)
            response = self.client.table(self.table_name).select('full_name','gender','age','balance','tgusr','user_state').eq('chat_id', chat_id).execute()
            item = response.data[0]
            user_data = item
            pseudo = user_data.get('full_name', 'Unknown')
            gender = user_data.get('gender', 'Unknown')
            age = user_data.get('age', 'Unknown')
            balance = user_data.get('balance')
            user_state = user_data.get('user_state')
            tgusr = user_data.get('tgusr')
            return User(
                chat_id=chat_id,
                full_name=pseudo,
                gender=gender,
                user_state=user_state,
                age=age,
                balance=balance,
                tgusr = tgusr
            )
        except Exception as e:
            print(f"Error get info about user: {chat_id}: {e}")
            return None
        
    def set(self,user : User) -> None:
        if self.get(user.chat_id):  
            self.client.table(self.table_name).update(user.dict()).eq('chat_id',user.chat_id).execute()
        else:
            #insert
            self.client.table(self.table_name).insert(user.dict()).execute()

    def delete(self,user : User) -> None:
        try:
            if self.get(user.chat_id):
                self.client.table(self.table_name).delete().eq('chat_id',user.chat_id).execute()
        except Exception as e:
            print(f"Error delete user {user.chat_id} error : {e}")

            
    def list(self,**kwargs) -> List[User]: 
        ...
