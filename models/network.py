import json
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from database.orm.BaseModels import IBaseModel


Base = declarative_base()


class Network(Base, IBaseModel):
    """Representation of a network
    
    VLAN can be a part of more than one network
    not implemented yet. Not requied for now.

    Args:
        Base :sqla declarative base
        IBaseModel : base model interface
    """
    
    __tablename__ = 'networks'
    
    id= Column(Integer, primary_key=True)
    ip= Column(String(15))
    name= Column(String(50))
    
       
    def model(self, meta):
        network= Table(self.__tablename__, meta,
                         Column('id', Integer, primary_key=True),
                         Column('name', String(50)),
                         Column('ip', String(15), unique=True)
                         )
        return network
    
    
    
    def to_json(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'ip': self.ip
        })
        
    def __str__(self):
        return "Network: \n Id: {} \t Name: {} \t ip: {}".format(self.id,self.name, self.ip)
        