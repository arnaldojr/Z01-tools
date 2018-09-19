#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Rafael Corsi @ insper.edu.br
# Agosto @ 2018
# Disciplina Elementos de Sistemas
#
# Envia relatório do teste realizado.

import string
import random
import os.path
import xml.etree.ElementTree as ET
import time
from firebase import firebase
import json
import os

TOOLSPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class report(object):
    def __init__(self, logFile, proj):
        self.proj = proj
        self.logFile = logFile
        self.idFile = os.path.join(TOOLSPATH,"user.txt")
        self.userId = self.userID()
        self.connection = self.openFirebase()
        self.testData = []
        self.Travis = False
        if os.environ.get('Travis') is not None:
            self.Travis = True

    def openFirebase(self):
        connection = firebase.FirebaseApplication('https://elementos-10281.firebaseio.com/', authentication=None)
        return(connection)

    def userID(self):
        #if os.path.isfile(self.idFile):
        #    f = open(self.idFile,"r+")
        #    userid = f.readline()
        #else:
        #    f = open(self.idFile,"w+")
        #    userid = id_generator(size=18)
        #    f.write(userid)
        #    print("----")
        #f.close()
        return("GrupoA")

    def hw(self):
        tree = ET.parse(self.logFile)
        root = tree.getroot()
        ts = int(time.time())
        error = 0

        for n in root.iter('testcase'):
            testName = n.attrib['classname']
            runtime = n.attrib['time']

            p = n.find('failure')
            if p is None:
                status = 'Ok'
            else:
                status = 'Failure'
                error = error + 1

            p = n.find('system-out')
            log = p.text
            testName = testName[7:]
            self.testData.append({'name': testName, 'ts': str(ts), 'status':status})
        return(error)

    def assemblyTeste(self, logFile):
        ts = int(time.time())
        for log in logFile:
            self.testData.append({'name': log['name'], 'ts': str(ts), 'status': log['resultado']     })

    def assembler(self, logFile):
        ts = int(time.time())
        for log in logFile:
            self.testData.append({'name': log['name'], 'ts': str(ts), 'status': log['resultado']     })


    def send(self):
        for n in self.testData:
            if self.Travis:
                url = '/'+self.userId+'/'+'Travis/'+self.proj+'/'+n['name']+'/'+n['ts']
            else:
                url = '/'+self.userId+'/'+self.proj+'/'+n['name']+'/'+n['ts']
            result = self.connection.put(url, name='status', data=n['status'], params={'print': 'pretty'})
            print('.. .', end='', flush=True)
        print('')

