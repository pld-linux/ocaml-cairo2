# TODO: C optflags (currently are taken from ocamlc -config)
#
# Conditional build:
%bcond_without	gtk		# lablgtk2 interface (cairo_gtk)
%bcond_without	ocaml_opt	# build opt (native code)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	OCaml interface to Cairo
Summary(pl.UTF-8):	Interfejs OCamla do biblioteki Cairo
Name:		ocaml-cairo2
Version:	0.5
Release:	2
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://github.com/Chris00/ocaml-cairo/releases
Source0:	https://github.com/Chris00/ocaml-cairo/releases/download/%{version}/cairo2-%{version}.tar.gz
# Source0-md5:	7081cf03e729ce05e5399d3023f267c2
URL:		https://github.com/Chris00/ocaml-cairo
BuildRequires:	ocaml >= 1:3.11.2
%{?with_gtk:BuildRequires:	ocaml-lablgtk2-devel}
BuildRequires:	ocaml-x11graphics-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCaml interface to Cairo, a 2D vector graphics library.

This package contains files needed to run bytecode executables using
Cairo library.

%description -l pl.UTF-8
Interfejs OCamla do biblioteki dwuwymiarowej grafiki wektorowej Cairo.

Ten pakiet zawiera binaria potrzebne do uruchamiania programów
używających biblioteki Cairo.

%package devel
Summary:	OCaml interface to Cairo - development part
Summary(pl.UTF-8):	Interfejs OCamla do Cairo - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
OCaml interface to Cairo, a 2D vector graphics library.

This package contains files needed to develop OCaml programs using
Cairo library.

%description devel -l pl.UTF-8
Interfejs OCamla do biblioteki dwuwymiarowej grafiki wektorowej Cairo.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki Cairo.

%package gtk
Summary:	OCaml interface to Cairo - Gtk canvas rendering
Summary(pl.UTF-8):	Interfejs OCamla do biblioteki Cairo - rendering na płótnie Gtk
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-lablgtk2

%description gtk
OCaml interface to Cairo with Gtk canvas rendering.

This package contains files needed to run bytecode executables using
Cairo-Gtk library.

%description gtk -l pl.UTF-8
Interfejs OCamla do biblioteki Cairo z renderowaniem na płótnie Gtk.

Ten pakiet zawiera binaria potrzebne do uruchamiania programów
używających biblioteki Cairo-Gtk.

%package gtk-devel
Summary:	OCaml interface to Cairo with Gtk canvas - development part
Summary(pl.UTF-8):	Interfejs OCamla do Cairo z płótnem Canvas - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk = %{version}-%{release}
Requires:	ocaml-lablgtk2-devel

%description gtk-devel
OCaml interface to Cairo with Gtk canvas rendering.

This package contains files needed to develop OCaml programs using
Cairo library.

%description gtk-devel -l pl.UTF-8
Interfejs OCamla do biblioteki Cairo z renderowaniem na płótnie Gtk.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki Cairo.

%prep
%setup -q -n cairo2-%{version}

%build
ocaml setup.ml -configure \
	%{?with_gtk:--enable-lablgtk2} \
	--enable-tests

ocaml setup.ml -build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

ocaml setup.ml -install

# adjust to PLD layout
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cairo2
%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo2/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cairo2/META
cat >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/cairo2/META <<EOF
directory = "+cairo2"
EOF

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo2/*.mli
# just for developers?
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo2/*.{annot,cmt*}
# useless with rpm
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so.owner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcairo2_stubs.so
%{_libdir}/ocaml/cairo2/cairo2.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/cairo2/cairo2.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc src/cairo.mli
%dir %{_libdir}/ocaml/cairo2
%{_libdir}/ocaml/cairo2/cairo.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/cairo2/cairo.cmx
%{_libdir}/ocaml/cairo2/cairo2.a
%{_libdir}/ocaml/cairo2/cairo2.cmxa
%endif
%{_libdir}/ocaml/cairo2/libcairo2_stubs.a
%{_libdir}/ocaml/site-lib/cairo2

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcairo_gtk_stubs.so
%{_libdir}/ocaml/cairo2/cairo_gtk.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/cairo2/cairo_gtk.cmxs
%endif

%files gtk-devel
%defattr(644,root,root,755)
%doc src/cairo_gtk.mli
%{_libdir}/ocaml/cairo2/cairo_gtk.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/cairo2/cairo_gtk.a
%{_libdir}/ocaml/cairo2/cairo_gtk.cmx
%{_libdir}/ocaml/cairo2/cairo_gtk.cmxa
%endif
%{_libdir}/ocaml/cairo2/libcairo_gtk_stubs.a
%endif
