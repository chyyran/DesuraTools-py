#coding=utf-8
__author__ = 'ron975'
import webbrowser

from generatehtml import TestReport

print "What is your Desura username?"
username = raw_input()
try:
    webbrowser.open(str(TestReport(username)))
except Exception:
    print "Invalid Desura Username"