from facades.CliFacade import CliFacade


class Cli ():
    """
    Responsible for managing the command line interface
    mostly through the facades.CLIFacade
    """
    def __init__(self, session) -> None:
        self._session = session

    def start(self) -> None:
        """
        cli stating point
        """
        self.welcome()
        while True:
            #never leave unles instructed or if there is an exception
            user_choice = self.options()
            if user_choice == 10:
                #exsit when input 10
                print("\nbye!\n")
                break
            #executing user choice
            CliFacade(self._session).execute_cli_command(user_choice)


    def welcome(self) -> None:
        """
        decorated welcome message
        """
        print("""
       \n\n
▀█▀ ░█▀▀█ 　 ░█▀▄▀█ █▀▀█ █▀▀▄ █▀▀█ █▀▀▀ █▀▀ █▀▄▀█ █▀▀ █▀▀▄ ▀▀█▀▀ 　 ░█▀▀▀█ █──█ █▀▀ ▀▀█▀▀ █▀▀ █▀▄▀█ 
░█─ ░█▄▄█ 　 ░█░█░█ █▄▄█ █──█ █▄▄█ █─▀█ █▀▀ █─▀─█ █▀▀ █──█ ──█── 　 ─▀▀▀▄▄ █▄▄█ ▀▀█ ──█── █▀▀ █─▀─█ 
▄█▄ ░█─── 　 ░█──░█ ▀──▀ ▀──▀ ▀──▀ ▀▀▀▀ ▀▀▀ ▀───▀ ▀▀▀ ▀──▀ ──▀── 　 ░█▄▄▄█ ▄▄▄█ ▀▀▀ ──▀── ▀▀▀ ▀───▀
              """)

    def options(self) -> int:
        #options list
        screen = """
               \n
               type (1) then enter to add a new subnet
               type (2) then enter to delete existing subnet 
               type (3) then enter to reserve an ip address in a subnet 
               type (4) then enter to add a vlan to a subnet 
               type (5) then enter to delete a vlan for a subnet
               type (6) then enter to modify a vlan for a subnet
               type (7) then enter to show a subnet information
               type (8) then enter to show vlan information
               type (9) then enter to show a client/ip information
               type (10) then enter to exit
              \n
               """

        choice = int(input(screen))
        return choice
