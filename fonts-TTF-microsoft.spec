Summary:	Microsoft TTF fonts
Summary(pl):	Czcionki TTF firmy Microsoft
Name:		fonts-TTF-microsoft
Version:	20020525
Release:	1
License:	Microsoft EULA
Group:		X11/Fonts
URL:		http://www.microsoft.com/truetype/fontpack/
Source0:	http://www.eu.microsoft.com/typography/downloads/andale32.exe
Source1:	http://www.eu.microsoft.com/typography/downloads/arial32.exe
Source2:	http://www.eu.microsoft.com/typography/downloads/arialb32.exe
Source3:	http://www.eu.microsoft.com/typography/downloads/comic32.exe
Source4:	http://www.eu.microsoft.com/typography/downloads/courie32.exe
Source5:	http://www.eu.microsoft.com/typography/downloads/georgi32.exe
Source6:	http://www.eu.microsoft.com/typography/downloads/impact32.exe
Source7:	http://www.eu.microsoft.com/typography/downloads/times32.exe
Source8:	http://www.eu.microsoft.com/typography/downloads/trebuc32.exe
Source9:	http://www.eu.microsoft.com/typography/downloads/verdan32.exe
Source10:	http://www.eu.microsoft.com/typography/downloads/webdin32.exe
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
BuildRequires:	cabextract
BuildRequires:	ttmkfdir
BuildRequires:	util-linux
BuildRequires:	textutils
Requires(post,postun):fileutils
Requires(post,postun):sed
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
%description -l pl
Czcionki TTF firmy Microsoft

%prep
%setup -q -c -T
/usr/bin/cabextract %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
%{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} \
%{SOURCE10}

cat Licen.TXT |more

reply=
while [ x$reply = x ]; do
    echo "Type a - Agree or d - Disagree and then press ENTER"
    read reply leftover
    case $reply in
	a|A)
	    reply=1
	    ;;
	d|D)
	    exit 1
	    ;;
    esac
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.ttf *.TTF $RPM_BUILD_ROOT%{ttffontsdir}
cd $RPM_BUILD_ROOT%{ttffontsdir}
/usr/bin/ttmkfdir |tail +2 >fonts.scale.fonts-TTF-microsoft
cd -
%clean
rm -rf $RPM_BUILD_ROOT

%post
cd %{ttffontsdir}
umask 022
rm -f fonts.scale.bak
cat fonts.scale.* | sort -u > fonts.scale.tmp
cat fonts.scale.tmp | wc -l | sed -e 's/ //g' > fonts.scale
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
cat fonts.scale.tmp | wc -l | sed -e 's/ //g' > fonts.scale
cat fonts.scale.tmp >> fonts.scale
rm -f fonts.scale.tmp fonts.dir
ln -sf fonts.scale fonts.dir
if [ -x /usr/X11R6/bin/xftcache ]; then
	/usr/X11R6/bin/xftcache .
fi

%files
%defattr(644,root,root,755)
%{ttffontsdir}/*
