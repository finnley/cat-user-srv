import sys
import os
import logging
import signal
import argparse
from concurrent import futures

import grpc
from loguru import logger

# 获取当前项目相对路径 /Users/finnley/Code/cat-srvs 需要引入 os
# os.path.dirname(__file__) 表示当前 server.py 运行的目录位置
print(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
sys.path.insert(0, BASE_DIR)

from proto import user_pb2, user_pb2_grpc
from handler.user import UserServicer


def on_exit(signo, frame):
    logger.info("进程中断")
    # 直接退出
    sys.exit(0)


def serve():
    # 实例化
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        nargs="?",
                        type=str,
                        default="127.0.0.1",
                        help="binding host"
                        )
    parser.add_argument('--port',
                        nargs="?",
                        type=int,
                        default=50051,
                        help="the listening port"
                        )
    args = parser.parse_args()
    # command: python3 server.py --port=50052
    # 2021-02-28 20:03:13.674 | INFO     | __main__:serve:44 - Namespace(host='127.0.0.1', port=50052)
    logger.info(args)
    # 2021-02-28 20:03:13.674 | INFO     | __main__:serve:45 - 127.0.0.1
    logger.info(args.host)
    # 2021-02-28 20:03:13.675 | INFO     | __main__:serve:46 - 50052
    logger.info(args.port)

    logger.add("logs/user-srv-{time}.log")

    # 1.实例化server
    # 设置10个线程池
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 2.注册逻辑到server
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)

    # 3.启动 server
    # server.add_insecure_port("[::]:50051")
    server.add_insecure_port(f"{args.host}:{args.port}")

    # 主进程退出监听，需要引入 signal
    """
        windows 下支持的信号是有限的：
            SIGINT: 这个信号是由 Ctrl + c 发起的
            SIGTERM: 这个信号是由 kill 发起的软件终止
    """
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    # print(f"启动服务: 127.0.0.1:50051")
    # logger.info(f"启动服务: 127.0.0.1:50051")
    logger.info(f"启动服务: {args.host}:{args.port}")
    server.start()
    # 加上这一句，否则一旦start,主程序就结束了，其他的相关线程就关闭了
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
    # logger.debug("调试信息")
    # logger.info("普通信息")
    # logger.warning("警告信息")
    # logger.error("错误信息")
    # logger.critical("严重错误信息")
