from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

import atexit
import csv
import datetime
import os
import ssl


def log_delete():
    # Deleting the old file:
    print('Deleting old log...')
    lines = ''
    first_line = True
    with open('Materials\write_list.txt', mode='r') as file:
        file_to_remove = file.readline().strip()
        try:
            os.remove('Logs\\' + file_to_remove)
        except FileNotFoundError:
            pass
        lines = file.readlines()
    with open('Materials\write_list.txt', mode='w') as file:
        for line in lines:
            file.write(line.strip()+'\n')
        file.write('config_summary_{}.csv'.format(datetime.date.today()))


# utility for host login and getting a service_instance
def get_content(host, user, pwd):
    sslContext = None
    service_instance = None
    try:
        service_instance = connect.SmartConnect(host=host,
                                                user=user,
                                                pwd=pwd,
                                                port=443)

        atexit.register(connect.Disconnect, service_instance)
    except vmodl.MethodFault as error:
        print("vmodl error on "+host+": " + error.msg)
        pass
    except:
        try:
            print('Trying '+host+' without ssl cert...')
            sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslContext.verify_mode = ssl.CERT_NONE
            service_instance = connect.SmartConnect(host=host,
                                                    user=user,
                                                    pwd=pwd,
                                                    port=443,
                                                    sslContext=sslContext)
        except:
            print('ERROR: could not connect to '+host)
            pass

    if service_instance:
        print("Connected to host {}".format(host))
        content = service_instance.RetrieveServiceContent()
        return content


# Returns dict of vm's for given service_instance content
def get_summary(content):
    content = content
    results = []
    host_IP = ''

    # Finding all vm's for the host
    container = content.rootFolder
    search_object = [vim.VirtualMachine]
    recursive = True
    in_container = content.viewManager.CreateContainerView(container, search_object, recursive)
    host_vms = in_container.view

    # Creating a list of lists with vm info: ([VM][infopiece])
    for vm in host_vms:
        info_list = ['', '', '', '','']
        disk = 0

        # quick disk computation
        storage = vm.storage
        for datastore in storage.perDatastoreUsage:
            disk += datastore.committed

        # vm details: name, ip, cpu, mem, disk
        info_list[0] = vm.config.name
        info_list[1] = vm.guest.ipAddress
        info_list[2] = vm.config.hardware.numCPU
        info_list[3] = vm.summary.config.memorySizeMB
        info_list[4] = "{0:.2f}".format(int(disk)/1000000000)

        results.append(info_list)

    # appending the host IP
    container = content.rootFolder
    search_object = [vim.HostSystem]
    recursive = True
    in_container = content.viewManager.CreateContainerView(container, search_object, recursive)
    hosts = in_container.view
    for host in hosts:
        network = host.config.network
        for physical_adapter in network.vnic:
            host_IP += physical_adapter.spec.ip.ipAddress+"  "

    results.append(host_IP)

    return results

# Main Method
def main(user,pwd):
    # Getting login info
    user = user
    pwd = pwd
    hosts = []
    with open("Materials\connect_info.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            hosts.append(row[0])

    # Using a csv to write to
    with open('Logs\config_summary_{}.csv'.format(datetime.date.today()), mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # File Setup
        writer.writerow(['Timestamp: '])
        writer.writerow([" "+str(datetime.datetime.now())])
        writer.writerow([''])
        writer.writerow(['Host', 'IP\'s from host vnic\'s', 'VM', 'Guest IP', 'CPU (NUM)', 'MEM (MB)', 'DISK (GB)'])

        # Iterating through every host
        for host in hosts:

            content = get_content(host, user, pwd)
            if content:
                host_summary = get_summary(content)

                # Begin paragraph of a host
                if len(host_summary) > 1:
                    for num in range(0, len(host_summary) - 1):
                        writer.writerow([host, host_summary[-1]] + host_summary[num])
                else:
                    writer.writerow([host,host_summary[-1]])


if __name__ == '__main__':
    user = ''# user
    pwd = ''# pwd
    atexit.register(log_delete)
    main(user,pwd)