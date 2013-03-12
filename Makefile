all:
	mkdir obj
	for i in tzdata*/*; do ln -sf ../$$i src/; done
	cp -L src/yearistype.sh src/yearistype; chmod +x src/yearistype

include ./Makeconfig

install:
	$(MAKE) -C src install

check: $(objpfx)test-tz $(objpfx)tst-timezone
$(objpfx)test-tz: src/test-tz.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -o $@ $<
	TZDIR=$(inst_zonedir) $@ || ( echo TEST FAILED; exit 1 )
$(objpfx)tst-timezone: src/tst-timezone.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -o $@ $<
	TZDIR=$(inst_zonedir) $@ || ( echo TEST FAILED; exit 1 )

clean:
	rm -rf obj src/yearistype
	for i in tzdata*/*; do rm -f src/`basename $$i`; done
