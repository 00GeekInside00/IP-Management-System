import json
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from database.orm.BaseModels import IBaseModel
import models.subnet as SubnetModule 

Base = declarative_base()

class VLan (Base, IBaseModel):
    """
    This class represents a VLAN. It is a child of the IBaseModel class.
    """
    __tablename__ = 'vlans'
    
    id = Column(Integer, primary_key=True)
    vlan_id = Column(Integer)
    name = Column(String(50))
    
    
    def model(self, meta)->Table:
        """model is intended to be returned and be used to migrate fields """
        vlan = Table(self.__tablename__, meta,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(50)),
                      Column('vlan_id', Integer, unique=True, nullable=False),
                      )
        return vlan
    
    def related_subnets(self, session)->None:
        """returns a list of subnets (querysets) that are related to this vlan"""
        return session.query(SubnetModule.Subnet).filter(SubnetModule.Subnet.vlan_id == self.id)
    
    def add_vlan(self, session)->None:
        """using the session, add a new vlan to the database"""
        self.insert(session)
        return self.id
    
    
    
    def modify_vlan(self, session, new_vlan_id, new_name= "")->None:
        """
        This method is used to modify a vlan data.
        Args:
            session ([type]): sqlalchemy session passed from the main function
            new_vlan_id ([type]): new vlan id to be assigned to the vlan.
            new_name (str, optional): mew vlam name to be assigned to the vlan. Defaults to "".

        Raises:
            Exception: [description]
        """
        vlan = session.query(VLan).filter(VLan.vlan_id == self.vlan_id).first()
        
        if vlan is None:
            raise Exception("Vlan not found")
            
        if new_name is None:
            new_name= self.name
            
        try:
            vlan.vlan_id = new_vlan_id
            vlan.name = new_name
            session.commit()
            
        except Exception as e:
            print(e)
            print("\nError modifying vlan make sure you supplied a unique Virtual LAN ID\n")
        
        
    
    def delete_vlan(self, session)->bool:
        """
        This method is used to delete a vlan from the database.
        Also making sure related subnets are not relted to it anymore.
        """
        vlan = session.query(VLan).filter(VLan.vlan_id == self.id).first()
        
        if (vlan is None):
            raise Exception("Vlan not found")
        
        related_subnets = session.query(SubnetModule.Subnet).filter(SubnetModule.Subnet.vlan_id == vlan.id)
        
        for subnet in related_subnets:
            subnet.vlan_id = None
            
        
        vlan.delete(session)
        session.commit()
        print("\nVlan deleted!\n")
        return True
    
    
    def to_json(self):
        """Helper Json representation of the vlan can be used in API"""
        return json.dumps({
            'id': self.id,
            'vlan_id': self.vlan_id,
            'name': self.name
        })
        
    def __str__(self):
        """Helper string representation of the vlan can be used in CLI"""
        return "Vlan: \n \n id: {} Virtual LAN ID : {} \t ".format(self.id, self.vlan_id, self.name)