'''
S3 SFTP Server interface.
Inherits from paramiko ServerInterface and SFTPServerInterface.
'''

from paramiko import SFTPServerInterface, SFTP_OK, SFTP_PERMISSION_DENIED
import tempfile
import boto3
import logging
from src.s3_attributes import S3Attributes
from src.s3_sftp_handle import StubSFTPHandle

class S3SFTPServerInterface (SFTPServerInterface):
    s3 = boto3.client('s3')
    bucket = ''

    def __init__(self, server, *largs, **kwargs):
        '''
        Create a new SFTPServerInterface object.
        :param .ServerInterface server:
            the server object associated with this channel and SFTP subsystem
        '''
        SFTPServerInterface.__init__(self, server)
        config = kwargs.get('config')
        if config:
            self.bucket = config.bucket


    def list_folder(self, path):
        '''
        Returns the contents of that path as SFTPAttributes.
        '''
        logging.info(f'LIST_FOLDER {path}')
        path = path.lstrip('/').rstrip('/')
        if path:
            path+='/'
        try:
            isTruncated = True
            flist = []
            while isTruncated:
                s3_list_response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=path, Delimiter='/')
                flist += s3_list_response.get('Contents', [])
                flist += s3_list_response.get('CommonPrefixes', [])
                isTruncated = s3_list_response.get('isTruncated', False)
            return [S3Attributes.from_object(x) for x in flist]
        except Exception as err:
            return SFTP_PERMISSION_DENIED

    def stat(self, path):
        '''
        Returns the `stat` of an S3 object as SFTPAttributes.
        '''
        logging.info(f'STAT {path}')
        path = path.lstrip('/')
        if not path:
            return S3Attributes.root()
        try:
            s3_list_response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=path, Delimiter='/')
            obj = s3_list_response.get('Contents',[]) + s3_list_response.get('CommonPrefixes',[])
            if not obj:
                raise FileNotFoundError(path)
            return S3Attributes.from_object(obj[0])
        except Exception as err:
            return SFTP_PERMISSION_DENIED

    def lstat(self, path):
        '''
        There are no symlinks in S3, so the result is the same as `stat`.
        '''
        logging.info(f'LSTAT {path}')
        return self.stat(path)

    def open(self, path, flags, attr):
        logging.info(f'OPEN {path}')
        path = path.lstrip('/')
        tmp_file = tempfile.TemporaryFile()
        fobj = StubSFTPHandle()
        fobj.filename = path
        fobj.readfile = tmp_file
        fobj.writefile = tmp_file
        fobj.bucket = self.bucket
        fobj.path = path
        fobj.s3 = self.s3
        return fobj

    def remove(self, path):
        '''
        Remove the object at the given location
        '''
        logging.info(f'REMOVE {path}')
        path = path.lstrip('/').rstrip('/')
        try:
            response = self.s3.delete_object(Bucket=self.bucket, Key=path)
            logging.info(response)
        except Exception as err:
            logging.info(err)
            return SFTP_PERMISSION_DENIED
        return SFTP_OK

    def rename(self, oldpath, newpath):
        '''
        To rename a file, we create a copy and remove the original.
        '''
        logging.info(f'RENAME {oldpath} to {newpath}')
        oldpath = oldpath.lstrip('/').rstrip('/')
        newpath = newpath.lstrip('/').rstrip('/')
        try:
            s3 = boto3.resource('s3')
            s3.Object(self.bucket, newpath).copy_from(CopySource=f"{self.bucket}/{oldpath}")
            s3.Object(self.bucket, oldpath).delete()
        except Exception as err:
            logging.info(err)
            return FileNotFoundError(oldpath)
        return SFTP_OK

    def mkdir(self, path, attr):
        '''
        Create a placeholder on that path.
        As there are no such things as `folders` in S3, an empty path cannot exist.
        '''
        logging.info(f'MKDIR {path}')
        path = path.lstrip('/').rstrip('/') + '/.touch'
        response = self.s3.put_object(Bucket=self.bucket, Key=path, Body=b'placeholder')
        logging.info(response)
        return SFTP_OK

    def rmdir(self, path):
        '''
        Rmdir will try to delete the placeholder created by mkdir.
        As there are no such things as `folders` in S3, an empty path cannot exist.
        '''
        logging.info(f'RMDIR {path}')
        path = path.lstrip('/').rstrip('/') + '/.touch'
        try:
            response = self.s3.delete_object(Bucket=self.bucket, Key=path)
            logging.debug(response)
        except Exception as err:
            logging.info(err)
            return SFTP_PERMISSION_DENIED
        return SFTP_OK

    def chattr(self, path, attr):
        '''
        Attrs are not supported on S3
        '''
        logging.info(f'CHATTR {path}')
        return SFTP_PERMISSION_DENIED

    def symlink(self, target_path, path):
        '''
        Symlinks are not supported on S3
        '''
        logging.info(f'SYMLINK {path}')
        return SFTP_PERMISSION_DENIED

    def readlink(self, path):
        '''
        Symlinks are not supported on S3
        '''
        logging.info(f'READLINK {path}')
        return SFTP_PERMISSION_DENIED