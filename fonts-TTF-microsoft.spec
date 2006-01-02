#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
Summary:	Microsoft True Type fonts
Summary(pl):	Fonty True Type firmy Microsoft
%define		base_name	fonts-TTF-microsoft
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	20020525
Release:	6%{?with_license_agreement:wla}
License:	Microsoft EULA (for non-commercial use)
Group:		Fonts
%if %{with license_agreement}
Source0:	http://dl.sourceforge.net/corefonts/andale32.exe
# NoSource0-md5:	cbdc2fdd7d2ed0832795e86a8b9ee19a
Source1:	http://dl.sourceforge.net/corefonts/arial32.exe
# NoSource1-md5:	9637df0e91703179f0723ec095a36cb5
Source2:	http://dl.sourceforge.net/corefonts/arialb32.exe
# NoSource2-md5:	c9089ae0c3b3d0d8c4b0a95979bb9ff0
Source3:	http://dl.sourceforge.net/corefonts/comic32.exe
# NoSource3-md5:	2b30de40bb5e803a0452c7715fc835d1
Source4:	http://dl.sourceforge.net/corefonts/courie32.exe
# NoSource4-md5:	4e412c772294403ab62fb2d247d85c60
Source5:	http://dl.sourceforge.net/corefonts/georgi32.exe
# NoSource5-md5:	4d90016026e2da447593b41a8d8fa8bd
Source6:	http://dl.sourceforge.net/corefonts/impact32.exe
# NoSource6-md5:	7907c7dd6684e9bade91cff82683d9d7
Source7:	http://dl.sourceforge.net/corefonts/times32.exe
# NoSource7-md5:	ed39c8ef91b9fb80f76f702568291bd5
Source8:	http://dl.sourceforge.net/corefonts/trebuc32.exe
# NoSource8-md5:	0d7ea16cac6261f8513a061fbfcdb2b5
Source9:	http://dl.sourceforge.net/corefonts/verdan32.exe
# NoSource9-md5:	12d2a75f8156e10607be1eaa8e8ef120
Source10:	http://dl.sourceforge.net/corefonts/webdin32.exe
# NoSource10-md5:	230a1d13a365b22815f502eb24d9149b
%else
Source0:	license-installer.sh
# extracted from one of the above
Source20:	Microsoft-EULA.txt
%endif
URL:		http://corefonts.sourceforge.net/
%if %{with license_agreement}
BuildRequires:	cabextract
Requires:	%{_fontsdir}/TTF
Requires(post,postun):	fontpostinst
%else
Requires:	cabextract
Requires:	rpm-build-tools
Requires:	wget
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft free True Type fonts collection.
%if %{without license_agreement}
License issues made us not to include inherent files into this package
by default. If you want to create full working package please build it
with one of the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%description -l pl
Kolekcja darmowych fontów True Type firmy Microsoft.
%if %{without license_agreement}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików. Je¶li chcesz stworzyæ w pe³ni funkcjonalny pakiet, zbuduj go za
pomoc± polecenia:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%endif

%prep
%if %{with license_agreement}
%setup -q -c -T
/usr/bin/cabextract -L %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
%{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} \
%{SOURCE10}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@LICENSE@,%{_datadir}/%{base_name}/Microsoft-EULA.txt,
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install %{SOURCE20} $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT%{ttffontsdir}
install *.ttf $RPM_BUILD_ROOT%{ttffontsdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with license_agreement}
%post
fontpostinst TTF

%postun
fontpostinst TTF

%else
%post
echo "
If you accept the license enclosed in the file
%{_datadir}/%{base_name}/Microsoft-EULA.txt
and want to install real fonts, then rebuild the package with the
following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%files
%defattr(644,root,root,755)
%if %{with license_agreement}
%doc licen.txt
%{ttffontsdir}/*
%else
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%endif
