from models.vlan import VLan
from models.client import Client
from models.subnet import Subnet
from models.network import Network
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Table, Column, Integer, String, MetaData



class MigrationManager():
    """
    responsible for migrating the database structure.
    """
    def __init__(self, engine):
        self._engine = engine

    def migrate_structure(self):

        meta = MetaData()
        print("Migrating tables structure...")

        # create tables
        Network().model(meta)
        Subnet().model(meta)
        Client().model(meta)
        VLan().model(meta)

        meta.create_all(self._engine)
        print("Tables migrated!")

