'''
S3 Server interface.
Inherits from paramiko ServerInterface.
'''

from paramiko import ServerInterface, SFTP_OK, AUTH_SUCCESSFUL, OPEN_SUCCEEDED, AUTH_FAILED
from binascii import hexlify
import logging

class S3ServerInterface (ServerInterface):
    '''
    Handle connection and authentication
    '''
    allowed_keys = []
    caller_key = None
    caller_username = None
    def __init__(self, allowed_keys):
        ServerInterface.__init__(self)
        self.allowed_keys=allowed_keys

    def check_auth_password(self, username, password):
        # Not allowed
        return AUTH_FAILED
        
    def check_auth_publickey(self, username, key):
        # all are allowed
        ssh_fingerprint = hexlify(key.get_fingerprint()).decode('utf-8')
        if key in self.allowed_keys:
            logging.info(f"Auth succeded for username {username} with key fingerprint {ssh_fingerprint}")
            self.caller_key = key
            self.caller_username = username
            return AUTH_SUCCESSFUL
        logging.warning(f"Auth failed for username {username} and key fingerprint {ssh_fingerprint}")
        return AUTH_FAILED
        
    def check_channel_request(self, kind, chanid):
        return OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        """List availble auth mechanisms."""
        return "publickey"
