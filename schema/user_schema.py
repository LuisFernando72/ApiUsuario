from pydantic import BaseModel
from typing import Optional

class Userschema(BaseModel):
    id: Optional[str]
    name: str
    password : str
    fecha: str
    
class DataUser(BaseModel):
    name : str
    password: str