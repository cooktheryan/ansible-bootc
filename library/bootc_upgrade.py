#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bootc_upgrade

short_description: Bootc Upgrade

description:
    - This is a bootc module that manages the upgrading of bootc.

options:
    check:
        description:
            - Control to check for updates without applying them.
            - This is a boolean value.
        required: false
        type: bool
    apply:
        description:
            - Control to apply the updates.
            - This is a boolean value.
            - NOTE: This will not reboot the system. Please use the reboot module to reboot the system.
        required: false
        type: bool

extends_documentation_fragment:
    - my_namespace.bootc.bootc

author:
    - Ryan Cook (@cooktheryan)
'''

EXAMPLES = r'''
# Pass check to check for updates without applying them
- name: Check for updates without applying them
  bootc_upgrade:
    check: true


# Pass apply to apply updates of the current running image
- name: Apply updates of the current running image
  bootc_upgrade:
    apply: true
'''

RETURN = r'''
'''

# bootc_upgrade.py

from ansible.module_utils.basic import *
import json

def main():
    argument_spec = dict(
        check=dict(type='bool', default=False),
        apply=dict(type='bool', default=False)
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if module.params['check']:
        # Check if an update is available without applying it
        print("Checking for updates...")
        # Run bootc upgrade check to verify if an update is available
        # mark the task as changed if an update is available
        command = 'bootc upgrade --check'
        rc, out, err = module.run_command(command)
        # If an update is available, mark the task as changed
        # an example output would be "Update available for"
        if 'Update available for' in out:
            result = {'changed': True}
            module.exit_json(**result)
        else:
            result = {'changed': False}
            module.exit_json(**result)

    if module.params['apply']:
        # Run the command to apply the updates
        # this will download and apply the updates
        # this will not reboot the system
        print("Applying updates...")
        command = 'bootc upgrade'
        rc, out, err = module.run_command(command)
        if 'No update available.' in out:
            result = {'changed': False}
            module.exit_json(**result)
        else:
            result = {'changed': True}
            module.exit_json(**result)

if __name__ == '__main__':#
    main()
