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
Release:	4%{?with_license_agreement:wla}
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
# extracted from one of the above
Source20:	Microsoft-EULA.txt
%endif
URL:		http://corefonts.sourceforge.net/
%if %{with license_agreement}
BuildRequires:	cabextract
Requires:	%{_fontsdir}/TTF
Requires(post,postun):	fontpostinst
%else
Requires:	rpm-build-tools
Requires:	wget
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ttffontsdir	%{_fontsdir}/TTF

%description
Microsoft free True Type fonts collection.
%if ! %{with license_agreement}
License issues made us not to include inherent files into this package
by default. If you want to create full working package please build it
with one of the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%{base_name}.install --with license_agreement ftp://ftp.pld-linux.org/dists/ac/PLD/<your_arch>/PLD/RPMS/%{base_name}-{version}-{release}.src.rpm
%endif

%description -l pl
Kolekcja darmowych fontów True Type firmy Microsoft.
%if ! %{with license_agreement}
Kwestie licencji zmusi³y nas do niedo³±czania do tego pakietu istotnych
plików. Je¶li chcesz stworzyæ w pe³ni funkcjonalny pakiet, zbuduj go za
pomoc± polecenia:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
%{base_name}.install --with license_agreement ftp://ftp.pld-linux.org/dists/ac/PLD/<your_arch>/PLD/RPMS/%{base_name}-{version}-{release}.src.rpm
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

%if ! %{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/%{base_name}.install
#!/bin/sh
if [ "\$1" = "--with" -a "\$2" = "license_agreement" ]
then
	TMPDIR=\`rpm --eval "%%{tmpdir}"\`; export TMPDIR
	SPECDIR=\`rpm --eval "%%{_specdir}"\`; export SPECDIR
	SRPMDIR=\`rpm --eval "%%{_srcrpmdir}"\`; export SRPMDIR
	SOURCEDIR=\`rpm --eval "%%{_sourcedir}"\`; export SOURCEDIR
	BUILDDIR=\`rpm --eval "%%{_builddir}"\`; export BUILDDIR
	RPMDIR=\`rpm --eval "%%{_rpmdir}"\`; export RPMDIR
	BACKUP_SPEC=0
	mkdir -p \$TMPDIR \$SPECDIR \$SRPMDIR \$RPMDIR \$SRPMDIR \$SOURCEDIR \$BUILDDIR
	if [ -f \$SPECDIR/%{base_name}.spec ]; then
		BACKUP_SPEC=1
		mv -f \$SPECDIR/%{base_name}.spec \$SPECDIR/%{base_name}.spec.prev
	fi
	if echo "\$3" | grep '\.src\.rpm$' >/dev/null; then
		( cd \$SRPMDIR
		if echo "\$3" | grep '://' >/dev/null; then
			wget --passive-ftp -t0 "\$3"
		else
			cp -f "\$3" .
		fi
		rpm2cpio \`basename "\$3"\` | ( cd \$TMPDIR; cpio -i %{base_name}.spec ) )
		if ! cp -i \$TMPDIR/%{base_name}.spec \$SPECDIR/%{base_name}.spec; then
			exit 1
		fi
	else
		if ! cp -i "\$3" \$SPECDIR; then
			exit 1
		fi
	fi
	( cd \$SPECDIR
	%{_bindir}/builder -nc -ncs --with license_agreement --opts --target=%{_target_cpu} %{base_name}.spec
	if [ "\$?" -ne 0 ]; then
		exit 2
	fi
	RPMNAME=%{base_name}-%{version}-%{release}wla.noarch.rpm
	rpm -U \$RPMDIR/\$RPMNAME || \
		echo -e Install manually the file:\\\n   \$RPMDIR/\$RPMNAME )
	if [ "\$BACKUP_SPEC" -eq 1 ]; then
		mv -f \$SPECDIR/%{base_name}.spec.prev \$SPECDIR/%{base_name}.spec
	fi
else
	cat %{_datadir}/%{base_name}/Microsot-EULA.txt
	echo "
If you accept the above license rebuild the package using:

\$0 --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
fi
EOF

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
%pre
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
