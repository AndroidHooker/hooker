#!/usr/bin/env python

import ntpath
import os
import hashlib

class APK(object):
    """Definition of an APK downloaded from
    a Market.

    An APK is defined by:
    - its APKID
    - its filepath
    - its name
    - its url
    - its version
    - its author name
    - its category
    - its description
    - its file size
    - its sha1

    """

    def __init__(self, APKID, filepath, name=None, url=None, version=None, author=None, category=None, description=None):
        self.APKID = APKID
        self.filepath = filepath
        self.filename = self.__computeFilename(filepath)
        self.filesize = self.__computeFilesize(filepath)
        self.sha1 = self.__computeSha1(filepath)
        self.name = name
        self.url = url
        self.version = version
        self.author = author
        self.category = category
        self.description = description

    def __str__(self):
        return "APK {0} ({1})".format(self.APKID, self.filepath)

    def __computeFilename(self, filepath):
        return ntpath.basename(filepath)

    def __computeFilesize(self, filepath):
        return os.path.getsize(filepath)

    def __computeSha1(self, filepath):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with open(filepath, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()
        
    #
    # Properties
    #

    @property
    def APKID(self):
        return self.__APKID

    @APKID.setter
    def APKID(self, APKID):
        if APKID is None:
            raise ValueError("APKID is Mandatory.")
        self.__APKID = APKID

    @property
    def filepath(self):
        return self.__filepath

    @filepath.setter
    def filepath(self, filepath):
        if filepath is None:
            raise ValueError("Filepath is Mandatory.")
        self.__filepath = filepath

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        if filename is None:
            raise ValueError("Filename is Mandatory.")
        self.__filename = filename

    @property
    def filesize(self):
        return self.__filesize

    @filesize.setter
    def filesize(self, filesize):
        if filesize is None:
            raise ValueError("Filesize is Mandatory.")
        self.__filesize = filesize

    @property
    def sha1(self):
        return self.__sha1

    @sha1.setter
    def sha1(self, sha1):
        if sha1 is None:
            raise ValueError("Sha1 is Mandatory.")
        self.__sha1 = sha1

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__version = version

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, category):
        self.__category = category

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author):
        self.__author = author
        
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url        
