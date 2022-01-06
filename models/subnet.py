import json
from IPy import IP
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String
from database.orm.BaseModels import IBaseModel
from sqlalchemy.orm import declarative_base
from models.vlan import VLan
import models.client as  clientModule
from types_mangement.ip import IPv4
from utilities.Validators import is_valid_vlan_id



Base = declarative_base()

class Subnet (Base, IBaseModel):
    """
    This class represents a Subnet. It is a child of the IBaseModel class.
    """
    __tablename__ = 'subnets'

    id = Column(Integer, primary_key=True)
    ip = Column(String(15))
    mask = Column(String(12))
    name = Column(String(255), default="Unnamed Subnet")
    vlan_id = Column(Integer, ForeignKey(VLan.id))
        
    def model(self, meta)->Table:
        """model is intended to be returned and be used to migrate fields """
        subnet= Table(self.__tablename__, meta,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(255)),
                        Column('ip', String(15)),
                        Column('mask', String(12)),
                        Column('vlan_id', Integer,
                               ForeignKey('vlans.id'))
                        )
        return subnet
    
    def add_subnet(self, session):
        """
        adds a subnet to the database with an initial vlan
        """
        IPv4(self.ip)
        self.mask = IP(self.ip).netmask().strNormal(1)
        self.insert(session)
        
        #vlans are assigned sequentially in many network standards
        #getting the latest vlan id value
        new_vlan_id = session.query(func.max(VLan.vlan_id)).scalar()
        
        #handling the case when there are no vlans in the database
        if new_vlan_id is None:
            new_vlan_id = 1
        else:
            new_vlan_id = new_vlan_id + 1
        
        #validating the new vlan id value to be stored
        is_valid_vlan_id(new_vlan_id)
        
        #assigning the new vlan id to the subnet
        vlan_id=VLan(vlan_id=new_vlan_id, name="VLAN for Subnet {}".format(self.ip)).add_vlan(session)
        self.vlan_id = vlan_id
        
        reserved_by_default_ips = IP(self.ip)[0], IP(self.ip)[-1]
        #adding clients to the subnet
        for client_ip in IP(self.ip):
            
            print(client_ip)
            clientModule.Client(ip = client_ip.strNormal(1), network_id =1, subnet_id = self.id, reserved = True if client_ip in reserved_by_default_ips else False).insert(session)
            
        print("{} clients added".format(len(IP(self.ip))))
        
        
    
    def delete_subnet(self, session):
        """deletes a subnet from the database. Makes sure that the related subnets are disconnected before deleting it"""
        subnet = session.query(Subnet).filter(Subnet.id == self.id).first()
        related_clients = session.query(clientModule.Client).filter(clientModule.Client.subnet_id == self.id)
        
        for client in related_clients:
            client.subnet_id = None
        
        subnet.delete(session)
        session.commit()
        return True
    
    
    def subnet_information(self, session)->dict:
        """
        returns a dictionary with the subnet information including
        subnet_name
        subnet_mask
        total_subnet_ips
        reserved_ips
        free_ips
        utilization_percentage
        """

        total_subnet_ips = len(IP(self.ip))
        reserved_ips = session.query(clientModule.Client).filter(clientModule.Client.subnet_id == self.id, clientModule.Client.reserved == True ).count()
        free_ips = session.query(clientModule.Client).filter(clientModule.Client.subnet_id == self.id, clientModule.Client.reserved == False )
        percentage = (reserved_ips / total_subnet_ips) * 100
        
        return {
            'subnet_name': self.name,
            'subnet_mask': self.mask,
            'total_subnet_ips': total_subnet_ips,
            'reserved_ips': reserved_ips,
            'free_ips': [ip.ip for ip in free_ips],
            'utilization_percentage': "{}%".format(percentage)
        }
        
        
        
    
    def to_json(self):
        return json.dumps({
            'id': self.id,
            'ip': self.ip,
            'mask': self.mask,
            'vlan_id': self.vlan_id
        }, indent = 4)
        
    def __str__(self):
        return "Subnet: \n id: {} \t ip: {} \t Network Mask:{} \t VLAN ID: {}\n".format(self.id, self.ip, self.mask, self.vlan_id)