import enum
from models.client import Client
from models.subnet import Subnet
from models.vlan import VLan
from models.network import Network
from types_mangement.ip import IPv4
from utilities.Formatters import (
    display_all_formatter, display_information_formatter)


# Using enum class create enumerations for cki commands
class Choice(enum.Enum):
    add_new_subnet = 1
    delete_existing_subnet = 2
    reserve_ip_address = 3
    add_vlan_to_subnet = 4
    delete_vlan_from_subnet = 5
    modify_existing_vlan = 6
    show_subnet_information = 7
    show_vlan_information = 8
    show_client_information = 9


class CliFacade():
    """Facade class to help with the command line interface
    It can simplify the process of adding new subnets, vlans, clients ...
    
    """
    def __init__(self, session) -> None:
        self._subnet = Subnet
        self._client = Client
        self._vlan = VLan
        self._network = Network
        self._session = session

    def add_new_subnet(self) -> None:
        """
        adds new subnet to the database
        through the command line interface
        and Subnet add_subnet
        """
        ip = input("\nEnter the IP address of the subnet with a range: \n")
        ip = IPv4(ip).get_ip()
        self._subnet(ip=ip).add_subnet(self._session)

    def delete_existing_subnet(self) -> None:
        """
        delets subnet from the database
        through the command line interface
        and Subnet delete_subnet
        """
        subnets = self._session.query(self._subnet).all()
        print("\nRegistered Subnets: \n")
        display_all_formatter(entities = subnets)
        choice = input("\n please choose a subnet by typing the id then enter: \n")
        selected_subnet = self._session.query(self._subnet).filter(
            self._subnet.id == int(choice)).first()
        selected_subnet.delete_subnet(self._session)

    def reserve_ip_address(self) -> None:
        """
        adds subnet to the database
        through the command line interface
        and Subnet add_subnet
        """
        client = self._session.query(self._client).all()
        display_all_formatter(entities=client)
        choice = input(
            "Type the id of the client/IP you want to reserve an IP address: \n")
        selected_client = self._session.query(self._client).filter(
            self._client.id == int(choice)).first()
        name = input("\n Enter the name of the client: \n")
        selected_client.reserve_ip(
            session=self._session, name=name, ip=selected_client.ip)
        print("\n IP address: {} reserved with client name: {} \n".format(
            selected_client.ip, name))

    def add_vlan_to_subnet(self) -> None:
        """
        adds subnet to a vlan
        through the command line interface
        
        shows subnets and vlans to assign a vlan to a subnet
        """
        subnets = self._session.query(self._subnet).all()
        print("\n Registered Subnets: \n")
        display_information_formatter(entities=subnets)
        choice = input(
            "\n please choose a subnet by typing the id then enter: \n")
        selected_subnet = self._session.query(self._subnet).filter(
            self._subnet.id == int(choice)).first()

        vlans = self._session.query(self._vlan).all()
        print("\n Registered Vlans: \n")
        display_all_formatter(entities=vlans)
        
        choice = input(
            "\n please choose a vlan by typing the virtual network id then enter: \n")
        selected_vlan = self._session.query(self._vlan).filter(
            self._vlan.id == int(choice)).first()
        selected_subnet.vlan_id = selected_vlan.vlan_id
        
        print("\n Vlan {} added to subnet {} \n".format(
            selected_vlan.vlan_id, selected_subnet.id))

    def delete_vlan_from_subnet(self) -> None:
        """
        deletes vlan from a subnet
        through the command line interface
        and Subnet add_subnet
        """
        subnets = self._session.query(self._subnet).all()
        print("\nRegistered Subnets: \n")
        display_all_formatter(entities=subnets)
        choice = input("Type the id of the vlan: \n")
        selected_subnet = self._session.query(self._subnet).filter(
            self._subnet.id == int(choice)).first()
        selected_subnet.vlan_id = None
        self._session.commit()

    def show_subnet_information(self) -> None:

        subnets = self._session.query(self._subnet).all()

        print("\n Registered Subnets: \n")

        for subnet in subnets:
            print(subnet.__str__())

        choice = input(
            "\n please choose a subnet by typing the id then enter: \n")
        selected_subnet = self._session.query(self._subnet).filter(
            self._subnet.id == int(choice)).first()
        info = selected_subnet.subnet_information(self._session)
        display_information_formatter(entities=info)

    def show_client_information(self) -> None:
        """
        shows client/IP information through Client.client_information 
        """
        choice = input("\n please type in the requested ip: \n")
        selected_client = self._session.query(self._client).filter(
            self._client.ip == IPv4(choice).get_ip()).first()

        if selected_client is None:
            print("\n No client with that ip address \n")
            return

        info = selected_client.client_information(self._session)
        
        print("client {} information\n".format(selected_client.ip))
        display_information_formatter(entities=info)

    #todo
    def delete_existing_vlan(self, vlan: dict) -> None:
        self._vlan.delete_vlan(self._session)

    def modify_existing_vlan(self) -> None:
        """
        modqifies vlan information including vlan id, name
        note that vlan id is not modifiable (db primary key)
        Vlan id is modifiable represented by vlan_id
        """
        subnets = self._session.query(self._subnet).all()
        print("\n Registered Subnets: \n")
        display_all_formatter(entities=subnets)
        choice = input(
            "\n please choose a subnet by typing the id then enter: \n")
        selected_subnet = self._session.query(self._subnet).filter(
            self._subnet.id == int(choice)).first()

        new_vlan_id = input(
            "\n Enter the new Virtual LAN ID (make sure it exists): \n")
        exists = self._session.query(self._vlan).filter(
            self._vlan.vlan_id == int(new_vlan_id)).first() is not None

        if exists:
            selected_subnet.vlan_id = new_vlan_id
            self._session.commit()
            print("\n VLAN ID changed to {} \n".format(new_vlan_id))
        else:
            print("\n VLAN ID does not exist, you may want to create it first \n")

    def show_vlan_information(self) -> None:
        vlans = self._session.query(self._vlan).all()
        display_information_formatter(entities=vlans)

    def execute_cli_command(self, command: int) -> None:
        """
        responsible for executing the command line interface
        relates choice to the function that is called
        """
        # command_func_map dictionary of commands for users to choose from
        command_func_map = {

            Choice.add_new_subnet.value: self.add_new_subnet,
            Choice.delete_existing_subnet.value: self.delete_existing_subnet,
            Choice.reserve_ip_address.value: self.reserve_ip_address,
            Choice.show_subnet_information.value: self.show_subnet_information,
            Choice.show_client_information.value: self.show_client_information,
            Choice.delete_vlan_from_subnet.value: self.delete_vlan_from_subnet,
            Choice.show_client_information.value: self.show_vlan_information,
            Choice.modify_existing_vlan.value: self.modify_existing_vlan,
            Choice.delete_vlan_from_subnet: self.delete_existing_vlan,
            Choice.add_vlan_to_subnet: self.add_vlan_to_subnet
        }

        # get users choice from a dictionary then run the function associated with that choice
        func = command_func_map.get(command)
        if not func:
            raise ValueError("Invalid command")
        func()
