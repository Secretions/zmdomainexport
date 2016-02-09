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
    if not args.admin_user:
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
    zmsoap.Auth(name = args.admin_user, password = args.password)

    accounts = []

    if not args.users:
        print("Getting all accounts...")
        source_accounts = zmsoap.GetAllAccounts(domain = {'by':'name', 'value':args.domain})

        for account in source_accounts.GetAllAccountsResponse.children():
            if account.get_name() == 'account':
                accounts.append(account['name'])
    else:
        accounts = args.users.split(',')

    for account in accounts:
        print("Exporting {0}...".format(account))
        auth = zmsoap.DelegateAuth(attributes = {'duration':'86400'}, account = {'by':'name', 'value':account})
        url = "https://{0}/home/{1}/?fmt={2}&auth=qp&zauthtoken={3}&meta=1".format(args.server,account,args.format,auth.authToken)
        if args.wget:
            rval = call(['wget', url, '-O', "{0}/{1}.{2}".format(args.backup_dir, account, args.format)])
        else:
            rval = call(['curl', url, '-o', "{0}/{1}.{2}".format(args.backup_dir, account, args.format)])
        if rval != 0:
            print("Error backing up: {0}, aborting!".format(account))
            exit(1)

    print("Finished successfully!")

def parse():
    parser = argparse.ArgumentParser(description='Zimbra Domain Account Auto-Exporter')
    parser.add_argument('-u', '--users', help="Users to migrate (optional, defaults to all)")
    parser.add_argument('-d', '--domain', help='Domain to export')
    parser.add_argument('-f', '--format', help='Format for export (tgz, tar, zip), default: tgz', default='tgz')
    parser.add_argument('-s', '--server', help="Zimbra server hostname, default: zimbra.xmission.com", default='zimbra.xmission.com')
    parser.add_argument('-a', '--admin_user', help="Zimbra Admin Username")
    parser.add_argument('-p', '--password', help="Zimbra Admin Password")
    parser.add_argument('-b', '--backup_dir', help="Directory for backups")
    parser.add_argument('-w', '--wget', help="Use wget instead of curl", action='store_true')
    parser.add_argument('-v', '--verbose', help="Verbose mode (SOAP Tracing)", action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    main()
