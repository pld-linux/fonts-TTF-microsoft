#
# Conditional build:
# _with_license_agreement       - generates package
#
Summary:	Microsoft True Type fonts
Summary(pl):	Fonty True Type firmy Microsoft
Name:		fonts-TTF-microsoft
Version:	20020525
Release:	4
License:	Microsoft EULA (for non-commercial use)
Group:		Fonts
URL:		http://www.microsoft.com/truetype/fontpack/
Source0:	http://dl.sourceforge.net/corefonts/andale32.exe
# Source0-md5:	cbdc2fdd7d2ed0832795e86a8b9ee19a
Source1:	http://dl.sourceforge.net/corefonts/arial32.exe
# Source1-md5:	9637df0e91703179f0723ec095a36cb5
Source2:	http://dl.sourceforge.net/corefonts/arialb32.exe
# Source2-md5:	c9089ae0c3b3d0d8c4b0a95979bb9ff0
Source3:	http://dl.sourceforge.net/corefonts/comic32.exe
# Source3-md5:	2b30de40bb5e803a0452c7715fc835d1
Source4:	http://dl.sourceforge.net/corefonts/courie32.exe
# Source4-md5:	4e412c772294403ab62fb2d247d85c60
Source5:	http://dl.sourceforge.net/corefonts/georgi32.exe
# Source5-md5:	4d90016026e2da447593b41a8d8fa8bd
Source6:	http://dl.sourceforge.net/corefonts/impact32.exe
# Source6-md5:	7907c7dd6684e9bade91cff82683d9d7
Source7:	http://dl.sourceforge.net/corefonts/times32.exe
# Source7-md5:	ed39c8ef91b9fb80f76f702568291bd5
Source8:	http://dl.sourceforge.net/corefonts/trebuc32.exe
# Source8-md5:	0d7ea16cac6261f8513a061fbfcdb2b5
Source9:	http://dl.sourceforge.net/corefonts/verdan32.exe
# Source9-md5:	12d2a75f8156e10607be1eaa8e8ef120
Source10:	http://dl.sourceforge.net/corefonts/webdin32.exe
# Source10-md5:	230a1d13a365b22815f502eb24d9149b
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
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/TTF
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft free True Type fonts collection.

%description -l pl
Kolekcja darmowych fontów True Type firmy Microsoft.

%prep
%setup -q -c -T
/usr/bin/cabextract -L %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
%{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} \
%{SOURCE10}

%if %{!?_with_license_agreement:1}%{?_with_license_agreement:0}
cat licen.txt

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
install *.ttf $RPM_BUILD_ROOT%{ttffontsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst TTF

%postun
fontpostinst TTF

%files
%defattr(644,root,root,755)
%doc licen.txt
%{ttffontsdir}/*
