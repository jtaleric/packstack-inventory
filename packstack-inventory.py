import os
import csv
import argparse
import configparser

_HOST_TYPES = {'CONFIG_CONTROLLER_HOST':'controller',
               'CONFIG_COMPUTE_HOSTS':'compute',
               'CONFIG_NETWORK_HOSTS':'network',
               'CONFIG_STORAGE_HOST':'storage',
               'CONFIG_SAHARA_HOST':'sahara',
               'CONFIG_AMQP_HOST':'amqp',
               'CONFIG_MARIADB_HOST':'mariadb',
               'CONFIG_MONGODB_HOST':'mongodb',
               'CONFIG_REDIS_MASTER_HOST':'redis_master',
               'CONFIG_REDIS_SLAVE_HOSTS':'redis_slave',
               'CONFIG_REDIS_SENTINEL_HOSTS':'redis_sentinel'}

if __name__ == '__main__':
    cli = argparse.ArgumentParser()
    cli.add_argument("--file","-f", help="Packstack answer file")
    cli.add_argument("--inventory","-i",help="File to create inventory")
    args = cli.parse_args()
    answer_file=args.file

    config = configparser.ConfigParser()
    config.read(answer_file)

    _host_maps=[]
    _hosts={}
    for host in _HOST_TYPES:
        if config['general'][host]:
            if ',' in config['general'][host]:
                count = 0
                hosts = {}
                for node in config['general'][host].split(','):
                    hosts["{}-{}".format(_HOST_TYPES[host],count)] = node
                    _host_maps.append("{}-{} ansible_ssh_host={}".format(_HOST_TYPES[host],
                                                                          count,
                                                                          node))
                    count+=1

                _hosts[host]=hosts
            else:
                _hosts[host]=config['general'][host]
                _host_maps.append("{}-{} ansible_ssh_host={}".format(_HOST_TYPES[host],
                                                                     0,
                                                                     config['general'][host]))
    print "{}".format("\n".join(_host_maps))
    print ""
    for host in _hosts:
        print "[{}]".format(_HOST_TYPES[host])
        if type(_hosts[host]) is dict:
            for node in _hosts[host] :
                print node
            print ""
        else:
            print _hosts[host]
            print ""
