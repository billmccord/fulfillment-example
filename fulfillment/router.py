class DefaultRouter:
    """
    A router to control all database operations on models in the
    store application.
    """

    _LABELS = (
        'auth',
        'admin',
        'contenttypes',
        'sessions',
    )

    def db_for_read(self, model, **hints):
        """
        Attempts to read store models go to store_db.
        """
        if model._meta.app_label in self._LABELS:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write store models go to store_db.
        """
        if model._meta.app_label in self._LABELS:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the store app is involved.
        """
        if obj1._meta.app_label in self._LABELS or \
            obj2._meta.app_label in self._LABELS:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the store app only appears in the 'store_db'
        database.
        """
        if app_label in self._LABELS:
            return db == 'default'
        return None
