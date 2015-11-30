# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.


# The package path prefix, if you want to install to another root, set DESTDIR to that root
PREFIX = /usr
# The command path excluding prefix
BIN = /bin
# The resource path excluding prefix
DATA = /share
# The command path including prefix
BINDIR = $(PREFIX)$(BIN)
# The resource path including prefix
DATADIR = $(PREFIX)$(DATA)
# The generic documentation path including prefix
DOCDIR = $(DATADIR)/doc
# The info manual documentation path including prefix
INFODIR = $(DATADIR)/info
# The man page documentation path including prefix
MANDIR = $(DATADIR)/man
# The man page section 1 path including prefix
MAN1DIR = $(MANDIR)/man1
# The license base path including prefix
LICENSEDIR = $(DATADIR)/licenses

# Python 3 command to use in shebangs
SHEBANG = /usr/bin/env python3
# The name of the command as it should be installed
COMMAND = cmdipc
# The name of the package as it should be installed
PKGNAME = cmdipc



# Build rules

.PHONY: default
default: base info

.PHONY: all
all: base doc

.PHONY: base
base: command

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
info: bin/cmdipc.info
bin/%.info: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p bin
	makeinfo $<
	mv $*.info $@

.PHONY: pdf
pdf: bin/cmdipc.pdf
bin/%.pdf: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p obj/pdf bin
	cd obj/pdf ; yes X | texi2pdf ../../$<
	mv obj/pdf/$*.pdf $@

.PHONY: dvi
dvi: bin/cmdipc.dvi
bin/%.dvi: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p obj/dvi bin
	cd obj/dvi ; yes X | $(TEXI2DVI) ../../$<
	mv obj/dvi/$*.dvi $@

.PHONY: ps
ps: bin/cmdipc.ps
bin/%.ps: doc/info/%.texinfo doc/info/fdl.texinfo
	@mkdir -p obj/ps bin
	cd obj/ps ; yes X | texi2pdf --ps ../../$<
	mv obj/ps/$*.ps $@



# Install rules

.PHONY: install
install: install-base install-info

.PHONY: install
install-all: install-base install-doc

# Install base rules

.PHONY: install-base
install-base: install-command install-copyright

.PHONY: install-command
install-command: bin/cmdipc
	install -dm755 -- "$(DESTDIR)$(BINDIR)"
	install -m755 $< -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"

.PHONY: install-copyright
install-copyright: install-copying install-license

.PHONY: install-copying
install-copying:
	install -dm755 -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	install -m644 COPYING -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"

.PHONY: install-license
install-license:
	install -dm755 -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	install -m644 LICENSE -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"

# Install documentation

.PHONY: install-doc
install-doc: install-info install-pdf install-ps install-dvi install-man

.PHONY: install-info
install-info: bin/cmdipc.info
	install -dm755 -- "$(DESTDIR)$(INFODIR)"
	install -m644 $< -- "$(DESTDIR)$(INFODIR)/$(PKGNAME).info"

.PHONY: install-pdf
install-pdf: bin/cmdipc.pdf
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).pdf"

.PHONY: install-ps
install-ps: bin/cmdipc.ps
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).ps"

.PHONY: install-dvi
install-dvi: bin/cmdipc.dvi
	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
	install -m644 $< -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).dvi"

.PHONY: install-man
install-man:
	install -dm755 -- "$(DESTDIR)$(MAN1DIR)"
	install -m644 doc/man/cmdipc.1 -- "$(DESTDIR)$(MAN1DIR)/$(COMMAND).1"


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
	-rm -- "$(DESTDIR)$(MAN1DIR)/$(COMMAND).1"



# Clean rules

.PHONY: all
clean:
	-rm -r bin obj

