class DatabaseRouter(object):
    def db_for_read(self, model, **hints):
        "Point all operations on vpay models to 'tiger_admin'"
        if model._meta.app_label == 'tiger_admin':
            return 'tiger_admin'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on vpay models to 'tiger_admin'"
        if model._meta.app_label == 'tiger_admin':
            return 'tiger_admin'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'tiger_admin' or obj2._meta.app_label == 'tiger_admin':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'tiger_admin':
            return model._meta.app_label == 'tiger_admin'
        elif model._meta.app_label == 'tiger_admin':
            return False
        return None
