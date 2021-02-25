#!/usr/bin/python3
from src import config, start_server, AppConfig
import argparse
import logging
import textwrap

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    usage = """\
    usage: sftpserver [options]
    -k/--keyfile Private key
    -b/--bucket Linked bucket
    -l/--level Log level
    -p/--port Listen port
    --host Listen address
    """
    parser = argparse.ArgumentParser(usage=textwrap.dedent(usage))
    parser.add_argument(
        '--host', dest='host',
        help='listen on HOST'
    )
    parser.add_argument(
        '-p', '--port', dest='port', type=int,
        help='listen on PORT'
    )
    parser.add_argument(
        '-l', '--level', dest='level',
        help='Debug level: WARNING, INFO, DEBUG'
    )
    parser.add_argument(
        '-k', '--keyfile', dest='keyfile', metavar='FILE',
        help='Path to private key, for example /tmp/test_rsa.key'
    )
    parser.add_argument(
        '-b', '--bucket', dest='bucket', metavar='BUCKET_NAME',
        help='Name of the bucket'
    )
    parser.add_argument(
        '-c', '--config', dest='config_file',
        help='Path of the configuration file'
    )

    args = parser.parse_args()
    config = AppConfig(args=args)

    logging.getLogger().setLevel(config.log_level)
    start_server(config)

if __name__ == "__main__":
    main()
