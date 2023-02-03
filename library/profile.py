#!/usr/bin/python3

# from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
module: profile
XXX: fill in
'''

EXAMPLES = r'''
XXX
'''

RETURN = r'''
XXX
'''

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
        # original_message='',
        # message='',
        profiles=None,
        default_profiles=None,
    )

    if module.check_mode:
        result['message'] = "Just checking"
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

