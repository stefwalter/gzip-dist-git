Summary: The GNU data compression program.
Name: gzip
Version: 1.3.3
Release: 1
License: GPL
Group: Applications/File
Source: ftp://alpha.gnu.org/gnu/gzip/gzip-%{version}.tar.gz
Patch0: gzip-1.3-openbsd-owl-tmp.diff
Patch1: gzip-1.2.4-zforce.patch
Patch2: gzip-1.2.4a-dirinfo.patch
Patch3: gzip-1.3-stderr.patch
Patch4: gzip-1.3.1-zgreppipe.patch
Patch5: gzip-1.3-rsync.patch
URL: http://www.gzip.org/
Prereq: /sbin/install-info
Requires: mktemp less
Buildroot: %{_tmppath}/gzip-%{version}-root

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your Red Hat Linux system, because it is a
very commonly used data compression program.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 
#%patch2 -p1 
%patch3 -p1
%patch4 -p1 -b .nixi
%patch5 -p1 -b .rsync

%build
export DEFS="-DNO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"
%configure  --bindir=/bin
make 
make gzip.info

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall  bindir=$RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -sf ../../bin/gzip $RPM_BUILD_ROOT/usr/bin/gzip
ln -sf ../../bin/gunzip $RPM_BUILD_ROOT/usr/bin/gunzip

for i in  zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore ; do
    mv $RPM_BUILD_ROOT/bin/$i $RPM_BUILD_ROOT/usr/bin/$i
done

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/gzip.info*


cat > $RPM_BUILD_ROOT/usr/bin/zless <<EOF
#!/bin/sh
/bin/zcat "\$@" | /usr/bin/less
EOF
chmod 755 $RPM_BUILD_ROOT/usr/bin/zless

%post
/sbin/install-info %{_infodir}/gzip.info.gz %{_infodir}/dir 

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gzip.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
/bin/*
/usr/bin/*
%{_mandir}/*/*
%{_infodir}/gzip.info*

%changelog
* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.3-1
- 1.3.3

* Sun Mar 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add rsyncable patch #58888

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.2-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.3.2-1
- 1.3.2: no need for autoconf 2.5x hacks anymore

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.3.1:
	- disable patch2

* Fri Oct 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.3.0-16
- replace tempfile patches with improved ones solar@openwall.com
- Add less to the dependency chain - zless needs it

* Thu Aug 23 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.3.0-15
- Fix typo in comment in zgrep (#52465) 
- Copyright -> License

* Tue Jun  5 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Patch various uses of $$ in the bundled scripts

* Mon Jun  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix the SIGPIPE patch to avoid blank lines (#43319)

* Thu Feb 08 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed buzilla bug #26680. Wrong skip value after mktemp patch and forced
  overwrite for output file during decompression.

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- trap SIGPIPE in zgrep, so "zgrep | less" gets a happy ending
  (#24104)

* Sun Dec 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add HAVE_LSTAT define, to avoid it doing weird things to symlinks
  instead of ignoring them as the docs say it should (#22045)

* Fri Dec 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Thu Nov 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patch all scripts so usage error messages are written to 
  stderr (#20597)

* Mon Oct 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable assembly, as it is faster without it (bug #19910)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%{_mandir}, %%{_infodir},  %%configure, %%makeinstall
  and %%{_tmppath}

* Fri May 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add root as default owner of the files, permits building 
  as non-root user

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Build system handles stripping
- Don't do thing the system does, like creating directories
- use --bindir /bin
- Added URL
- skip unnecesarry sed step
- Include THANKS, AUTHORS, ChangeLog, TODO

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3
- handle RPM_OPT_FLAGS

* Tue Feb 15 2000 Cristian Gafton <gafton@redhat.com>
- handle compressed man pages even better

* Tue Feb 08 2000 Cristian Gafton <gafton@redhat.com>
- adopt patch from Paul Eggert to fix detection of the improper tables in
  inflate.c(huft_build)
- the latest released version 1.2.4a, which provides documentation updates
  only. But it lets us use small revision numbers again
- add an dirinfo entry for gzip.info so we can get rid of the ugly --entry
  args to install-info

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Fix bug #7970

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- built against gliibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- added /usr/bin/gzip and /usr/bin/gunzip symlinks as some programs are too
  brain dead to figure out they should be at least trying to use $PATH
- added BuildRoot

* Wed Jan 28 1998 Erik Troan <ewt@redhat.com>
- fix /tmp races

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info
- applied patch for gzexe

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Marc Ewing <marc@redhat.com>
- (Entry added for Marc by Erik) fixed gzexe to use /bin/gzip

