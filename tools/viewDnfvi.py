#!/usr/local/bin/python3

from ncclient import manager
import untangle
import argparse
import yaml

def view_clsfr(obj):
    try:
        for clsfr in obj.rpc_reply.data.classifiers.classifier:
            print('')
            print("Classifier Name:     ", clsfr.children[0].cdata)
            print("  filter-parameter:  ", clsfr.filter_entry.filter_parameter.cdata)
            print("  logical-not:       ", clsfr.children[1].logical_not.cdata)
            try:
                print("    Outer Tag Level: ", clsfr.children[1].children[2].tag.cdata)
                print("    VLAN ID:         ", clsfr.children[1].children[2].vlan_id.cdata)
            except:
                pass
            try:
                print("    Untagged-excl-pri-tagged: ",clsfr.children[1].untagged_exclude_priority_tagged.cdata)
            except:
                pass
    except:
        print("No Classifiers found.")

def view_sfs(obj):
    try:
        line = 30 * "*"
        num_sfs = len(obj.rpc_reply.data.sfs)
        for item in obj.rpc_reply.data.sfs.sf:
            print("")
            print("")
            print(item.sf_name.cdata)
            print(line)
            print("CPUs Assigned: ", item.sf_state.num_cpus.cdata)
            print("Mem Allocated: ", item.sf_state.mem_allocated.cdata)
            print("Admin State:   ", item.sf_operation.state.cdata)
            print("Operational State:   ", item.sf_state.oper_state.cdata)
            print("VNC Console:   ", item.sf_state.console.vnc_port.cdata)
            num_if = len(item.sfo.network_interface)
            for intf in item.sfo.network_interface:
                print(line)
                if_name = intf.name.cdata
                if_type = intf.network_type.cdata
                print(if_name)
                print("Interface Type: ",if_type)
                if not if_type == "default":
                    log_port = intf.logical_port.cdata
                    print("Logical Port: ", log_port)
            print(line)
    except:
        print("No SFs found.")

def view_sffs(obj):
    try:
        for fd in obj.rpc_reply.data.sffs.sff:
            print()
            print('SFF Name: ', fd.sff_name.cdata)
            print('SFF Mode:', fd.sff_mode.cdata)
            for fp in fd.interface:    
                print('  ', 'Flow Point Name: ', fp.name.cdata)
                print('    ', 'Logical Port: ', fp.logical_port.cdata)
                for clsfr in fp.classifier_list: 
                    print('    ', 'Classifier: ', clsfr.cdata)

    except:
        print("No SFFs found")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Provide a filename to get device credentials")
    parser.add_argument("option", help="Provide view option (clsfr,sfs,sffs)")
    args = parser.parse_args()
    if args.option != 'sfs' and args.option != 'sffs' and args.option != 'clsfr':
        print("Incorrect 2nd argument. Must be one of sfs, sffs, clsfr")
        return

    with open(args.filename) as f:
        ymlmap = yaml.safe_load(f)
        server = ymlmap['server']

    with open('hosts') as f:
        f.seek(0)
        while True:
            line = f.readline()
            lst = line.split()
            if lst[0] == server:
                ip_lst = lst[1].split("=")
                ip = ip_lst[1]
                user_lst = lst[2].split("=")
                user = user_lst[1]
                pwd_lst = lst[3].split("=")
                pwd = pwd_lst[1]
                break

    with manager.connect(host=ip,
                             port=830,
                             username=user,
                             password=pwd,
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False
                             ) as netconf_manager:
        
        data = netconf_manager.get()
    data_str = str(data)
    dnfvi_obj = untangle.parse(data_str)
    if args.option == 'clsfr':
        print("Searching for Classifiers")
        view_clsfr(dnfvi_obj)
    elif args.option == 'sfs':
        print("Searching for VNF's/SF's")
        view_sfs(dnfvi_obj)
    else:
        print("Searching SFF's (Service Chain build)")
        view_sffs(dnfvi_obj)


if __name__ == "__main__":
    main()

