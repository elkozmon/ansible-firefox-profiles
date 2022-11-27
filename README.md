Role Name
=========

Create and configure Firefox roles.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

- `jmespath` package (for parsing json):
  `python3-jmespath` in apt, or `py-jmespath` in Macports.
- `py-certifi` port in Macports.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

- jmespath package
  In apt, install `python3-jmespath`.
  In MacPorts, install `py-jmespath`.
- Mozilla CA bundle
  In apt, install `ca-certificates` (I think).
  On MacPorts, install `py-certifi`.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }
		 
    - hosts: desktops
	  roles:
	    - role: firefox
		  vars:
		    profile: work
		    addons:
		      - switchyomega
		      - password-manager
		      # Theme:
		      - solarize-fox
		    security_devices:
		      - name: 2FA Dongle
		        lib: /usr/local/lib/opensc-pkcs15.so
			prefs:
			  extensions.privatebrowsing.notification: "true"
			  # Note the doubly-nested quotes. Necessary for string values.
			  network.proxy.ftp: '"localhost"'
			  network.proxy.ftp_port: 12345
License
-------

BSD

Author Information
------------------

Andrew Arensburger, 2020.
