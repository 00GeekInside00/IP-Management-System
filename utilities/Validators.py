from IPy import IP

""" 
    declaring the validators for the projcet
"""

def is_valid_ipv4(cls):
    """
    simple validator for ipv4 relying on IPy
    this function used as a decorator for ips
    """
    def validator_wrapper(*args):
        """ decorator for ipv4 """
        ip = args[0]
        instance = cls(ip)
        
        #relying on IPy to validate the ip    
        IP(ip)
            
        return instance
    return validator_wrapper


def is_valid_mask(cls):
    """
    simple validator for ip masks
    this function used as a decorator for ips
    """
    def validator_wrapper(*args):
        net_mask = args[0]
        instance = cls(net_mask)
        parts = net_mask.split(".")

        if len(parts) != 4:
            raise ValueError("Network Mask must have 4 parts")

        for part in parts:
            
            if not isinstance(int(part), int):
                raise ValueError("Network Mask octants must be numeric")

            if int(part) < 0 or int(part) > 255:
                raise ValueError("Network Mask octants must be between 0 and 255")
            
        return instance
    return validator_wrapper

def is_valid_vlan_id(vlan_id):
        """
        Validator for Virtual LAN Id
        """
        #check the latest vlan id
        #vlans are assigned sequentially in many network standards
        #getting the latest vlan id value
        
        
        #excluding vlan id 0, 1 ,4095
        if vlan_id is None:
    
            return 1
        
        #considering vlan id limits
        if vlan_id == 4095 or vlan_id == 1 or vlan_id > 4095:
            raise Exception("VLAN ID is not available")
        
        
        

