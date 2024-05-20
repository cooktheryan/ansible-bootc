# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bootc_switch

short_description: Bootc Switch

description:
    - This is a bootc module that switches the current running image of a bootc managed system.

options:
    retain:
        description:
            - Retain the current running image.
            - This is a boolean value.
        required: false
        type: bool
    image:
        description:
            - The OCI image reference to switch to.
            - This is a string value.
            - NOTE: A reboot is required to apply the changes.
        required: false
        type: str

author:
    - Ryan Cook (@cooktheryan)
'''

EXAMPLES = r'''
# Pass image to switch to a different image
- name: Provide image to switch to a different image
  bootc_switch:
    image: "example.com/image:latest"


# Pass image to switch to a different image and retain the current running image
- name: Provide image to switch to a different image and retain the current running image
  bootc_switch:
    image: "example.com/image:latest"
    retain: true
'''

RETURN = r'''
'''

# bootc_switch.py

from ansible.module_utils.basic import AnsibleModule

def main():
    argument_spec = dict(
        image=dict(type='str', required=True),
        retain=dict(type='bool', default=False)
    )
    module = AnsibleModule(argument_spec=argument_spec)

    image = module.params['image']
    retain = module.params['retain']

    command = f'bootc switch {image}'
    if retain:
        command += ' --retain'

    rc, out, err = module.run_command(command)

    if rc == 0:
        # Assume success if return code is 0
        result = {'changed': True, 'output': out}
        module.exit_json(**result)
    else:
        result = {'changed': False, 'stderr': err}
        module.fail_json(msg='ERROR: Failed to switch image.', **result)

if __name__ == '__main__':
    main()