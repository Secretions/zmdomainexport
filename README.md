zmdomainexport
==============

Zimbra Domain Export Utilities

Utilities to automate web-based Zimbra account exports and imports.
Requires an admin account with adminLoginAs permissions.

Uses the zimbrasoap library (https://github.com/Secretions/zimbrasoap), which
is included in this repo for convenience.


zmdomainexport.py:

```
usage: zmdomainexport.py [-h] [-u USERS] [-d DOMAIN] [-f FORMAT] [-s SERVER]
                         [-a ADMIN_USER] [-p PASSWORD] [-b BACKUP_DIR] [-w]
                         [-v]

Zimbra Domain Account Auto-Exporter

optional arguments:
  -h, --help            show this help message and exit
  -u USERS, --users USERS
                        Users to migrate (optional, defaults to all)
  -d DOMAIN, --domain DOMAIN
                        Domain to export
  -f FORMAT, --format FORMAT
                        Format for export (tgz, tar, zip), default: tgz
  -s SERVER, --server SERVER
                        Zimbra server hostname, default: zimbra.xmission.com
  -a ADMIN_USER, --admin_user ADMIN_USER
                        Zimbra Admin Username
  -p PASSWORD, --password PASSWORD
                        Zimbra Admin Password
  -b BACKUP_DIR, --backup_dir BACKUP_DIR
                        Directory for backups
  -w, --wget            Use wget instead of curl
  -v, --verbose         Verbose mode (SOAP Tracing)
```

Example usage:

./zmdomainexport.py -d yourdomain -f tgz -s zimbra.someserver.com \
   -a admin@yourdomain.com -p yourpassword -b /backups/`date +%s`/ \
   -u user1@yourdomain.com,user5@yourdomain.com,user12@yourdomain.com


zmdomainimport.py:

```
usage: zmdomainimport.py [-h] [-f FORMAT] [-s SERVER] [-u USER]
                         [-a ADMIN_USER] [-p PASSWORD] [-b BACKUP_FILE] [-v]

Zimbra Domain Account Importer

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Format for import (tgz, tar, zip), default: tgz
  -s SERVER, --server SERVER
                        Zimbra server hostname, default: zimbra.xmission.com
  -u USER, --user USER  Zimbra Username
  -a ADMIN_USER, --admin_user ADMIN_USER
                        Zimbra Admin User
  -p PASSWORD, --password PASSWORD
                        Zimbra Admin Password
  -b BACKUP_FILE, --backup_file BACKUP_FILE
                        Backup file (ie account@domain.com.tgz)
  -v, --verbose         Verbose mode (SOAP Tracing)
```

Example usage: 

./zmdomainimport.py -f tgz -s zimbra.yourserver.com -u account@yourdomain.com \
   -a admin@yourdomain.com -p yourpassword.com -b backups/account.tgz


zmdomainmigrate.py:

```
usage: zmdomainmigrate.py [-h] [-f FORMAT] [-u USERS] [-ss SOURCE_SERVER]
                          [-sd SOURCE_DOMAIN] [-sa SOURCE_ADMIN_USER]
                          [-sp SOURCE_PASSWORD] [-ds DEST_SERVER]
                          [-dd DEST_DOMAIN] [-da DEST_ADMIN_USER]
                          [-dp DEST_PASSWORD] [-b BACKUP_DIR] [-w] [-v]

Zimbra Domain Account Migrator

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Format for export (tgz, tar, zip), default: tgz
  -u USERS, --users USERS
                        Users to migrate (optional, defaults to all)
  -ss SOURCE_SERVER, --source_server SOURCE_SERVER
                        Zimbra source server hostname, default:
                        zimbra.xmission.com
  -sd SOURCE_DOMAIN, --source_domain SOURCE_DOMAIN
                        Source domain to export
  -sa SOURCE_ADMIN_USER, --source_admin_user SOURCE_ADMIN_USER
                        Source Zimbra Admin Username
  -sp SOURCE_PASSWORD, --source_password SOURCE_PASSWORD
                        Source Zimbra Admin Password
  -ds DEST_SERVER, --dest_server DEST_SERVER
                        Zimbra dest server hostname, default:
                        zimbra.xmission.com
  -dd DEST_DOMAIN, --dest_domain DEST_DOMAIN
                        Destination domain to import
  -da DEST_ADMIN_USER, --dest_admin_user DEST_ADMIN_USER
                        Destination Zimbra Admin Username
  -dp DEST_PASSWORD, --dest_password DEST_PASSWORD
                        Destination Zimbra Admin Password
  -b BACKUP_DIR, --backup_dir BACKUP_DIR
                        Directory for backups
  -v, --verbose         Verbose mode (SOAP Tracing)
```

Example usage:

./zmdomainmigrate.py -b ./tmp/ -f tgz \
   -u 'user1@somedomain.com,user5@somedomain.com' \
   -sd somedomain.com -ss zimbra.oldserver.com \
   -sa admin@somedomain.com -sp sourcepassword
   -dd somedomain.com -ds zimbra.newserver.com \
   -da admin@somedomain.com -dp destpassword

