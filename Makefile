.PHONY:	rpm clean

VERSION ?= 3.4.14
BUILD_NUMBER ?= 1
SOURCE = zookeeper-$(VERSION).tar.gz
URL = https://archive.apache.org/dist/zookeeper/zookeeper-$(VERSION)/zookeeper-$(VERSION).tar.gz
JOLOKIA = jolokia-jvm-1.6.2-agent.jar
JOLOKIA_URL = http://search.maven.org/remotecontent?filepath=org/jolokia/jolokia-jvm/1.6.2/${JOLOKIA}
TOPDIR = /tmp/zookeeper-rpm
PWD = $(shell pwd)

rpm: $(SOURCE)
	@rpmbuild -v -bb \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)/RPMS" \
			--define "_topdir $(TOPDIR)" \
			--define "version $(VERSION)" \
			--define "build_number $(BUILD_NUMBER)" \
			zookeeper.spec

source: $(SOURCE)

$(SOURCE): KEYS $(SOURCE).asc
	@wget -q $(URL)
	gpg --verify $(SOURCE).asc $(SOURCE)

jolokia:
	@wget "${JOLOKIA_URL}" -O ${JOLOKIA}

$(SOURCE).asc:
	@wget -q https://archive.apache.org/dist/zookeeper/zookeeper-$(VERSION)/$(SOURCE).asc

KEYS:
	@wget -q https://archive.apache.org/dist/zookeeper/KEYS
	gpg --import KEYS

clean:
	@rm -rf $(TOPDIR) $(PWD)/RPMS
	@rm -f $(SOURCE)
