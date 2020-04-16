#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import subprocess

## kullanım: python3 cli01.py -i ali

# Parametreler
parser = argparse.ArgumentParser(description='Temel uygulama')
parser.add_argument('--isim', '-i',action="store",metavar='"isim"', help='isim giriniz',required=True)
parser.add_argument('--soyad', '-s',action="store",metavar='"soyad"', help='soyad giriniz')

args = parser.parse_args()

def isim2dosya(isimdeger):
    cmd = "echo 'isim: "+isimdeger+"' >> ornekdosya.txt"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cikti=proc.communicate()

if __name__ == "__main__":
    isim2dosya(args.isim)
    exit(0)
