.PHONY:	rpm clean

VERSION ?= 3.4.14
BUILD_NUMBER ?= 1
SOURCE = zookeeper-$(VERSION).tar.gz
TOPDIR = /tmp/zookeeper-rpm
PWD = $(shell pwd)
URL = https://archive.apache.org/dist/zookeeper/zookeeper-$(VERSION)/zookeeper-$(VERSION).tar.gz

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

clean:
	@rm -rf $(TOPDIR) $(PWD)/RPMS
	@rm -f $(SOURCE)

$(SOURCE).asc:
	@wget -q https://archive.apache.org/dist/zookeeper/zookeeper-$(VERSION)/$(SOURCE).asc

KEYS:
	@wget -q https://archive.apache.org/dist/zookeeper/KEYS
	gpg --import KEYS
