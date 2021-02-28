import time
from datetime import date

import grpc
from loguru import logger

from models.models import User
from proto import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):
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

            rsp.data.append(user_info_rsp)

        return rsp
