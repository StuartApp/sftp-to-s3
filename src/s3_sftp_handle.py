
import logging
from paramiko import SFTPServer, SFTPAttributes, \
    SFTPHandle, SFTP_OK, AUTH_SUCCESSFUL, OPEN_SUCCEEDED, AUTH_FAILED, SFTP_PERMISSION_DENIED

class StubSFTPHandle (SFTPHandle):
    __tell = None
    downloaded = False
    def stat(self):
        return SFTP_OP_UNSUPPORTED

    def chattr(self, attr):
        return SFTP_OK

    def read(self, offset, length):
        readfile = getattr(self, 'readfile', None)
        if not readfile:
            return SFTP_OP_UNSUPPORTED
        logging.debug(f"Reading offset {offset}, length: {length}, file downloaded? {self.downloaded}")
        if not self.downloaded:
            self.s3.download_fileobj(self.bucket, self.path, readfile)
            self.downloaded = True
        logging.debug(f"Got file, tell is {readfile.tell()}")
        try:
            if self.__tell is None:
                self.__tell = readfile.tell()
            if offset != self.__tell:
                readfile.seek(offset)
                self.__tell = offset
            data = readfile.read(length)
            self.__tell += len(data)
            return data
        except Exception as e:
            logging.error("Error reading", e)
            self.__tell = None
            return SFTP_PERMISSION_DENIED

    def write(self, offset, data):
        writefile = getattr(self, 'writefile', None)
        if not writefile:
            return SFTP_OP_UNSUPPORTED
        writefile.write(data)
        writefile.seek(0)
        try:
            self.s3.upload_fileobj(writefile, self.bucket, self.path)
            return SFTP_OK
        except Exception as err:
            logging.error(err)
