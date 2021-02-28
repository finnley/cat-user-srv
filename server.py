import logging
from concurrent import futures

import grpc

from proto import user_pb2, user_pb2_grpc
from handler.user import UserServicer


def serve():
    # 1.实例化server
    # 设置10个线程池
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 2.注册逻辑到server
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)

    # 3.启动 server
    server.add_insecure_port("[::]:50051")
    print(f"启动服务: 127.0.0.1:50051")
    server.start()
    # 加上这一句，否则一旦start,主程序就结束了，其他的相关线程就关闭了
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
