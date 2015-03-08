#!/usr/bin/env python
# --------------------------------------------------
# Copyright The IETF Trust 2011, All Rights Reserved
# --------------------------------------------------

import os
import re
from setuptools import setup

description = "Xml2rfc generates RFCs and IETF drafts from document source in XML according to the dtd in RFC2629."

def parse(changelog):
    ver_line = "^([a-z0-9+-]+) \(([^)]+)\)(.*?) *$"
    sig_line = "^ -- ([^<]+) <([^>]+)>  (.*?) *$"

    entries = []
    if type(changelog) == type(''):
        changelog = open(changelog)
    for line in changelog:
        if re.match(ver_line, line):
            package, version, rest = re.match(ver_line, line).groups()
            entry = {}
            entry["package"] = package
            entry["version"] = version
            entry["logentry"] = ""
        elif re.match(sig_line, line):
            author, email, date = re.match(sig_line, line).groups()
            entry["author"] = author
            entry["email"] = email
            entry["datetime"] = date
            entry["date"] = " ".join(date.split()[:3])

            entries += [ entry ]
        else:
            entry["logentry"] += line
    changelog.close()
    return entries

changelog_entry_template = """
Version %(version)s (%(date)s)
------------------------------------------------

%(logentry)s

"""

long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read()
long_description += """
Changelog
=========

""" + "\n".join([ changelog_entry_template % entry for entry in parse("changelog") ])

setup(
    # Package metadata
    name='xml2rfc',
    version='2.3.11.3',
    author='Josh Bothun (Concentric Sky)',
    author_email='tools-discuss@ietf.org',
    maintainer = "Henrik Levkowetz",
    maintainer_email = "henrik@levkowetz.com",
    url='http://tools.ietf.org/tools/xml2rfc/trac/',
    description=description,
    long_description=long_description,
    download_url = "http://pypi.python.org/pypi/xml2rfc",
    classifiers= [
        'Environment :: Console',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup :: XML',
        'License :: OSI Approved :: BSD License',
    ],
    license="Simplified BSD Licence",

    # Program data
    scripts=['scripts/xml2rfc'],
    packages=['xml2rfc', 'xml2rfc/writers'],
    package_data={'xml2rfc': ['templates/*',
                              ]},

    install_requires = ['lxml >= 2.2.8, < 2.9 '],
)
