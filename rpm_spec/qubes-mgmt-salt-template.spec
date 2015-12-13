%{!?version: %define version %(make get-version)}
%{!?rel: %define rel %(make get-release)}
%{!?package_name: %define package_name %(make get-package_name)}
%{!?package_summary: %define package_summary %(make get-summary)}
%{!?package_description: %define package_description %(make get-description)}

%{!?formula_name: %define formula_name %(make get-formula_name)}
%{!?state_name: %define state_name %(make get-state_name)}
%{!?saltenv: %define saltenv %(make get-saltenv)}
%{!?pillar_dir: %define pillar_dir %(make get-pillar_dir)}
%{!?formula_dir: %define formula_dir %(make get-formula_dir)}

Name:      %{package_name}
Version:   %{version}
Release:   %{rel}%{?dist}
Summary:   %{package_summary}
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt

%define _builddir %(pwd)

%description
%{package_description}

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
qubesctl top.enable %{state_name} saltenv=%{saltenv} -l quiet --out quiet > /dev/null || true

# Enable Pillar States
qubesctl top.enable %{state_name} saltenv=%{saltenv} pillar=true -l quiet --out quiet > /dev/null || true

# Enable Test States
#qubesctl top.enable %{state_name} saltenv=test -l quiet --out quiet > /dev/null || true

# Enable Test Pillar States
#qubesctl top.enable %{state_name} saltenv=test pillar=true -l quiet --out quiet > /dev/null || true

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
