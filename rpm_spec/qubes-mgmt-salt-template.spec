%{!?version: %define version %(cat version)}

Name       qubes-mgmt-salt-template
Version:   %{version}
Release:   1%{?dist}
Summary:   Formula description
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt

%define _builddir %(pwd)

%description
Formula description.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%post
# Update Salt Configuration
qubesctl state.sls config -l quiet --out quiet > /dev/null || true
qubesctl saltutil.clear_cache -l quiet --out quiet > /dev/null || true
qubesctl saltutil.sync_all refresh=true -l quiet --out quiet > /dev/null || true

# Enable States
qubesctl top.enable template saltenv=base -l quiet --out quiet > /dev/null || true

# Enable Pillar States
qubesctl top.enable template saltenv=base pillar=true -l quiet --out quiet > /dev/null || true

# Enable Test States
#qubesctl top.enable template saltenv=test -l quiet --out quiet > /dev/null || true

# Enable Test Pillar States
#qubesctl top.enable template saltenv=test pillar=true -l quiet --out quiet > /dev/null || true

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/formulas/base/template-formula
/srv/formulas/base/template-formula/LICENSE
/srv/formulas/base/template-formula/README.rst
/srv/formulas/base/template-formula/template/init.sls
/srv/formulas/base/template-formula/template/init.top

%attr(750, root, root) %dir /srv/formulas/test/template-formula/template
/srv/formulas/test/template-formula/LICENSE
/srv/formulas/test/template-formula/README.rst
/srv/formulas/test/template-formula/template/init.sls
/srv/formulas/test/template-formula/template/init.top
/srv/formulas/test/template-formula/template/pillar/template/init.sls
/srv/formulas/test/template-formula/template/pillar/template/init.top

%attr(750, root, root) %dir /srv/pillar/base/template
%config(noreplace) /srv/pillar/base/template/init.sls
/srv/pillar/base/template/init.top

%attr(750, root, root) %dir /srv/pillar/test/template
%config(noreplace) /srv/pillar/test/template/init.sls
/srv/pillar/test/template/init.top

%changelog
