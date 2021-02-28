import time
from datetime import date

import grpc
from loguru import logger
from peewee import DoesNotExist
from models.models import User
from proto import user_pb2, user_pb2_grpc
from passlib.hash import pbkdf2_sha256
from google.protobuf import empty_pb2


class UserServicer(user_pb2_grpc.UserServicer):
    # 公用方法，将 user 的 model 对象转换成 message 对象
    def convert_user_to_rsp(self, user):
        user_info_rsp = user_pb2.UserInfoResponse()
        user_info_rsp.id = user.id
        user_info_rsp.mobile = user.mobile
        user_info_rsp.password = user.password
        user_info_rsp.role = user.role

        if user.nickname:
            user_info_rsp.nickname = user.nickname
        if user.gender:
            user_info_rsp.gender = user.gender
        if user.birthday:
            user_info_rsp.birthday = int(time.mktime(user.birthday.timetuple()))

        return user_info_rsp

    # 获取用户列表
    @logger.catch
    def GetUserList(self, request: user_pb2.PageInfo, context):
        rsp = user_pb2.UserListResponse()

        users = User.select()
        # 列表总数
        rsp.total = users.count()

        # 分页
        # offset start
        start = 0
        # 第几页
        page = 1
        # 每页条数 就是 proto 里面的 pageSize
        per_page_number = 10
        if request.pageSize:
            per_page_number = request.pageSize
        # 页码，即第几页
        if request.page:
            start = per_page_number * (request.page - 1)

        users = users.limit(per_page_number).offset(start)

        for user in users:
            # user_info_rsp = user_pb2.UserInfoResponse()
            # user_info_rsp.id = user.id
            # user_info_rsp.mobile = user.mobile
            # user_info_rsp.password = user.password
            # user_info_rsp.role = user.role
            #
            # if user.nickname:
            #     user_info_rsp.nickname = user.nickname
            # if user.gender:
            #     user_info_rsp.gender = user.gender
            # if user.birthday:
            #     user_info_rsp.birthday = int(time.mktime(user.birthday.timetuple()))
            #
            # rsp.data.append(user_info_rsp)
            # 优化
            rsp.data.append(self.convert_user_to_rsp(user))

        return rsp

    # 根据 id 查询用户信息
    @logger.catch
    def GetUserById(self, request: user_pb2.IdRequest, context):
        # 有可能id是不存在的，所以需要异常处理
        try:
            user = User.get(User.id == request.id)
            # 构造用户信息
            return self.convert_user_to_rsp(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    # 根据 mobile 查询用户信息
    @logger.catch
    def GetUserByMobile(self, request: user_pb2.MobileRequest, context):
        # 有可能id是不存在的，所以需要异常处理
        try:
            user = User.get(User.mobile == request.mobile)
            return self.convert_user_to_rsp(user)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()

    # 新建用户
    @logger.catch
    def CreateUser(self, request: user_pb2.CreateUserInfo, context):
        try:
            User.get(User.mobile == request.mobile)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("用户已存在")
            return user_pb2.UserInfoResponse()
        except DoesNotExist as e:
            pass

        user = User()
        user.nickname = request.nickname
        user.mobile = request.mobile
        user.password = pbkdf2_sha256.hash(request.password)
        user.save()

        return self.convert_user_to_rsp(user)

    # 更新用户
    @logger.catch
    def UpdateUser(self, request: user_pb2.UpdateUserInfo, context):
        try:
            user = User.get(User.id == request.id)

            user.nickname = request.nickname
            user.gender = request.gender
            # 将 int 类型转 date
            user.birthday = date.fromtimestamp(request.birthday)
            user.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return user_pb2.UserInfoResponse()
