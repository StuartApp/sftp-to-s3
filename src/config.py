import os
import io
import yaml
import paramiko
import logging
from base64 import b64decode

class AppConfig:
    #
    log_level = "INFO"
    #
    listen_addr = '0.0.0.0'
    listen_port = 3373
    #
    bucket = None
    #
    keys = []
    private_key = None

    def __init__(self, *largs, **kwargs):
        if 'args' in kwargs:
            config_file = kwargs['args'].config_file.rstrip().lstrip()

        config_file = os.getenv('CONFIG_FILE', config_file)
        self.load_from_envvars()
        try:
            with open(config_file, 'r') as cfg_file:
                config_dict = yaml.load(cfg_file, Loader=yaml.FullLoader)
                self.load_from_dictionary(config_dict)
        except Exception as err:
            logging.error('Error loading config file:', err)
        
        if 'args' in kwargs:
            self.load_from_params(kwargs.get('args'))
        self.listen_port = int(self.listen_port)

    def load_from_envvars(self):
        ''' 
        Load the config from environment variables
        '''
        try:
            raw_key = os.getenv('SSH_PUBLIC_KEY')
            decoded_key = b64decode(raw_key.split(' ')[1])
            self.keys = [paramiko.rsakey.RSAKey(data=decoded_key)]
        except AttributeError:
            self.keys = []
        self.bucket = os.getenv('S3_BUCKET', self.bucket)
        self.listen_addr = os.getenv('LISTEN_ADDR', self.listen_addr)
        self.listen_port = os.getenv('LISTEN_PORT', self.listen_port)
        self.log_level = os.getenv('LOG_LEVEL', self.log_level)

    def load_from_dictionary(self, cfg):
        '''
        Load the config from a dictionary
        '''
        keys = cfg.get('keys',[])
        if keys:
            self.keys = [
                paramiko.rsakey.RSAKey(data=b64decode(x.split(' ')[1]))
                for x in keys
            ]
        self.listen_addr = cfg.get('listen_addr', self.listen_addr)
        self.listen_port = cfg.get('listen_port', self.listen_port)
        private_key = cfg.get('private_key')
        if private_key:
            fd = io.StringIO(private_key)
            self.private_key = paramiko.RSAKey.from_private_key(fd)
        self.bucket = cfg.get('bucket', self.bucket)

    def load_from_params(self, params):
        '''
        Load the configuration from execution arguments
        '''
        if params.host != None:
            self.listen_addr = params.host.rstrip().lstrip()
        if params.port != None:
            self.listen_port = params.port.rstrip().lstrip()
        if params.level != None:
            self.log_level = params.level.rstrip().lstrip()
        if params.bucket != None:
            self.bucket = params.bucket.rstrip().lstrip()
        if params.keyfile != None:
            file_name = params.keyfile.rstrip().lstrip()
            self.private_key = paramiko.RSAKey.from_private_key_file(file_name)

    def asDict(self):
        '''
        For debugging purposes
        '''
        return {
            "bucket": self.bucket,
            "pk": self.private_key,
            "ssh_keys": self.keys,
            "addr": self.listen_addr,
            "port": self.listen_port,
        }
