#!/usr/bin/env python

import argparse
from subprocess import call
import zimbrasoap;

def main():
    args = parse()

    if not args.server:
        print("Missing server name!")
        exit(1)
    if not args.user:
        print("Missing user name!")
        exit(1)
    if not args.admin_user:
        print("Missing admin user name!")
        exit(1)
    if not args.password:
        print("Missing admin password!")
        exit(1)
    if not args.backup_file:
        print("Missing backup file!")
        exit(1)

    # Setup zimbra soap session
    print("Performing admin authentication...")
    zmsoap = zimbrasoap.admin(server = args.server, trace=args.verbose)
    zmsoap.Auth(name = args.admin_user, password = args.password)

    print("Backing up {0}...".format(args.user))
    auth = zmsoap.DelegateAuth(attributes = {'duration':'86400'}, account = {'by':'name', 'value':args.user})
    rval = call(['curl', '-o', '/dev/null', '-F', 'file=@{0};filename={0}'.format(args.backup_file), "https://{0}/home/{1}/?fmt={2}&auth=qp&zauthtoken={3}&callback=ZmImportExportController__callback__import1&charset=UTF-8".format(args.server,args.user,args.format,auth.authToken)])
    if rval != 0:
        print("Error importing up: {0}, aborting!".format(args.user))
        exit(1)

    print("Finished successfully!")

def parse():
    parser = argparse.ArgumentParser(description='Zimbra Domain Account Importer')
    parser.add_argument('-f', '--format', help='Format for import (tgz, tar, zip), default: tgz', default='tgz')
    parser.add_argument('-s', '--server', help="Zimbra server hostname, default: zimbra.xmission.com", default='zimbra.xmission.com')
    parser.add_argument('-u', '--user', help="Zimbra Username")
    parser.add_argument('-a', '--admin_user', help="Zimbra Admin User")
    parser.add_argument('-p', '--password', help="Zimbra Admin Password")
    parser.add_argument('-b', '--backup_file', help="Backup file (ie account@domain.com.tgz)")
    parser.add_argument('-v', '--verbose', help="Verbose mode (SOAP Tracing)", action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    main()
