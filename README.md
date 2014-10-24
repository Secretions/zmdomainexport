zmdomainexport
==============

Zimbra Domain Export Utility

Utility to automate web-based Zibmra account exports.
Requires an admin account with adminLoginAs permissions.

Uses the zimbrasoap library (https://github.com/Secretions/zimbrasoap), which
is included in this repo for convenience.


This is the help output:

```
usage: zmdomainexport.py [-h] [-d DOMAIN] [-f FORMAT] [-s SERVER] [-u USER]
                         [-p PASSWORD] [-b BACKUP_DIR] [-v]

Zimbra Domain Account Auto-Exporter

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to export
  -f FORMAT, --format FORMAT
                        Format for export (tgz, tar, zip), default: tgz
  -s SERVER, --server SERVER
                        Zimbra server hostname, default: zimbra.xmission.com
  -u USER, --user USER  Zimbra Admin Username
  -p PASSWORD, --password PASSWORD
                        Zimbra Admin Password
  -b BACKUP_DIR, --backup_dir BACKUP_DIR
                        Directory for backups
  -v, --verbose         Verbose mode (SOAP Tracing)
```


This has only been tested on Zimbra Network Edition 8.0.7P2.
