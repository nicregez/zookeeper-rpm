%define __jar_repack 0
%define debug_package %{nil}
%define name zookeeper
%define _prefix /opt
%define _conf_dir %{_sysconfdir}/zookeeper
%define _log_dir %{_var}/log/zookeeper/log
%define _change_log_dir %{_sharedstatedir}/zookeeper/log
%define _data_dir %{_sharedstatedir}/zookeeper/data

Summary: Apache ZooKeeper.
Name: zookeeper
Version: %{version}
Release: %{build_number}
License: Apache License, Version 2.0
Group: Applications/Databases
URL: http://zookeper.apache.org/
Source0: zookeeper-%{version}.tar.gz
Source1: jolokia-jvm-1.6.2-agent.jar
Source2: zookeeper.service
Source3: zookeeper.logrotate
Source4: zoo.cfg
Source5: log4j.properties
Source6: log4j-cli.properties
Source7: zookeeper.sysconfig
Source8: zkcli
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
Vendor: Apache Software Foundation
Packager: Nicolas Regez <nicolas.regez@swisscom.com>
Provides: zookeeper
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Apache ZooKeeper.

%prep
%setup

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/zookeeper
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_change_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_data_dir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service.d
mkdir -p $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 zookeeper-%{version}.jar $RPM_BUILD_ROOT%{_prefix}/zookeeper/
install -p -D -m 644 lib/*.jar $RPM_BUILD_ROOT%{_prefix}/zookeeper/
install -p -D -m 644 %{S:1} $RPM_BUILD_ROOT%{_prefix}/zookeeper/
install -p -D -m 644 %{S:2} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 644 %{S:3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 644 %{S:4} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:5} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:6} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:7} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zookeeper
install -p -D -m 755 %{S:8} $RPM_BUILD_ROOT/usr/local/bin/zkcli
install -p -D -m 644 conf/configuration.xsl $RPM_BUILD_ROOT%{_conf_dir}/
# stupid systemd fails to expand file paths in runtime
CLASSPATH=
for i in $RPM_BUILD_ROOT%{_prefix}/zookeeper/*.jar
do
  CLASSPATH="%{_prefix}/zookeeper/$(basename ${i}):${CLASSPATH}"
done
echo "[Service]" > $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service.d/classpath.conf
echo "Environment=CLASSPATH=${CLASSPATH}" >> $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service.d/classpath.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group zookeeper >/dev/null || /usr/sbin/groupadd -r zookeeper
if ! /usr/bin/getent passwd zookeeper >/dev/null ; then
    /usr/sbin/useradd -r -g zookeeper -m -d %{_prefix}/zookeeper -s /bin/bash -c "Zookeeper" zookeeper
fi

%post
%systemd_post zookeeper.service

%preun
%systemd_preun zookeeper.service

%postun
# When the last version of a package is erased, $1 is 0
# Otherwise it's an upgrade and we need to restart the service
if [ $1 -ge 1 ]; then
    /usr/bin/systemctl restart zookeeper.service
fi
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%{_unitdir}/zookeeper.service
%{_unitdir}/zookeeper.service.d/classpath.conf
%{_prefix}/zookeeper
/usr/local/bin/zkcli
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_sysconfdir}/sysconfig/zookeeper
%config(noreplace) %{_conf_dir}/*
%attr(0755,zookeeper,zookeeper) %dir %{_log_dir}
%attr(0700,zookeeper,zookeeper) %dir %{_change_log_dir}
%attr(0700,zookeeper,zookeeper) %dir %{_data_dir}
