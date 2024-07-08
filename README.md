# WIP Ansible Module for Bootc
This is a WIP module for using Ansible to upgrade and switch Bootc managed systems.

### Playbooks

The module only has two options switch and upgrade.

To switch the currently running Bootc image run the following in an Ansible playbook.

```yaml
---
- name: Using Bootc collection
  hosts: localhost
  tasks:
  - name: Switch bootc
    cooktheryan.bootc.bootc_manage:
      state: switch
      image: quay.io/rcook/bootc-chatbot:1
```

To upgrade to a new image for a system running Bootc run the following Ansible playbook.

```yaml
---
- name: Using Bootc collection
  hosts: localhost
  tasks:
  - name: Upgrade bootc
    cooktheryan.bootc.bootc_upgrade:
      state: latest
```

Both of these functions require a reboot to be added to the playbook to officially use the new image.

```yaml
  - name: Reboot the system
    ansible.builtin.reboot:
    when: result.changed
```