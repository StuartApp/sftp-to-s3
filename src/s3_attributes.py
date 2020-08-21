import stat
import os
import time
from paramiko import SFTPAttributes

class S3Attributes(SFTPAttributes):
    @classmethod
    def from_object(cls, obj):
        """
        Create an `.SFTPAttributes` object from an S3 object in boto format.
        :param object obj: a dictionary returned by `boto3`.
        :return: new `.SFTPAttributes` object with the same attribute fields.
        """
        me = SFTPAttributes()
        if obj.get('Key'):
            me.st_size = obj.get('Size', 0)
            me.st_mtime = int(obj.get('LastModified').strftime('%s'))
            me.filename = os.path.basename(obj.get('Key'))
            me._flags = SFTPAttributes.FLAG_SIZE + SFTPAttributes.FLAG_PERMISSIONS
            me.st_mode = stat.S_IFREG + 0o777 # Show always as 777 perms
        if obj.get('Prefix'):
            me._flags = SFTPAttributes.FLAG_PERMISSIONS
            me.st_mode = stat.S_IFDIR + 0o777 # Show always as 777 perms
            me.filename = obj.get('Prefix').rstrip('/').split('/')[-1]
            me.st_mtime = int(time.time())
        return me

    @classmethod
    def root(cls):
        """
        Create an `.SFTPAttributes` object simulating the root folder.
        :return: new `.SFTPAttributes` object with the root attribute fields.
        """
        me = SFTPAttributes()
        me.st_mode = stat.S_IFDIR
        me.filename = '/'
        me.st_mtime = int(time.time())
        return me

    def __repr__(self):
        return "<S3Attributes: {}>".format(self._debug_str())
