from utilities.Validators import is_valid_mask

@is_valid_mask
class NetworkMask():
    """[summary]
        This class is used to represent a network mask
        validated be the is_valid_mask decorator
    """
    def __init__(self, mask):
        self._mask = mask
    
    def get_mask(self)->None:
        return self._mask
    
    def set_mask(self, mask)->None:
        self._mask = mask
        