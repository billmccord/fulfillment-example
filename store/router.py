class StoreRouter:
    """
    A router to control all database operations on models in the
    store application.
    """

    LABEL = 'store'
    DB = 'store_db'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.LABEL:
            return self.DB
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.LABEL:
            return self.DB
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if self.LABEL in (obj1._meta.app_label, obj2._meta.app_label):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.LABEL:
            return db == self.DB
        return None
