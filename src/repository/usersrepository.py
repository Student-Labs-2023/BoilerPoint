from abc import ABC
from src.models.users import User
from typing import List

class UserRepository(ABC):
  
  def get(self,id : str) -> User:
    ...
  
  def set(self,user : User) -> None:
    ...

  def delete(self,id : str) -> None:
    ...

  def list(self,**kwargs) -> List[User]: 
    ...