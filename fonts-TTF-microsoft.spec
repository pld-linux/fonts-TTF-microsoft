#
# Conditional build:
# _with_license_agreement       - generates package
#
Summary:	Microsoft TTF fonts
Summary(pl):	Czcionki TTF firmy Microsoft
Name:		fonts-TTF-microsoft
Version:	20020525
Release:	3
License:	Microsoft EULA (for non-commercial use)
Group:		X11/Fonts
URL:		http://www.microsoft.com/truetype/fontpack/
Source0:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/andale32.exe
Source1:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/arial32.exe
Source2:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/arialb32.exe
Source3:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/comic32.exe
Source4:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/courie32.exe
Source5:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/georgi32.exe
Source6:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/impact32.exe
Source7:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/times32.exe
Source8:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/trebuc32.exe
Source9:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/verdan32.exe
Source10:	ftp://cvsup.pl.freebsd.org/pub/FreeBSD/ports/distfiles/webfonts/webdin32.exe
%if %{!?_with_license_agreement:1}%{?_with_license_agreement:0}
NoSource:	0
NoSource:	1
NoSource:	2
NoSource:	3
NoSource:	4
NoSource:	5
NoSource:	6
NoSource:	7
NoSource:	8
NoSource:	9
NoSource:	10
%endif
BuildRequires:	cabextract
BuildRequires:	ttmkfdir
Requires(post,postun):	fileutils
Requires(post,postun):	textutils
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft free TTF fonts collection.

%description -l pl
Kolekcja darmowych czcionek TTF firmy Microsoft.

%prep
%setup -q -c -T
/usr/bin/cabextract %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
%{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} \
%{SOURCE10}

%if %{!?_with_license_agreement:1}%{?_with_license_agreement:0}
cat Licen.TXT

cat <<EOF

Use:
  rpm -ba --with license_agreement <specfile>
to rebuild the package if you accept the above license.

EOF
exit 1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.ttf *.TTF $RPM_BUILD_ROOT%{ttffontsdir}

cd $RPM_BUILD_ROOT%{ttffontsdir}
/usr/bin/ttmkfdir |tail +2 >fonts.scale.%{name}
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%post
cd %{ttffontsdir}
umask 022
rm -f fonts.scale.bak
cat fonts.scale.* | sort -u > fonts.scale.tmp
cat fonts.scale.tmp | wc -l | tr -d ' ' > fonts.scale
cat fonts.scale.tmp >> fonts.scale
rm -f fonts.scale.tmp fonts.dir
ln -sf fonts.scale fonts.dir
if [ -x /usr/X11R6/bin/xftcache ]; then
	/usr/X11R6/bin/xftcache .
fi

%postun
cd %{ttffontsdir}
umask 022
rm -f fonts.scale.bak
cat fonts.scale.* 2>/dev/null | sort -u > fonts.scale.tmp
cat fonts.scale.tmp | wc -l | tr -d ' ' > fonts.scale
cat fonts.scale.tmp >> fonts.scale
rm -f fonts.scale.tmp fonts.dir
ln -sf fonts.scale fonts.dir
if [ -x /usr/X11R6/bin/xftcache ]; then
	/usr/X11R6/bin/xftcache .
fi

%files
%defattr(644,root,root,755)
%doc Licen.TXT
%{ttffontsdir}/*
