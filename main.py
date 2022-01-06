from cli.bootstrap import Cli
from database.connection import Connection
from database.migrations import MigrationManager

"""This package is the main entry point for the project."""


def main():
    """Project initialization. Creates the database and the tables and a sqlalchemy session."""
    connection = Connection().create_connection()
    MigrationManager(connection).migrate_structure()
    session = Connection().create_db_session()

    Cli(session).start()


if __name__ == '__main__':
    main()
