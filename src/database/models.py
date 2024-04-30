import peewee
from settings import SETTINGS

database = peewee.MySQLDatabase(
    database=SETTINGS.DATABASE_SETTINS.DATABASE,
    host=SETTINGS.DATABASE_SETTINS.HOST,
    user=SETTINGS.DATABASE_SETTINS.USER,
    password=SETTINGS.DATABASE_SETTINS.PASSWORD,
    port=SETTINGS.DATABASE_SETTINS.PORT
)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class UserAuth(BaseModel):
    username: peewee.CharField = peewee.CharField(unique=True, null=False)
    password: peewee.CharField = peewee.CharField(null=False)


UserAuth.create_table()