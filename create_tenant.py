#!/usr/bin/env python

import sys
from cobra.mit.session import LoginSession
from cobra.mit.access import MoDirectory
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant

from cobra.internal.codec.xmlcodec import toXMLStr

def apic_login(hostname, username, password):
    url = "https://" + hostname
    sess = LoginSession(url, username, password)
    modir = MoDirectory(sess)
    try:
        modir.login()
    except:
	print 'Login error'
	exit(1)
    return modir
pass

def create_tenant(modir, tenant_name):
    policy_universe = modir.lookupByDn('uni')

    # 
    fvTenant = Tenant(policy_universe, tenant_name)

    # print the query in XML format
    print toXMLStr(policy_universe, prettyPrint=True)

    # Commit the change using a ConfigRequest object
    configReq = ConfigRequest()
    configReq.addMo(policy_universe)
    modir.commit(configReq)
pass

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: create_tenant.py <hostname> <username> <password> <tenant_name>'
	sys.exit()
    else:
	hostname, username, password, tenant_name = sys.argv[1:]
	modir = apic_login(hostname, username, password)
	create_tenant(modir, tenant_name)
	modir.logout()
    pass
pass
