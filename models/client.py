import json
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean
from database.orm.BaseModels import IBaseModel
from models.network import Network
import models.subnet as SubnetModule
from types_mangement.ip import IPv4


Base = declarative_base()

class Client(Base, IBaseModel):
    
    """Representation of a IP address(Client)
    
    Stores all ips for subnets. can be used to reserve/release ip.

    Args:
        Base :sqla declarative base
        IBaseModel : base model interface
    """
    
    
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), unique=True)
    name = Column(String(50), default='IP- {}'.format(ip))
    reserved = Column(Boolean, default=True)
    network_id = Column(Integer, ForeignKey(Network.id))
    subnet_id = Column(Integer, ForeignKey(SubnetModule.Subnet.id))
    
    def reserve_ip(self, session, name, ip):
        """reserve ip for client"""
        #validate ip
        IPv4(ip)
        #Ip passed can have 3 states:
        #1. ip is not in database (does not exist)
        #2. ip is in database but is not reserved (available)
        #3. ip is in database and is reserved (reserved already)
        available = session.query(Client).filter(Client.ip == ip, Client.reserved == False)
        reserved_already = session.query(Client).filter(Client.ip == ip, Client.reserved == True) is not None
        doesnt_exist = session.query(Client).filter(Client.ip == ip).first() is None

        if available:
            #store reservedclient if available
            available.update({Client.name: name,Client.reserved: True})
            session.commit()
            print('IP {} was reseved succesfully!'.format(ip))
            return
        
        if doesnt_exist:
            #ip is not in database
            print('Client {} is not available for reservation'.format(ip))
            return
        
        if reserved_already:
            #cant reserve ip that is already reserved
            print('IP {} was already reserved and cant be modified'.format(ip))
            return
            

            
        
    def release_ip(self, session, ip):
        #validate ip
        IPv4(ip)
        #release ip changing flag to false
        session.query(Client).filter(Client.ip == ip).update({Client.reserved: False})
        session.commit()
    
    def released_ips(self, session):
        #shows all released ips
        ips = session.query(Client).filter(Client.reserved == False).all()
        return [ip.to_json() for ip in ips]
        
    def client_information(self, session):
        """client information
        returns client information including client_ip,parent_subnet,
        available_ip.
        
        
        Args:
            session : sqla session

        """
        parent_subnet = session.query(SubnetModule.Subnet).filter(SubnetModule.Subnet.id == self.subnet_id).first()
        is_available = session.query(Client).filter(Client.ip == self.ip, Client.reserved == False).first() is not None

        if parent_subnet is None:
            parent_subnet = "has no parent subnet (N/A)"
        else:
            parent_subnet = parent_subnet.ip
            
        if is_available is None:
            is_available = "not available on our records"
            
        return {
            'client_ip': self.ip,
            'parent_subnet':  parent_subnet,
            'available_ip': 'YES' if is_available else 'NO' 
        }
        
    def model(self, meta):
        """model is intended to be returned and be used to migrate fields """
        clients = Table(self.__tablename__, meta,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(50)),
                        Column('ip', String(15), unique=True),
                        Column('network_id', Integer,
                               ForeignKey('networks.id')),
                        Column('reserved', Boolean, default=True),
                        Column('subnet_id', Integer, ForeignKey('subnets.id'))
                        )
        return clients
    
    
    def to_json(self):
        """" representation of client for apis"""
        return json.dumps({
            'id': self.id,
            'ip': self.ip,
            'name': self.name,
            'network_id': self.network_id,
            'subnet_id': self.subnet_id
        })

    def __str__(self):
        """" representation of client for cli"""
        return "Client Machine: \n id: {} \t ip: {} \t name:{} \t network (Database Id): {} \t subnet (Database Id): {}\n".format(self.id, self.ip, self.name, self.network_id, self.subnet_id)
        