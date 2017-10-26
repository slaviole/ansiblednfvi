#!/usr/local/bin/python3


from ncclient import manager
import untangle

with manager.connect(host='10.181.35.57',
                         port=830,
                         username='user',
                         password='ciena123',
                         hostkey_verify=False,
                         allow_agent=False,
                         look_for_keys=False
                         ) as netconf_manager:
    
    clsfr_filter = '''  
                        <classifiers xmlns="urn:ciena:params:xml:ns:yang:ciena-pn::ciena-mef-classifier">
                             <classifier>
                             </classifier>
                        </classifiers>
                    '''
    
    vnf_filter = '''
                        <sfs xmlns="urn:ciena:params:xml:ns:yang:ciena-pn::ciena-sf">
                            <sf>
                            </sf>
                        </sfs>    
                '''
    
    sffs_filter = '''
                        <sffs xmlns="urn:ciena:params:xml:ns:yang:ciena-pn::ciena-sfc">
                             <sff>
                             </sff>
                        </sffs>    
                    '''
    
#    data = netconf_manager.get(('subtree',clsfr_filter))
    data = netconf_manager.get_config(source='running')
    data_str = str(data)

# The next bit parses the subtree to extract the relevant parts for display. Should this be a function?
obj = untangle.parse(data_str)
try:
    num_clsfr = len(obj.rpc_reply.data.classifiers.classifier)
    for clsfr in range(num_clsfr):
        # See if I can simplify and use names instead of indices. particularly for Classifer Name
        print('')
        print("Classifier Name:     ", obj.rpc_reply.data.classifiers.classifier[clsfr].children[0].cdata)
        print("  filter-parameter:  ", obj.rpc_reply.data.classifiers.classifier[clsfr].children[1].filter_parameter.cdata)
        print("  logical-not:       ", obj.rpc_reply.data.classifiers.classifier[clsfr].children[1].logical_not.cdata)
        num_chld = len(obj.rpc_reply.data.classifiers.classifier[clsfr].children[1].children[2].children)
        #print(num_chld). used this to  determine only a single item below is used.
        for item in range(num_chld): 
            try:
                # Only one of these items returns a value. Troubleshoot and simplify if possible
                print("    Outer Tag Level: ", obj.rpc_reply.data.classifiers.classifier[clsfr].children[item].children[2].tag.cdata)
                print("    VLAN ID:         ", obj.rpc_reply.data.classifiers.classifier[clsfr].children[item].children[2].vlan_id.cdata)
            except:
                pass
        try:
            print("    Untagged-excl-pri-tagged: ",obj.rpc_reply.data.classifiers.classifier[clsfr].children[1].untagged_exclude_priority_tagged.cdata) 
        except:
            pass
except:
    print("No Classifiers found")
