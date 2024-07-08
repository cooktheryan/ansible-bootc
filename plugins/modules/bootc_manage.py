#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bootc_manage

short_description: Bootc Switch and Upgrade

description:
    - This is a bootc module that manages the switching and upgrading of bootc.

options:
    state:
        description:
            - Control to apply the latest image or switch the image.
            - This is a string value.
            - NOTE: This will not reboot the system. Please use the reboot module to reboot the system.
        required: true
        type: str
    image:
        description:
            - The image to switch to.
            - This is required when state is 'switch'.
        required: false
        type: str

author:
    - Ryan Cook (@cooktheryan)
'''

EXAMPLES = r'''
# Switch to a different image
- name: Provide image to switch to a different image and retain the current running image
  bootc_manage:
    state: switch
    image: "example.com/image:latest"

# Apply updates of the current running image
- name: Apply updates of the current running image
  bootc_manage:
    state: latest
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule

def main():
    argument_spec = dict(
        state=dict(type='str', required=True, choices=['switch', 'latest']),
        image=dict(type='str', required=False)
    )
    module = AnsibleModule(argument_spec=argument_spec)

    state = module.params['state']
    image = module.params['image']

    if state == 'switch':
        if not image:
            module.fail_json(msg="Image is required when state is 'switch'")
        command = f'bootc switch {image} --retain'
        rc, out, err = module.run_command(command)
        if 'Queued for next boot: ' in out:
            result = {'changed': True, 'output': out}
            module.exit_json(**result)
        elif 'Image specification is unchanged.' in out:
                result = {'changed': False, 'stderr': out}
                module.exit_json(**result)
        else:
            result = {'changed': False, 'stderr': err}
            module.fail_json(msg='ERROR: Failed to switch image.', **result)

    elif state == 'latest':
        command = 'bootc upgrade'
        rc, out, err = module.run_command(command)
        if rc == 0 and 'No changes in ' in out:
            result = {'changed': False, 'output': out}
            module.exit_json(**result)
        elif rc == 0 and 'Queued for next boot: ' in out:
            result = {'changed': True, 'output': out}
            module.exit_json(**result)
        else:
            result = {'changed': False, 'stderr': err}
            module.fail_json(msg='ERROR: Failed to apply updates.', **result)

if __name__ == '__main__':
    main()
