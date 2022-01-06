from IPy import IP
from abc import ABCMeta, abstractmethod
from utilities.Validators import is_valid_ipv4

class Iip(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_ip(self):
        pass
    
    @staticmethod
    @abstractmethod
    def set_ip(self, ip):
        pass

@is_valid_ipv4   
class IPv4(Iip):
        
    def __init__(self, ip):
        self._ip = ip

    def get_ip(self):
        return self._ip
    
    def set_ip(self, ip):
        self._ip= ip
    
    def __str__(self) -> str:
        return "IPv4: {}".format(self._ip)
    
    def __repr__(self) -> str:
        return "IPv4: {}".format(self._ip)
    

    def get_ip_range(self,ip):
        ip_range = IP(ip)
        return {
            'clients': [ips for ips in ip_range],
            'number_of_clients': len(ip_range)
        }
        
    
    
class IPv6(Iip):
    pass

