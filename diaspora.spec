%define debug_package	%{nil}
%define _sname Diaspora_R1_Linux
%define srcdir Diaspora

Summary:	A library for audio labelling
Name:		diaspora
Version:	1.1.1
Release:	1
License:	CCPL
Group:		Sound
Url:		http://diaspora.hard-light.net/
Source0:	http://diaspora.fs2downloads.com/%{_sname}.tar.lzma
#Diaspora_R1_Patch_1.1.tar.lzma::https://copy.com/8wo3AQnYu0bj%2FDiaspora_R1_Patch_1.1.tar.lzma?download=1
Source1:	Diaspora_R1_Patch_1.1.tar.lzma
Source2:	http://diaspora.fs2downloads.com/Diaspora_R1_Patch_1.1.1.tar.lzma
# Patch mugged from AUR
Patch0:		increase_joy_buttons_fixed.patch


BuildRequires:	lua5.1-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	mesa-common-devel
BuildRequires:	config(mesa)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(jansson)	

Requires:		wxlauncher >= 0.9.4


%description
Diaspora: Shattered Armistice is a single and 
multiplayer space fighter combat game 
set in the reimagined Battlestar Galactica universe.



%prep
%setup -qn%{_sname} -a1 -a2
# wxlauncher packed separately, 
# resources are replaced by the upgrade patch. Sflo
rm -r Diaspora/resources Diaspora/wxlauncher
#---------------------------------------------------------------
cd ..
# Upgrade patch
tar -xf %{_sname}/Patch_Files.1.1.tar -C %{_sname}/%{srcdir}
# Upstream fixe 6-th level patch
tar -xf %{_sname}/Diaspora_R1_Patch_1.1.1/Patch_Files.1.1.1.tar -C %{_sname}/%{srcdir}
#----------------------------------------------------------------
# other fix
pushd %{_sname}/%{srcdir}/fs2_open
# increasing the default resolution a bit.
perl -pi -e "s|(640x480)x16 bit|(1024x768)x32 bit|" code/osapi/osapi_unix.cpp
# Increases hard limit of joystick buttons.
%patch0 -p0
popd

%build
cd %{srcdir}/fs2_open
aclocal -I m4
automake --add-missing 
autoconf -i --force

%configure2_5x --enable-speech
%make
cd ..
# get ready the diaspora profile for wxlauncher
sed "s@^folder=.*\$@folder=%{_datadir}/%{name}@;s@pro00099.template.ini@@" pro00099.template.ini > pro00099.ini

%install
install -m755 -d %{buildroot}%{_datadir}/%{name}
cd %{srcdir}

mv *.vp *.png *.bmp mod.ini pro00099.ini data %{buildroot}%{_datadir}/%{name}
find %{buildroot}%{_datadir}/%{name} -type d -exec chmod 755 '{}' \;


%files
%doc %{srcdir}/*.pdf %{srcdir}/*.txt %{srcdir}/*.rtf 
%{_datadir}/%{name}








