all:
	@zip -r -x build/ Makefile .gitignore \*/.vimrc \*.swp .git/\* @ build/plasma-imap-resource-status.zip .
	@kbuildsycoca4 2> /dev/null
	@echo
	@plasmapkg -r plasma-imap-resource-status 2> /dev/null
	@echo
	@plasmapkg -i build/plasma-imap-resource-status.zip 2> /dev/null
	@kbuildsycoca4 2> /dev/null

run:
	plasmoidviewer plasma-imap-resource-status
