
import logging
import traceback

import os
from paramiko import SFTPServer, SFTPAttributes, \
    SFTPHandle, SFTP_OK, AUTH_SUCCESSFUL, OPEN_SUCCEEDED, AUTH_FAILED, SFTP_PERMISSION_DENIED, SFTP_OP_UNSUPPORTED

class StubSFTPHandle (SFTPHandle):
    __tell = None
    downloaded = False
    def __init__(self, flags=0):
        """
        Create a new file handle representing a local file being served over
        SFTP.  If ``flags`` is passed in, it's used to determine if the file
        is open in append mode.
        :param int flags: optional flags as passed to
            `.SFTPServerInterface.open`
        """
        self.__flags = flags
        self.__name = None
        # only for handles to folders:
        self.__files = {}
        self.__tell = None
        self.multipart_count = 0
        self.multipart_tags = []
        self.multipart_id = None

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
            writefile = getattr(self, "writefile", None)
            if writefile is None:
                return SFTP_OP_UNSUPPORTED
            try:
                # in append mode, don't care about seeking
                if (self.__flags & os.O_APPEND) == 0:
                    if self.__tell is None:
                        self.__tell = writefile.tell()
                    if offset != self.__tell:
                        writefile.seek(offset)
                        self.__tell = offset
                writefile.write(data)
                writefile.flush()
            except IOError as e:
                self.__tell = None
                return SFTPServer.convert_errno(e.errno)
            if self.__tell is None:
                return SFTP_OK

            self.__tell += len(data)

            # if self.__tell <= 50*1024*1024: #Min size in S3: 5MB
            #     return SFTP_OK
            # try:
            #     if not self.multipart_count:
            #         self.multipart_id = self.s3.create_multipart_upload(Bucket=self.bucket, Key=self.path).get("UploadId")
            #         self.multipart_count = 1
            #         self.multipart_tags = []
            #     r = self.s3.upload_part(Body=data, Bucket=self.bucket, Key=self.path, UploadId=self.multipart_id, PartNumber=self.multipart_count)
            #     self.multipart_tags.append(r.get('ETag'))
            # except Exception as err:
            #     logging.error(f"Error uploading to S3 :( {err} {self.bucket}/{self.path} (part {self.multipart_count})")
            #     traceback.print_exc()
            #     return SFTP_OP_UNSUPPORTED

            # self.multipart_count+=1

            # logging.debug(f"Done uploading to s3 multipart number {self.multipart_count} with offset {offset}")
            return SFTP_OK

    def close(self):
        writefile = getattr(self, "writefile", None)
        if writefile is not None:
            if not self.multipart_id:
                writefile.seek(0)
                self.s3.upload_fileobj(writefile, self.bucket, self.path)
            writefile.close()
        # if self.multipart_id and self.multipart_count:
        #     try:
        #         parts = [{'ETag': y, 'PartNumber': x} for x,y in enumerate(self.multipart_tags, start=1)]
        #         self.s3.complete_multipart_upload(Bucket=self.bucket,
        #             Key=self.path,
        #             UploadId=self.multipart_id,
        #             MultipartUpload={'Parts': parts}
        #         )
        #         logging.info("Finished upload!")
        #     except Exception as err:
        #         try:
        #             self.s3.abort_multipart_upload(Bucket=self.bucket, Key=self.path, UploadId=self.multipart_id)
        #         except Exception as err_abort:
        #             logging.error(f"Error aborting upload: {err}")
        #         logging.error(f"Error closing file: {err}")

        readfile = getattr(self, "readfile", None)
        if readfile is not None:
            readfile.close()
