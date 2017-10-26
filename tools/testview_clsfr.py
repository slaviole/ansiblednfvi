#!/usr/local/bin/python3

from ncclient import manager
import untangle

def view_clsfr(obj):
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

def view_sfs(obj):
    try:
        line = 30 * "*"

        num_sfs = len(obj.rpc_reply.data.sfs.sf)
        print("")
        print(line)

        print(obj.rpc_reply.data.sfs.sf.sf_name.cdata)
        print(line)
        print("CPUs Assigned: ", obj.rpc_reply.data.sfs.sf.sf_state.num_cpus.cdata)
        print("Mem Allocated: ", obj.rpc_reply.data.sfs.sf.sf_state.mem_allocated.cdata)
        print("Admin State:   ", obj.rpc_reply.data.sfs.sf.sf_operation.state.cdata)
        print("Operational State:   ", obj.rpc_reply.data.sfs.sf.sf_state.oper_state.cdata)
        print("VNC Console:   ", obj.rpc_reply.data.sfs.sf.sf_state.console.vnc_port.cdata)
        num_if = len(obj.rpc_reply.data.sfs.sf.sfo.network_interface)

        for if_num in range(num_if):
            print(line)
            if_name = obj.rpc_reply.data.sfs.sf.sfo.network_interface[if_num].name.cdata
            if_type = obj.rpc_reply.data.sfs.sf.sfo.network_interface[if_num].network_type.cdata
            print(if_name)
            print("Interface Type: ",if_type)
            if not if_type == "default":
                log_port = obj.rpc_reply.data.sfs.sf.sfo.network_interface[if_num].logical_port.cdata
                print("Logical Port: ", log_port)

        print(line)
    except:
        print("No SFS's found")

def view_sffs(obj):
    # This is a placeholder
    pass

if __name__ == "__main__":
    with manager.connect(host='10.181.35.57',
                             port=830,
                             username='user',
                             password='ciena123',
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False
                             ) as netconf_manager:
        
        data = netconf_manager.get()
        data_str = str(data)
    dnfvi_obj = untangle.parse(data_str)
    view_clsfr(dnfvi_obj)
    #view_sfs(dnfvi_obj)
