zookeeper-rpm
=============

A set of scripts to package zookeeper into an rpm.
Requires CentOS/RedHat 7.
Uses systemctl to register/manage service.
Configures Jolokia as Java Agent.

Setup
-----

    yum install make rpmdevtools

Product Documentation
---------------------

https://zookeeper.apache.org/doc/r3.4.14/zookeeperAdmin.html
https://jolokia.org/documentation.html

Build
-----

    git clone https://github.com/nicregez/zookeeper-rpm.git
    cd zookeeper-rpm
    export VERSION=3.4.14
    export BUILD_NUMBER=2
    make jolokia
    make rpm

Resulting RPM will be avaliable at $(shell pwd)/RPMS/x86_64

Install
-------

If you want to install locally

    yum install -y RPMS/x86_64/zookeeper-${VERSION}-${BUILD_NUMBER}.x86_64.rpm

If you install from an RPM repository

    yum install -y zookeeper

Configure
---------

    vi /etc/zookeeper/zoo.cfg
    vi /var/lib/zookeeper/data/myid
    chown zookeeper:zookeeper /var/lib/zookeeper/data/myid

Operation
---------

    sudo systemctl enable zookeeper
    sudo systemctl start zookeeper

Zookeeper command line is available via /usr/local/bin/zkcli or zkcli.

Default locations
-----------------

binaries
-   /opt/zookeeper/lib

configs
-   /etc/zookeeper/zoo.cfg
-   /etc/zookeeper/log4j.properties
-   /etc/zookeeper/configuration.xsl
-   /etc/sysconfig/zookeeper
-   /etc/logrotate.d/zookeeper

systemd
-   /usr/lib/systemd/system/zookeeper.service.d/classpath.conf
-   /usr/lib/systemd/system/zookeeper.service

data
-   /var/lib/zookeeper/data
-   /var/lib/zookeeper/log

logs
-   /var/log/zookeeper/log

command line
-   /usr/local/bin/zkcli
-   /etc/zookeeper/log4j-cli.properties
