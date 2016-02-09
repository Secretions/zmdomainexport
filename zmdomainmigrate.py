#!/usr/bin/env python

import argparse
from subprocess import call
import zimbrasoap;

def main():
    args = parse()

    if not args.source_server:
        print("Missing source server name!")
        exit(1)
    if not args.source_domain:
        print("Missing source domain name!")
        exit(1)
    if not args.source_admin_user:
        print("Missing source admin user name!")
        exit(1)
    if not args.source_password:
        print("Missing source admin password!")
        exit(1)
    if not args.dest_server:
        print("Missing dest server name!")
        exit(1)
    if not args.dest_domain:
        print("Missing dest domain name!")
        exit(1)
    if not args.dest_admin_user:
        print("Missing dest admin user name!")
        exit(1)
    if not args.dest_password:
        print("Missing dest admin password!")
        exit(1)
    if not args.backup_dir:
        print("Missing backup directory!")
        exit(1)

    # Setup zimbra soap session
    print("Performing admin authentication...")
    zmsoap = zimbrasoap.admin(server = args.source_server, trace=args.verbose)
    zmsoap.Auth(name = args.source_admin_user, password = args.source_password)

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
            url = "https://{0}/home/{1}/?fmt={2}&auth=qp&zauthtoken={3}&meta=1".format(args.source_server,account,args.format,auth.authToken)
            if args.wget:
                rval = call(['wget', url, '-O', "{0}/{1}.{2}".format(args.backup_dir, account, args.format)])
            else:
                rval = call(['curl', url, '-o', "{0}/{1}.{2}".format(args.backup_dir, account, args.format)])
            if rval != 0:
                print("Error backing up: {0}, aborting!".format(account))
                exit(1)

    print("Finished backing up, restoring to dest server...");

    zmsoap = zimbrasoap.admin(server = args.dest_server, trace=args.verbose)
    zmsoap.Auth(name = args.dest_admin_user, password = args.dest_password)

    for account in accounts:
        print("Importing {0}...".format(account))
        auth = zmsoap.DelegateAuth(attributes = {'duration':'86400'}, account = {'by':'name', 'value':account})
        rval = call(['curl', '-o', '/dev/null', '-F', 'file=@{0}/{1}.{2};filename={0}/{1}.{2}'.format(args.backup_dir,account,args.format), "https://{0}/home/{1}/?fmt={2}&auth=qp&zauthtoken={3}&callback=ZmImportExportController__callback__import1&charset=UTF-8".format(args.dest_server,account,args.format,auth.authToken)])
        if rval != 0:
            print("Error importing up: {0}, aborting!".format(account))
            exit(1)

    print("Finished successfully!")

def parse():
    parser = argparse.ArgumentParser(description='Zimbra Domain Account Auto-Exporter')
    parser.add_argument('-f', '--format', help='Format for export (tgz, tar, zip), default: tgz', default='tgz')
    parser.add_argument('-u', '--users', help="Users to migrate (optional, defaults to all)")
    parser.add_argument('-ss', '--source_server', help="Zimbra source server hostname, default: zimbra.xmission.com", default='zimbra.xmission.com')
    parser.add_argument('-sd', '--source_domain', help='Source domain to export')
    parser.add_argument('-sa', '--source_admin_user', help="Source Zimbra Admin Username")
    parser.add_argument('-sp', '--source_password', help="Source Zimbra Admin Password")
    parser.add_argument('-ds', '--dest_server', help="Zimbra dest server hostname, default: zimbra.xmission.com", default='zimbra.xmission.com')
    parser.add_argument('-dd', '--dest_domain', help='Destination domain to import')
    parser.add_argument('-da', '--dest_admin_user', help="Destination Zimbra Admin Username")
    parser.add_argument('-dp', '--dest_password', help="Destination Zimbra Admin Password")
    parser.add_argument('-b', '--backup_dir', help="Directory for backups")
    parser.add_argument('-w', '--wget', help="Use wget instead of curl", action='store_true')
    parser.add_argument('-v', '--verbose', help="Verbose mode (SOAP Tracing)", action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    main()
