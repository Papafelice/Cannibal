#!/usr/bin/env python3
# -*- coding: utf-8; -*-
"""
Copyright (c) 2020 Felix Huber

printing.py: helper functions to send a PDF document to a (CUPS) printer

printing.py is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with printing.py. If not, see <http://www.gnu.org/licenses/>.

"""

try:
    import gpg
except:
    canGpg = False
else:
    canGpg = True

import time
from datetime import datetime, date
import locale
from PyQt5.QtWidgets import QDialog, QApplication
from certProps import Ui_CertificateProperties
from applySignature import Ui_AttachSignature

OID_ADDR = "1.2.840.113549.1.9.1"


def getOIDuid(uid):
#1.2.840.113549.1.9.1=#746573746365727440636572742E6F7267,CN=Test Cert,OU=RB,O=DLR,L=Wessling,ST=Bayern,C=DE
    d = dict(x.split("=") for x in uid.split(","))
    #for k, v in d.items():
    #    print(k, v)
    if OID_ADDR in d:
        if d[OID_ADDR][0] == '#':
            addr = bytearray.fromhex(d[OID_ADDR][1:]).decode()
            d[OID_ADDR] = addr
    else:
        d[OID_ADDR] = None
    return d

def printOID(oid, title, dump=True):
    if dump is True:
        print("%s addr=%s,CN=%s,OU=%s,O=%s,C=%s" %
            (title, oid[OID_ADDR], oid["CN"], oid["OU"], oid["O"], oid["C"]))
        return None
    else:
        certText = "<pre>{0}:<br>E-Mail           {1}<br>"\
                                "Common Name (CN) {2}<br>"\
                                "Org-Unit         {3}<br>"\
                                "Organisation     {4}<br>"\
                                "Country          {5}</pre>"

        return certText.format(title, oid[OID_ADDR], 
                               oid.get("CN", None), oid.get("OU", None),
                               oid.get("O",  None), oid.get("C", None))
 
def date(time):
    date_format = locale.nl_langinfo(locale.D_T_FMT)
    date = datetime.fromtimestamp(time)
    return date.strftime(date_format)
 
def dumpKeys(keys):
    for k in keys:
        #print(k)
        print("Key fpr    %s" % k.fpr)
        oid = getOIDuid(k.issuer_name)
        printOID(oid, "Key issuer")
        uid = k.uids[0]  # first entry is prime
        if uid.uid.find(OID_ADDR) == 0:
            oid = getOIDuid(uid.uid)
            printOID(oid, "Subject   ")
        print("")
        for ks in k.subkeys:
            print("Subkey")
            print("\tfpr: %s " % ks.fpr)
            print("\texp: %s " % date(ks.expires))
            print("\texp: %s " % time.ctime(ks.expires))
            print("\tID : %s " % ks.keyid)
            print("\tlen: %s " % ks.length)
            print("")

    
class CertificatesDlg(QDialog):
    """
    A class to show a dialog where the X.509 certificates within gpg are shown  
    """

    def __init__(self, settings):
        super().__init__()
        self.ui = Ui_CertificateProperties()
        self.ui.setupUi(self)

        self.settings = settings
        if canGpg is True:
            self.c = gpg.Context(protocol=1) # GPGME_PROTOCOL_CMS

            # fill in list of keys
            keys = self.c.keylist(secret=True)
            for k in keys:
                oidI = getOIDuid(k.issuer_name)
                uid = k.uids[0]  # first entry is prime
                oidS = getOIDuid(uid.uid)
                ks = k.subkeys[0]
                self.ui.KeyList.addItem("{:16s} {:14s} {:14s}".format(ks.keyid, oidS["CN"], oidI["CN"]))

            # reload old values
            try:
                id = self.settings.value('Certs/current', "")
                index = self.ui.KeyList.findText(id)
                if index != -1:
                    self.ui.KeyList.setCurrentIndex(index)
            except:
                pass

            self.ui.KeyList.currentIndexChanged.connect(self.fillProps)        
            self.fillProps()
            
        self.show()

    def fillProps(self):
        pattern = self.ui.KeyList.currentText()[:16]
        try:
            k = next(self.c.keylist(pattern=pattern, secret=True))
            oid = getOIDuid(k.issuer_name)
            self.ui.Issuer.setText(printOID(oid, self.tr("Issuer"), dump=False))
            uid = k.uids[0]  # first entry is prime
            oid = getOIDuid(uid.uid)
            self.ui.Subject.setText(printOID(oid, self.tr("Subject"), dump=False))
            ks = k.subkeys[0]
            self.ui.Valid.setText(self.tr("<pre>Valid from:  %s\nValid until: %s ") % (date(ks.timestamp), date(ks.expires)))
            self.ui.Serial.setText(self.tr("<pre>Serial: %s\nKey-ID: %s\nFPR:    %s") % (k.issuer_serial, ks.keyid, ks.fpr))
        except:
            pass

    def accept(self):
        if self.settings is not None:
            self.settings.setValue('Certs/current', self.ui.KeyList.currentText())
        self.done(QDialog.Accepted)


class ApplySigDlg(QDialog):
    """
    A class to show a dialog to apply a signature  
    """

    def __init__(self, settings):
        super().__init__()
        self.ui = Ui_AttachSignature()
        self.ui.setupUi(self)

        self.settings = settings
        if canGpg is True:
            self.c = gpg.Context(protocol=1) # GPGME_PROTOCOL_CMS
            # fill in list of keys
            keys = self.c.keylist(secret=True)
            for k in keys:
                oidI = getOIDuid(k.issuer_name)
                uid = k.uids[0]  # first entry is prime
                oidS = getOIDuid(uid.uid)
                ks = k.subkeys[0]
                self.ui.KeyList.addItem("{:16s} {:14s} {:14s}".format(ks.keyid, oidS["CN"], oidI["CN"]))

            # reload old values
            try:
                id = self.settings.value('Certs/current', "")
                index = self.ui.KeyList.findText(id)
                if index != -1:
                    self.ui.KeyList.setCurrentIndex(index)
            except:
                pass

            #self.ui.KeyList.currentIndexChanged.connect(self.fillProps)        
            
        self.show()

    def accept(self):
        if self.settings is not None:
            self.settings.setValue('Certs/current', self.ui.KeyList.currentText())
        self.done(QDialog.Accepted)


if __name__ == '__main__':
    c = gpg.Context(protocol=1) # GPGME_PROTOCOL_CMS
    keys = c.keylist(secret=True)
    dumpKeys(keys)
        
    from sys import exit, argv
    app = QApplication(argv)
    
    dlg = CertificatesDlg(None)
    
    if dlg.exec() == QDialog.Accepted:
        pass
