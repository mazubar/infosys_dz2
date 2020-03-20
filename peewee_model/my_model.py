from peewee import *

base_db = SqliteDatabase('./peewee_model/my_model.db')

class Netflix(Model):
    show_id = CharField(primary_key=True)
    type_ = CharField()
    rating = CharField()
    duration = CharField()
    year_added = CharField()

    class Meta:
        database = base_db
        db_table = 'netflix'

class User(Model):
    id = AutoField(primary_key=True)
    login = CharField()
    password = CharField()

    class Meta:
        database = base_db
        db_table = 'logins'
