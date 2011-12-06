Summary:   5250 Telnet protocol and Terminal
Name:      tn5250
Version:   0.17.4
Release:   3.2%{?dist}
License:   LGPLv2+
Group:     Applications/Internet
Source:    http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:   xt5250.desktop
Patch0:    tn5250-0.16.5-bhc.patch
Patch1:    tn5250-0.17.4-tinfo.patch
Url:       http://tn5250.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  dialog, xterm, hicolor-icon-theme
Requires(post): /usr/bin/tic
Requires(post): /sbin/ldconfig
Requires(preun): coreutils
BuildRequires: ncurses-devel, openssl-devel, desktop-file-utils

%description
tn5250 is an implementation of the 5250 Telnet protocol.
It provides the 5250 library and a 5250 terminal emulation.

%package devel
Group: Development/Libraries
Summary: Development tools for the 5250 protocol
Requires: automake, pkgconfig, ncurses-devel, openssl-devel
Requires: %{name} = %{version}-%{release}

%description devel
Libraries and header files to use with lib5250.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

%build
touch -r aclocal.m4 configure configure.in
%configure CPPFLAGS="-I/usr/kerberos/include" CFLAGS="$RPM_OPT_FLAGS" --with-x=yes --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/{48x48,64x64}/apps
install -m644 -p linux/5250.tcap $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m644 -p linux/5250.terminfo $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -m644 -p tn5250-48x48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/tn5250.png
install -m644 -p tn5250-62x48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/64x64/apps/tn5250.png
install -m644 -p tn5250-48x48.xpm $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/tn5250.xpm
install -m644 -p tn5250-62x48.xpm $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/64x64/apps/tn5250.xpm
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib5250.la
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications
desktop-file-install --vendor fedora \
   --dir $RPM_BUILD_ROOT/%{_datadir}/applications %{SOURCE1}
  #--add-category "Application;Network;X-Red-Hat-Base" 
cp -pf linux/README README.Linux

%clean
rm -rf $RPM_BUILD_ROOT

%post
unset TERMINFO
/usr/bin/tic %{_datadir}/%{name}/5250.terminfo 2>/dev/null ||:
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor ||:
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%preun
if [ $1 = 0 ]; then
rm -f %{_datadir}/terminfo/5/5250 
rm -f %{_datadir}/terminfo/X/xterm-5250
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README* TODO
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/*.so.*
%{_bindir}/*
%{_datadir}/icons/hicolor/*/apps/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/*

%files devel
%defattr(-, root, root, -)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Fri Feb 26 2010 Karsten Hopp <karsten@redhat.com> 0.17.4-3.2
- link with libtinfo

* Mon Nov 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.17.4-3.1
- Rebuilt for RHEL 6

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.17.4-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Karsten Hopp <karsten@redhat.com> 0.17.4-1
- update icon-cache scriptlets
- update to 0.17.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 0.17.3-20
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17.3-19
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Karsten Hopp <karsten@redhat.com> 0.17.3-18
- fix multilib problem in /usr/bin/tn5250-config (#343301)

* Wed Dec 05 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-17
- rebuild with new openssl lib

* Mon Aug 27 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-16
- fix license tag
- rebuild

* Wed Aug 01 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-15
- change requires to hicolor-icon-theme for the icons directory
  (#250358)

* Wed Feb 28 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-14
- copy readme instead of moving it
- fix desktop file
- fix scriptlets

* Tue Feb 27 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-13
- drop buildrequirement libtool
- update icon cache on install/uninstall

* Mon Feb 26 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-12
- misc review fixes (#226496)

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-11
- fix permissions
- touch only patched files

* Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-10
- rename icon files to tn5250.{png,xpm}
- remove Mimetype from desktop file
- move category to desktop file
- use vendor fedora for desktop-file-install
- touch files to avoid autotools run

* Tue Feb 13 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-9
- fix icon name
- fix icon path

* Tue Feb 13 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-8
- merge review changes (#226496):
- move icons into hicolor subdir
- require fedora-logos for the icons directory
- require xterm for xt5250
- -devel subpackage requires automake, openssl-devel, ncurses-devel, pkgconfig
- Requires(post): /usr/bin/tic
- Requires(preun): coreutils
- disable static libs


* Thu Feb 01 2007 Karsten Hopp <karsten@redhat.com> 0.17.3-7
- move tn5250,m4 and lib5250.so to -devel subpackage (#203639)
- move tn5250-config, too
- use macros

* Fri Sep 08 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-5
- fix postinstall script

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17.3-4.1
- rebuild

* Wed Jun 28 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-4
- add buildrequires automake, libtool

* Tue May 23 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-3
- don't check for sizeof(long), the result isn't used anywhere and
  causes problems with multilib installs

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 0.17.3-2
- add buildrequirement openssl-devel (#191875, Andreas Thienemann)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.17.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Karsten Hopp <karsten@redhat.de> 0.17.3-1
- update

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 0.16.5-7
- rebuilt against new openssl

* Mon Jun 27 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-6
- add buildrequires ncurses-devel (#160985)

* Thu Mar 17 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-5
- rebuild with gcc-4

* Thu Feb 17 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-4
- change Copyright: -> License:

* Tue Jan 25 2005 Karsten Hopp <karsten@redhat.de> 0.16.5-3 
- add BuildRequires ncurses-devel (#137558)

* Tue Aug 03 2004 Karsten Hopp <karsten@redhat.de> 0.16.5-2 
- build for FC3
- add gcc34 patch

* Wed May 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add proper ldconfig calls

* Wed Mar 19 2003 Karsten Hopp <karsten@redhat.de> 0.16.5-1
- update to 0.16.5
- run libtoolize to fix config.sub
- fix _libdir
- fix Group:
- fix URLs
- remove obsolete patch

* Wed Sep 18 2002 Guy Streeter <streeter@redhat.com>
- unset the TERMINFO env var before running tic in %%post, so
  it puts the compiled files in the right place.
- require ncurses and dialog

* Mon Jan 29 2001 Henri Gomez <hgomez@slib.fr>
- 0.16.1 RPM release 2 
- Dave McKenzie's cursor positioning fixes
- Scott Klement fixes to lp5250d, auto-enter field handling, 
  field plus & field minus key handling , FER state key handling
 
* Fri Dec 22 2000 Henri Gomez <hgomez@slib.fr>
- 0.16.1

* Tue Dec 12 2000 Henri Gomez <hgomez@slib.fr>
- 0.16.0
- many fixes, take a look at ChangeLog
- compiled on Redhat 6.1 box plus updates with rpm-3.0.5

* Fri May 02 2000 Henri Gomez <hgomez@slib.fr>
- 0.16.0pre2

* Tue Apr 04 2000 Henri Gomez <gomez@slib.fr>
- 0.15.8-1
- Removed backspace patch (included in 0.15.8)

* Tue Feb 15 2000 Henri Gomez <gomez@slib.fr>
- 0.15.7-2
- Backspace problem corrected (Carey Evans Patch)

* Thu Feb 10 2000 Henri Gomez <gomez@slib.fr>
- 0.15.7
- Removed config.guess and config.sub from CVS since they should be
  provided by autogen.sh.
- Added --enable-old-keys switch to configure to compile in the old
  keyboard handler (preparation for 0.15.7).
- Fixed bugs with handling response code for printer sessions.
- Added a response code/error message lookup table so that we can get
  the error message in Plain English (tm).
- Apply patch from Mike Madore regarding IBMTRANSFORM set incorrectly
  (for printer sessions).
- Documented `-P cmd' option in usage message, removed `-p' option to
  indicate print session as `-P cmd' is required for a working session
  anyway.
- Fixed typo in new key-parsing code preventing PgDn from working.
- Added code to handle Esc+Del = Ins vt100 key mapping.
- Added stuff to XTerm resources to turn on real underlining and turn
  off silly color-instead-of-underline mode.
- Throw away weird keys we get from ncurses4 after before first
  keypress.
- Implemented FER (Field-Exit Required) state (not tested).
- Use 'TERM' to determine if terminal is an xterm or xterm-5250, as it
  *works* :) (Thanks to Frank Richter for pointing out bug).
- Apply Frank Richter's cursor-position-on-status-line patch.
- Implement rest of keys for #defined USE_OWN_KEY_PARSING.
- Finally object-orientized translation map stuff, but will have to be
  modified later to handle wide characters/DBCS characters/Unicode -
  however we intend to support different character sets better.
- In Field Exit handling for signed numeric fields, don't NUL-out the last
  (sign) position of the field - this is what Field- and Field+ are for.
- Home key when already in home position should send the Home aid code,
  even when we have a pending insert.  Also, home key should move to the
  beginning of the *first non-bypass field* not the *current field* when
  there is no pending insert (IC address).
- Clear pending insert flag on Clear Unit or Clear Unit Alternate command.

* Wed Jan 12 2000 Henri Gomez <gomez@slib.fr>
- 0.15.6
- Reported by Phil Gregory - display is not inhibited and cursor is not in
  proper place after Write Error Code.
- Implemented Read Immediate Alternate and Read MDT Fields Alternate commands,
  modified tn5250_session_query_reply to indicate that we now support them to
  the host.
- Implemented TD (Transparent Data) order.  There is apparently nowhere to
  indicate this to the host. (This may have been the cause of earlier binary
  data issues).
- Implemented MC (Move Cursor) order.  This is now indicated to the host.
- Move remaining keyboard handling from session.c to display.c, make
  tn5250_display_waitevent NOT return keyboard events. (Might we want to
  pass along ones we don't understand?  Nah...)
- Save/restore message line when Write Error Code is used by the host to
  inhibit display.  Also, use the correct message line (according to the
  format table header).
- Added refresh() call to cursesterm.c.  Hopefully, this will resolve the
  80 -> 132 column switch refresh issues reported by some users.
- Wrote a quick hack of a Perl script to insert Robodoc comment headers
  for all the functions (and manually did all the structures).  Yeah, it's
  ugly, but no-one produces a tool as good as Javadoc which works on C.
- tn5250_dbuffer_send_data_for_fields(): A *SET* bit inhibits the transmission
  of field data, not a clear one.  Also, fine point of spec, all three aid key
  bytes must be present before the 5294 controller will obey any of them.
- Carey Evans' suggestions for new xt5250 script portability, security
  incorporated.
- xt5250: Now changes window title to name of host.
- cursesterm.c: Now obeys the information returned from ENQ about what
  type of terminal, and only uses xterm resize escape when on an xterm
  again.


* Thu Jan  6 2000 Henri Gomez <gomez@slib.fr>
- 0.15.5
- Extensively modified xt5250 script to prompt for hostname if not given,
  automagically use xrdb to load the keyboard mappings.  Inspired by Henri
  (Thanks!)
- Renamed Xdefaults to xt5250.keys, installs in $pkgdatadir, also
  installs Linux keyboard maps there.
- Removed smacs, rmacs, and acsc from 5250.terminfo - we don't use them and
  they don't seem to work under an xterm.  Makes 'dialog' draw all sorts of
  funny looking characters.
- If installing on Linux system, automatically 'tic 5250.terminfo' if
  tic command is found (and user is root).
- Fixed bit-ordering issue causing beeps/screen flashes all the time
  (hopefully).
- Happy Y2K!
- Changed handling of Field+ and Field- in regards to number-only-type
  fields.
- No longer ignores the function key bits in the format table header.  This
  means that we won't transmit the field data for a function key unless the
  AS/400 has requested it.
- Rolled Tn5250Table functionality into Tn5250DBuffer, removed
  formattable.[ch] and resulting duplicate functionality in display.c
- Apparently, the AS/400 and S/36 differ in how they send the client the
  Restore Screen data.  The AS/400 just sends the data raw, while the
  System/36 prefixes it with a X'04' X'12' (Restore Screen) opcode.  This
  is now ignored.
- Removed portsnoop. It doesn't belong here and there's better stuff out
  there (check freshmeat.net).  nc seems to work well, and is installed on
  most distributions by default.
  formattable.[ch] and resulting duplicate functionality in display.c
- Apparently, the AS/400 and S/36 differ in how they send the client the
  Restore Screen data.  The AS/400 just sends the data raw, while the
  System/36 prefixes it with a X'04' X'12' (Restore Screen) opcode.  This
  is now ignored.
- Removed portsnoop. It doesn't belong here and there's better stuff out
  there (check freshmeat.net).  nc seems to work well, and is installed on
  most distributions by default.

* Tue Dec 21 1999 Henri Gomez <gomez@slib.fr>
- 0.15.4
- Rewrite of screen/format table save/restore code to generate Write to Display
  commands and orders.  This should even allow you to resume a session with
  a different emulator and have the restore screen feature still work.  This
  results in a noticable slowdown in situations where the save screen command
  is used.
- Fixes for End key behavior.
- Fixes for Del key behavior, other keys which weren't setting the field's
  modified flag.
- Buffered keystrokes will now cause the display to update.
- Some 'binary' characters now accepted as data characters.
- CC1/CC2 bytes in Read MDT Fields/Read INput Fields commands were not being
  handled.
- Partial work on restructuring... Auto Enter fields now work again.
- Updates to documentation and NEWS, including information about the FAQ and
  mailing list archives.


* Wed Nov 24 1999 Henri Gomez <gomez@slib.fr>
- 0.15.3
  When using --with-slang configure option, no longer cores after signon
  screen.
  When using debug:tracefile syntax, no longer cores after signon screen.
  Fixed assertion found by Sean Porterfield regarding 132-column display.
  Slight work to reduce number of screen updates, although this isn't
  finished.
  Some work on solidifying the lib API.


* Fri Nov 18 1999 Henri Gomez <gomez@slib.fr>
- 0.15.2
 Field Exit and Field + are now seperate functions. '+' in numeric field
  maps to Field +.  Field + changes the sign of the number like it should.
- Re-implemented transmitting signed fields to host.
- Re-implemented Field -.
- Numeric Only and Signed Number field types are handled according to spec
  now, even though the spec is really weird about how they are handled
  (The last digit's zone is changed on Numeric Only on Field -/+, but the
  sign position is changed from ' ' to '-' with Field -/+, and the zone
  shift for that one takes place at transmit.)
- Now ignore garbage keys again.  Why are we getting two decimal 410s when
  we type the first character?  This doesn't make sense unless it's related
  to how we detect the xterm.

* Wed Nov 17 1999 Henri Gomez <gomez@slib.fr>
- 0.15.1
- 3/4ths of the restructuring to make it feasible to use lib5250 for display
  services for applications has been done.
- Lots of cleanup - no longer has duplicate field value data, nor does it have
  many different componenets having a different perception of what the current
  field is.
- Implemented terminal bells.  Whistles yet to come.
- Some minor stuff.  Field Exit Required fields now require field exit, for
  example.

* Tue Nov  2 1999 Henri Gomez <gomez@slib.fr>
- 0.14
- Full FreeBSD support, see the README and other files in the freebsd/
  directory.  Special thanks to Scott Klement for this (I've put his name all
  over the ChangeLog for this -- this way, it's not _my_ fault <g>).
- Linux-specific files moved to linux/ subdir.
- README files updated - now more clear on how to set up X Windows support.
- Field Minus sequence (Esc+M) added.
- Dup key support added.
- Small field exit bug fixed.
- Help key/aid code implemented.
- Fix per Carey Evans for handling right-blank fields.
- Reset key now works even when keyboard is locked.  Possible but unlikely bug
  where reset key could cause the next keystroke to be ignored is fixed.
- C programs which use stdin/stdout will now clear the input line properly.
- A small fix to format table handling code with the Repeat to Address order.
  This problem may never have been observed, but hey...

* Mon Oct 6 1999 Henri Gomez <gomez@slib.fr>
- updated Readme

* Fri Oct 1 1999 Henri Gomez <gomez@slib.fr>
- 0.13.13
- added xrdb load key in xt5250
- added gnome icons entry for xt5250

* Mon Sep 6 1999 Henri Gomez <gomez@slib.fr>
- 0.13.12

* Wed Sep 1 1999 Henri Gomez <gomez@slib.fr>
- 0.13.11
  Initial RPM release
