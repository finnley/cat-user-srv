import grpc

from proto import user_pb2, user_pb2_grpc


class UserTest:
    def __init__(self):
        # 连接grpc服务器
        channel = grpc.insecure_channel("127.0.0.1:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(page=2, pageSize=2))
        print(rsp.total)

        for user in rsp.data:
            print(user.mobile, user.birthday)


if __name__ == "__main__":
    user = UserTest()
    user.user_list()
