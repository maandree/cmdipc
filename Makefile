# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.


# The package path prefix, if you want to install to another root, set DESTDIR to that root
PREFIX ?= /usr
# The command path excluding prefix
BIN ?= /bin
# The resource path excluding prefix
DATA ?= /share
# The command path including prefix
BINDIR ?= $(PREFIX)$(BIN)
# The resource path including prefix
DATADIR ?= $(PREFIX)$(DATA)
# The generic documentation path including prefix
DOCDIR ?= $(DATADIR)/doc
# The info manual documentation path including prefix
INFODIR ?= $(DATADIR)/info
# The license base path including prefix
LICENSEDIR ?= $(DATADIR)/licenses

# Python 3 command to use in shebangs
SHEBANG ?= /usr/bin/env python3
# The name of the command as it should be installed
COMMAND ?= cmdipc
# The name of the package as it should be installed
PKGNAME ?= cmdipc



# Build rules

.PHONY: default
default: command info

.PHONY: all
all: command doc

.PHONY: command
command: bin/cmdipc


# Build rules for Python source files

bin/cmdipc: obj/cmdipc.zip
	@mkdir -p bin
	echo '#!$(SHEBANG)' > $@
	cat $< >> $@
	chmod a+x $@

obj/cmdipc.zip: src/*.py
	mkdir -p obj
	cd src && zip ../$@ *.py


# Build rules for documentation

.PHONY: doc
doc: info pdf dvi ps

.PHONY: info
info: cmdipc.info
%.info: info/%.texinfo info/fdl.texinfo
	makeinfo $<

.PHONY: pdf
pdf: cmdipc.pdf
%.pdf: info/%.texinfo info/fdl.texinfo
	@mkdir -p obj/pdf
	cd obj/pdf ; yes X | texi2pdf ../../$<
	mv obj/pdf/$@ $@

.PHONY: dvi
dvi: cmdipc.dvi
%.dvi: info/%.texinfo info/fdl.texinfo
	@mkdir -p obj/dvi
	cd obj/dvi ; yes X | $(TEXI2DVI) ../../$<
	mv obj/dvi/$@ $@

.PHONY: ps
ps: cmdipc.ps
%.ps: info/%.texinfo info/fdl.texinfo
	@mkdir -p obj/ps
	cd obj/ps ; yes X | texi2pdf --ps ../../$<
	mv obj/ps/$@ $@



# Install rules

.PHONY: install
install: install-base install-info

.PHONY: install
install-all: install-base install-doc

# Install base rules

.PHONY: install-base
install-base: install-command install-license

.PHONY: install-command
install-command: bin/cmdipc
	install -dm755 -- "$(DESTDIR)$(BINDIR)"
	install -m755 $< -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"

.PHONY: install-license
install-license:
	install -dm755 -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	install -m644 COPYING LICENSE -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"

# Install documentation

.PHONY: install-doc
install-doc: install-info install-pdf install-ps install-dvi

.PHONY: install-info
install-info: cmdipc.info
	install -dm755 -- "$(DESTDIR)$(INFODIR)"
	install -m644 $< -- "$(DESTDIR)$(INFODIR)/$(PKGNAME).info"

.PHONY: install-pdf
install-pdf: cmdipc.pdf
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).pdf"

.PHONY: install-ps
install-ps: cmdipc.ps
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).ps"

.PHONY: install-dvi
install-dvi: cmdipc.dvi
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).dvi"


# Uninstall rules

.PHONY: uninstall
uninstall:
	-rm -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"
	-rm -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/COPYING"
	-rm -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/LICENSE"
	-rmdir -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	-rm -- "$(DESTDIR)$(INFODIR)/$(PKGNAME).info"
	-rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).pdf"
	-rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).ps"
	-rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).dvi"



# Clean rules

.PHONY: all
clean:
	-rm -r bin obj *.{pdf,ps,dvi,info}

