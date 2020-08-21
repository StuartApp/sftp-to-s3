import time
import socket

import paramiko
import logging

from src.s3_sftp_si import S3SFTPServerInterface
from src.sftp_si import S3ServerInterface
from src.config import AppConfig

import threading

BACKLOG = 10

def client_connection(server_socket, conn, addr, config):
    remote_ip,remote_port = addr
    logging.info(f"Connection from {remote_ip}:{remote_port}")
    transport = paramiko.Transport(conn)
    transport.add_server_key(config.private_key)
    transport.set_subsystem_handler(
        'sftp', paramiko.SFTPServer, S3SFTPServerInterface, config=config)

    server = S3ServerInterface(allowed_keys=config.keys)
    try:
        transport.start_server(server=server)

        channel = transport.accept()
        while transport.is_active():
            time.sleep(1)
    except EOFError:
        pass

def start_server(config):
    logging.info("Starting server")
    logging.debug('Config: ' + str(config.asDict()))
    paramiko_level = getattr(paramiko.common, config.log_level)
    paramiko.common.logging.basicConfig(level=paramiko_level)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((config.listen_addr, config.listen_port))
    server_socket.listen(BACKLOG)

    while True:
        conn, addr = server_socket.accept()

        t = threading.Thread(target=client_connection, args=(server_socket, conn, addr, config,))
        t.start()
