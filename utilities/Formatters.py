    
"""[summary]
    This package is used to format sqlalchemy quersets for commmand line output.
"""

def display_all_formatter(entities: list) -> None:
    """displays all the entities in a list of querysets"""
    for entity in entities:
        print(entity.__str__())
    
            
                   
def display_information_formatter(entities:dict) -> None:
    """displays all the entities of information dictionary"""
    print("\n ____________________________________________")
    for key, value in entities.items():
        print('{} {}'.format(key, value))
    print("\n ____________________________________________")