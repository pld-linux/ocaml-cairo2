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
Version:	0.6.2
Release:	3
License:	LGPL v3+
Group:		Libraries
#Source0Download: https://github.com/Chris00/ocaml-cairo/releases
Source0:	https://github.com/Chris00/ocaml-cairo/releases/download/%{version}/cairo2-%{version}.tbz
# Source0-md5:	2d13f7ae6c90dd29a72571e7e94dc2dd
URL:		https://github.com/Chris00/ocaml-cairo
BuildRequires:	ocaml >= 1:4.02
BuildRequires:	ocaml-dune
BuildRequires:	ocaml-graphics-devel
%{?with_gtk:BuildRequires:	ocaml-lablgtk2-devel}
BuildRequires:	pkgconfig
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
Summary(pl.UTF-8):	Interfejs OCamla do Cairo - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq ocaml

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
Summary(pl.UTF-8):	Interfejs OCamla do Cairo z płótnem Canvas - część programistyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk = %{version}-%{release}
Requires:	ocaml-lablgtk2-devel

%description gtk-devel
OCaml interface to Cairo with Gtk canvas rendering.

This package contains files needed to develop OCaml programs using
Cairo-Gtk library.

%description gtk-devel -l pl.UTF-8
Interfejs OCamla do biblioteki Cairo z renderowaniem na płótnie Gtk.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki Cairo-Gtk.

%package pango
Summary:	OCaml interface to Cairo - Pango text rendering
Summary(pl.UTF-8):	Interfejs OCamla do biblioteki Cairo - rendering tekstu poprzez Pango
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-lablgtk2

%description pango
OCaml interface to Cairo with Pango text rendering.

This package contains files needed to run bytecode executables using
Cairo-Pango library.

%description pango -l pl.UTF-8
Interfejs OCamla do biblioteki Cairo z renderowaniem tekstu Pango.

Ten pakiet zawiera binaria potrzebne do uruchamiania programów
używających biblioteki Cairo-Pango.

%package pango-devel
Summary:	OCaml interface toa Cairo with Pango - development part
Summary(pl.UTF-8):	Interfejs OCamla do Cairo z Pango - część programistyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-pango = %{version}-%{release}
Requires:	ocaml-lablgtk2-devel

%description pango-devel
OCaml interface to Cairo with Pango text rendering.

This package contains files needed to develop OCaml programs using
Cairo-Pango library.

%description pango-devel -l pl.UTF-8
Interfejs OCamla do biblioteki Cairo z renderowaniem tekstu Pango.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki Cairo-Pango.

%prep
%setup -q -n cairo2-%{version}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

dune install --destdir=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/cairo2/*.mli
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/cairo2{,-gtk,-pango}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcairo_stubs.so
%{_libdir}/ocaml/cairo2/cairo.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/cairo2/cairo.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc src/cairo.mli
%dir %{_libdir}/ocaml/cairo2
%{_libdir}/ocaml/cairo2/META
%{_libdir}/ocaml/cairo2/cairo.cmt
%{_libdir}/ocaml/cairo2/cairo.cmti
%{_libdir}/ocaml/cairo2/cairo.ml
%{_libdir}/ocaml/cairo2/cairo_ocaml.h
%{_libdir}/ocaml/cairo2/dune-package
%{_libdir}/ocaml/cairo2/cairo.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/cairo2/cairo.cmx
%{_libdir}/ocaml/cairo2/cairo.a
%{_libdir}/ocaml/cairo2/cairo.cmxa
%endif
%{_libdir}/ocaml/cairo2/libcairo_stubs.a
%{_libdir}/ocaml/cairo2/opam

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcairo_gtk_stubs.so
%dir %{_libdir}/ocaml/cairo2-gtk
%{_libdir}/ocaml/cairo2-gtk/META
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/cairo2-gtk/cairo_gtk.cmxs
%endif

%files gtk-devel
%defattr(644,root,root,755)
%doc gtk/cairo_gtk.mli
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.cmi
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.cmt
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.cmti
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.ml
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.mli
%{_libdir}/ocaml/cairo2-gtk/dune-package
%{_libdir}/ocaml/cairo2-gtk/opam
%if %{with ocaml_opt}
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.a
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.cmx
%{_libdir}/ocaml/cairo2-gtk/cairo_gtk.cmxa
%endif
%{_libdir}/ocaml/cairo2-gtk/libcairo_gtk_stubs.a
%endif

%files pango
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcairo_pango_stubs.so
%dir %{_libdir}/ocaml/cairo2-pango
%{_libdir}/ocaml/cairo2-pango/META
%{_libdir}/ocaml/cairo2-pango/cairo_pango.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/cairo2-pango/cairo_pango.cmxs
%endif

%files pango-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/cairo2-pango/cairo_pango.cmi
%{_libdir}/ocaml/cairo2-pango/cairo_pango.cmt
%{_libdir}/ocaml/cairo2-pango/cairo_pango.cmti
%if %{with ocaml_opt}
%{_libdir}/ocaml/cairo2-pango/cairo_pango.a
%{_libdir}/ocaml/cairo2-pango/cairo_pango.cmx
%{_libdir}/ocaml/cairo2-pango/cairo_pango.cmxa
%endif
%{_libdir}/ocaml/cairo2-pango/cairo_pango.ml
%{_libdir}/ocaml/cairo2-pango/cairo_pango.mli
%{_libdir}/ocaml/cairo2-pango/dune-package
%{_libdir}/ocaml/cairo2-pango/opam
%{_libdir}/ocaml/cairo2-pango/libcairo_pango_stubs.a
