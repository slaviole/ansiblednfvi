#!/usr/local/bin/python3

def view_clsfr(obj):
     ''' Takes an Untangle Object as Input, parses it, and prints out Field names and values
         of interest for Classifer tags.
         No return value.
     '''
     try:
         for clsfr in obj.rpc_reply.data.classifiers.classifier:
             print('')
             print("Classifier Name:     ", clsfr.name.cdata)
             print("  filter-parameter:  ", clsfr.filter_entry.filter_parameter.cdata)
             print("  logical-not:       ", clsfr.filter_entry.logical_not.cdata)
             try:
                 print("    Outer Tag Level: ", clsfr.filter_entry.vtags.tag.cdata)
                 print("    VLAN ID:         ", clsfr.filter_entry.vtags.vlan_id.cdata)
             except:
                 pass
             try:
                 print("    Untagged-excl-pri-tagged: ",clsfr.filter_entry.untagged_exclude_priority_tagged.cdata)
             except:
                 pass
     except:
         print("No Classifiers found.")

     return True

def get_nc_obj(host, username, password, port):
    ''' Takes D-NVFI server login credentials, makes a Netconf get for all config and oper data.
        Returns an Untangle object with the parsed xml tree.
    '''
    with manager.connect(host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False
            ) as netconf_manager:
        data = netconf_manager.get()
        data_str=str(data)
        d_obj=untangle.parse(data_str)
        return d_obj

def main():
    module = AnsibleModule(
            argument_spec=dict(
                host=dict(required=True),
                username=dict(required=True),
                password=dict(required=True),
                port=dict(required=True, type='int'),
                ),
            supports_check_mode=True,
            no_log=True
            )
    host = module.params['host']
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']

    dnfvi_obj=get_nc_obj(host, username, password, port)
    #view_clsfr(dnfvi_obj)

    if view_clsfr(dnfvi_obj):
        module.exit_json(changed=False)
    else:
        msg="Really no Classifiers found"
        module.fail_json(msg=msg)

from ncclient import manager
import untangle
import yaml
from ansible.module_utils.basic import *
main()
