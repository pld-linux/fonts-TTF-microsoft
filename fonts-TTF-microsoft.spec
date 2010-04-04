# NOTE
# according to EULA we *can* store the .exe's in distfiles in
# unaltered form (that is those .exe files), while can't distribute
# resulting rpm.
#
# Conditional build:
%bcond_with	license_agreement	# generates package

%define		base_name	fonts-TTF-microsoft
%define		rel	11
Summary:	Microsoft TrueType fonts
Summary(pl.UTF-8):	Fonty TrueType firmy Microsoft
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	20020525
Release:	%{rel}%{?with_license_agreement:wla}
License:	Microsoft EULA (for non-commercial use)
Group:		Fonts
%if %{with license_agreement}
Source0:	http://downloads.sourceforge.net/corefonts/andale32.exe
# Source0-md5:	cbdc2fdd7d2ed0832795e86a8b9ee19a
Source1:	http://downloads.sourceforge.net/corefonts/arial32.exe
# Source1-md5:	9637df0e91703179f0723ec095a36cb5
Source2:	http://downloads.sourceforge.net/corefonts/arialb32.exe
# Source2-md5:	c9089ae0c3b3d0d8c4b0a95979bb9ff0
Source3:	http://downloads.sourceforge.net/corefonts/comic32.exe
# Source3-md5:	2b30de40bb5e803a0452c7715fc835d1
Source4:	http://downloads.sourceforge.net/corefonts/courie32.exe
# Source4-md5:	4e412c772294403ab62fb2d247d85c60
Source5:	http://downloads.sourceforge.net/corefonts/georgi32.exe
# Source5-md5:	4d90016026e2da447593b41a8d8fa8bd
Source6:	http://downloads.sourceforge.net/corefonts/impact32.exe
# Source6-md5:	7907c7dd6684e9bade91cff82683d9d7
Source7:	http://downloads.sourceforge.net/corefonts/times32.exe
# Source7-md5:	ed39c8ef91b9fb80f76f702568291bd5
Source8:	http://downloads.sourceforge.net/corefonts/trebuc32.exe
# Source8-md5:	0d7ea16cac6261f8513a061fbfcdb2b5
Source9:	http://downloads.sourceforge.net/corefonts/verdan32.exe
# Source9-md5:	12d2a75f8156e10607be1eaa8e8ef120
Source10:	http://downloads.sourceforge.net/corefonts/webdin32.exe
# Source10-md5:	230a1d13a365b22815f502eb24d9149b
%else
Source21:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source21-md5:	329c25f457fea66ec502b7ef70cb9ede
# extracted from one of the above
Source20:	Microsoft-EULA.txt
%endif
URL:		http://corefonts.sourceforge.net/
%if %{with license_agreement}
BuildRequires:	cabextract
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/TTF
Requires:	%{name}-ariblk
Requires:	fontpostinst
%else
Requires:	cabextract
Requires:	mktemp > 1.5-18
Requires:	rpm-build-macros >= 1.544
Requires:	rpm-build-tools >= 4.4.37
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft free TrueType fonts collection.

%description -l pl.UTF-8
Kolekcja darmowych fontów TrueType firmy Microsoft.

%package ariblk
Summary:	Microsoft TrueType fonts - Arial Black
Group:		Fonts
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/TTF
Requires:	fontpostinst

%description ariblk
Microsoft TrueType fonts - Arial Black.

%prep
%if %{with license_agreement}
%setup -q -c -T
%{_bindir}/cabextract -L %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} \
%{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} \
%{SOURCE10}
mv licen.txt Microsoft-EULA.txt
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
	s,@DATADIR@,%{_datadir}/%{base_name},g
	s,@LICENSE@,%{_datadir}/%{base_name}/Microsoft-EULA.txt,
' %{SOURCE21} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

cp -a %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
install -p %{SOURCE20} $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else
install -d $RPM_BUILD_ROOT%{ttffontsdir}
cp -a *.ttf $RPM_BUILD_ROOT%{ttffontsdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with license_agreement}
%post
fontpostinst TTF

%postun
fontpostinst TTF

%post ariblk
fontpostinst TTF

%postun ariblk
fontpostinst TTF

%else
%post
echo "
If you accept the license enclosed in the file
%{_datadir}/%{base_name}/Microsoft-EULA.txt
and want to install real fonts, then rebuild the package with the
following command:

%{_bindir}/%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%files
%defattr(644,root,root,755)
%if %{with license_agreement}
%doc Microsoft-EULA.txt
%{ttffontsdir}/andalemo.ttf
%{ttffontsdir}/arial.ttf
%{ttffontsdir}/arialbd.ttf
%{ttffontsdir}/arialbi.ttf
%{ttffontsdir}/ariali.ttf
%{ttffontsdir}/comic*.ttf
%{ttffontsdir}/cour*.ttf
%{ttffontsdir}/georgia*.ttf
%{ttffontsdir}/impact.ttf
%{ttffontsdir}/times*.ttf
%{ttffontsdir}/trebuc*.ttf
%{ttffontsdir}/verdana*.ttf
%{ttffontsdir}/webdings.ttf
%else
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%endif

%if %{with license_agreement}
%files ariblk
%defattr(644,root,root,755)
%{ttffontsdir}/ariblk.ttf
%endif
