from sqlalchemy import create_engine
import sqlalchemy


class Connection:
    """This class is used to create a connection to the database."""
    def __init__(self):
        self.database_name = 'database.db'
        self.connection_string = 'sqlite:///database/{}'.format(
            self.database_name)
        self.engine = create_engine(self.connection_string)

    def create_connection(self)->None:
        try:
            print('connecting to database...')
            return self.engine
        except:
            print("Connection failed")

    def create_db_session(self):
        """database Session creation."""
        try:
            Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
            session = Session()
            return session
        except:
            raise Exception("DB Session creation failed")

    def verbos_connection_info(self, engine):
        """used when a verbose connection info is needed."""
        print("connection info: \n\n{}\n".format(engine.url))
        print("dialect: {}\n".format(engine.dialect))
        print("driver: {}\n".format(engine.driver))
