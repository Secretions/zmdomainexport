#!/usr/bin/env python

import argparse
from subprocess import call
import zimbrasoap;

def main():
    args = parse()

    if not args.server:
        print("Missing server name!")
        exit(1)
    if not args.domain:
        print("Missing domain name!")
        exit(1)
    if not args.user:
        print("Missing admin user name!")
        exit(1)
    if not args.password:
        print("Missing admin password!")
        exit(1)
    if not args.backup_dir:
        print("Missing backup directory!")
        exit(1)

    # Setup zimbra soap session
    print("Performing admin authentication...")
    zmsoap = zimbrasoap.admin(server = args.server, trace=args.verbose)
    zmsoap.Auth(name = args.user, password = args.password)

    print("Getting all accounts...")
    accounts = zmsoap.GetAllAccounts(domain = {'by':'name', 'value':args.domain})

    for account in accounts.GetAllAccountsResponse.children():
        if account.get_name() == 'account':
            print("Backing up {0}...".format(account['name']))
            auth = zmsoap.DelegateAuth(attributes = {'duration':'86400'}, account = {'by':'name', 'value':account['name']})
            url = "https://zimbra.xmission.com/home/{0}/?fmt={1}&auth=qp&zauthtoken={2}&meta=1".format(account['name'],args.format,auth.authToken)
            rval = call(['wget', url, '-O', "{0}/{1}.{2}".format(args.backup_dir, account['name'], args.format)])
            if rval != 0:
                print("Error backing up: {0}, aborting!".format(account['name']))
                exit(1)

    print("Finished successfully!")

def parse():
    parser = argparse.ArgumentParser(description='Zimbra Domain Account Auto-Exporter')
    parser.add_argument('-d', '--domain', help='Domain to export')
    parser.add_argument('-f', '--format', help='Format for export (tgz, tar, zip), default: tgz', default='tgz')
    parser.add_argument('-s', '--server', help="Zimbra server hostname, default: zimbra.xmission.com", default='zimbra.xmission.com')
    parser.add_argument('-u', '--user', help="Zimbra Admin Username")
    parser.add_argument('-p', '--password', help="Zimbra Admin Password")
    parser.add_argument('-b', '--backup_dir', help="Directory for backups")
    parser.add_argument('-v', '--verbose', help="Verbose mode (SOAP Tracing)", action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    main()
