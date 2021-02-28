from peewee import *
from settings import settings
from datetime import datetime


class BaseModel(Model):
    class Meta:
        database = settings.DB


# 用户模型
class User(BaseModel):
    GENDER_CHOICES = (
        (1, "male"),
        (0, "female")
    )
    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员")
    )

    # 不去指明id,peewee会自动生成id作为primary key
    # user_id = AutoField(primary_key=True)
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=100, verbose_name="密码")
    nickname = CharField(max_length=20, null=True, verbose_name="昵称")
    avatar = CharField(max_length=200, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=200, null=True, verbose_name="地址")
    description = TextField(null=True, verbose_name="个人简介")
    gender = BooleanField(choices=GENDER_CHOICES, default=1, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="用户角色")
    gmt_create = DateTimeField(default=datetime.now())
    gmt_modified = DateTimeField(default=datetime.now())
    deleted_at = DateTimeField(null=True)


if __name__ == "__main__":
    # 生成用户表结构
    settings.DB.create_tables([User])

    # 生成用户并加密用户密码
    # import the hash algorithm
    from passlib.hash import pbkdf2_sha256

    # for i in range(10):
    #     user = User()
    #     user.nickname = f"finnley-{i}"
    #     user.mobile = f"1339070350{i}"
    #     user.password = pbkdf2_sha256.hash("123456")
    #     user.save()

    # 加密验证
    # for user in User.select():
    #     print(pbkdf2_sha256.verify("123456", user.password))

    # python date 转int
    # for user in User.select():
    #     import time
    #     from datetime import date
    #
    #     if user.birthday:
    #         print(user.birthday)
    #         # float 类型
    #         u_time = time.mktime(user.birthday.timetuple())
    #         print(u_time)
    #         # float 转 int
    #         print(int(u_time))
    #         # int 转 date
    #         print(date.fromtimestamp(int(u_time)))

    users = User.select()
    # 没有接受返回值
    # users.limit(2).offset(2)
    users = users.limit(2).offset(2)
    for user in users:
        print(user.mobile)





