from abc import abstractmethod


class IBaseModel():
    
    @staticmethod
    def select_all(session, columns):
        return session.query(*columns).all()

    def insert(self, session):
        session.add(self)
        return session.commit()
    
    def delete(self, session):
        session.delete(self)
        return session.commit()
    
    @staticmethod
    @abstractmethod
    def to_json(self):
        pass