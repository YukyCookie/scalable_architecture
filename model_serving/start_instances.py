# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

def start_instance( flavor = "ssc.medium", \
                    private_net = "UPPMAX 2022/1-1 Internal IPv4 Network", \
                    floating_ip_pool_name = None, \
                    floating_ip = None, \
                    image_name = "98c10a7f-2587-450b-866c-1266ea0dbe4b", \
                    key_name = "Weilin_Zhang", \
                    secgroups = ['default', 'Weilin'], \
                    cloud_cfg_name = "", \
                    instance_name = "", \
                    ):
    
    identifier = random.randint(1000,9999)

    loader = loading.get_plugin_loader('password')

    auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                    username=env['OS_USERNAME'],
                                    password=env['OS_PASSWORD'],
                                    project_name=env['OS_PROJECT_NAME'],
                                    project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                    #project_id=env['OS_PROJECT_ID'],
                                    user_domain_name=env['OS_USER_DOMAIN_NAME'])

    sess = session.Session(auth=auth)
    nova = client.Client('2.1', session=sess)
    print ("user authorization completed.")

    image = nova.glance.find_image(image_name)

    flavor = nova.flavors.find(name=flavor)

    if private_net != None:
        net = nova.neutron.find_network(private_net)
        nics = [{'net-id': net.id}]
    else:
        sys.exit("private-net not defined.")

    #print("Path at terminal when executing this file")
    #print(os.getcwd() + "\n")
    cfg_file_path =  os.getcwd()+'/{}'.format(cloud_cfg_name)
    if os.path.isfile(cfg_file_path):
        userdata = open(cfg_file_path)
    else:
        sys.exit("{} is not in current working directory".format(cloud_cfg_name))    


    print ("Creating instances ... ")
    instance = nova.servers.create(name="{}".format(instance_name)+str(identifier), image=image, flavor=flavor, key_name=key_name,userdata=userdata, nics=nics,security_groups=secgroups)
    inst_status = instance.status

    print ("waiting for 10 seconds.. ")
    time.sleep(10)

    while inst_status == 'BUILD':
        print ("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
        time.sleep(5)
        instance = nova.servers.get(instance.id)
        inst_status = instance.status

    ip_address = None
    for network in instance.networks[private_net]:
        if re.match('\d+\.\d+\.\d+\.\d+', network):
            ip_address = network
            break
    if ip_address is None:
        raise RuntimeError('No IP address assigned!')

    print ("Instance: "+ instance.name +" is in " + inst_status + " state" + " ip address: "+ ip_address)


number_of_prod_server = int(input("The number of production server: "))
number_of_dev_server = int(input("The number of development server: "))

for i in range(number_of_prod_server):
    start_instance(cloud_cfg_name = "prod-cloud-cfg.txt", instance_name = "g13_prod_")

for i in range(number_of_dev_server):
    start_instance(cloud_cfg_name = "dev-cloud-cfg.txt", instance_name = "g13_dev_")