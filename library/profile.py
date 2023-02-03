#!/usr/bin/python3

# from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: profile
XXX: fill in
'''

EXAMPLES = r'''
- name: "Look up bob's Firefox profiles"
  profile:
    user: bob

- name: "Look up a specific profile file"
  profile:
    path: "/path/to/profiles.ini"
'''

RETURN = r'''
XXX
'''

import os
import platform
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            # User: read this user's profiles.ini file.
            user=dict(type='str', required=False, default=None),
            # Path: read this specific profiles.ini file.
            # Overrides user.
            path=dict(type='str', required=False, default=None),
        ),
        mutually_exclusive=[
            ('user', 'path'),
        ],
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        profiles=None,
        default_profiles=None,
        # XXX - Just for development, I think
        message="",
    )

    user = module.params['user']
    path = module.params['path']

    # Figure out which path to open.
    #
    # On most Unix/Linux systems, it's ~/.mozilla/firefox/profiles.ini .
    #
    # On MacOS, it's ~/Library/Application
    # Support/Firefox/profiles.ini (and the profiles themselves are
    # under ~/Library/Application Support/Firefox/Profiles/).
    #
    # On Windows, it's %APPDATA%\Mozilla\Firefox\profiles.ini .

    if user is None:
        home = "~"
    else:
        home = f"~{user}"
    home = os.path.expanduser(home)

    if path is None:
        system = platform.system()
        if system == "Darwin":
            path = f"{home}/Library/Application Support/Firefox/profiles.ini"
        else:
            path = f"{home}/.mozilla/firefox/profiles.ini"

    result['message'] += f"path: {path}\n"

    if os.path.exists(path):
        result['message'] += "It exists.\n"
    else:
        result['message'] += "It doesn't exist.\n"

    if module.check_mode:
        module.exit_json(**result)

    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    if module.params['name'] == "fail me":
        module.fail_json(msg="You requested failure", **result)

    module.exit_json(**result)


def main():
    run_module()


# Main
if __name__ == "__main__":
    main()
