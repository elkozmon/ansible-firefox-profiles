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
    module_args = dict(
        user=dict(type='str', required=True),
        # name=dict(type='str', required=True),
        # new=dict(type='bool', required=False, default=False),
    )

    result = dict(
        changed=False,
        # original_message='',
        # message='',
        profiles=None,
        default_profiles=None,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

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

