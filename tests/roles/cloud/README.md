# Ansible role for cloud disk image subjects

Put this role in your test_cloud.yml playbook. You'll need
to have the following variables defined:

 * subjects: A cloud qcow2 or raw image
 * artifacts: An artifacts directory
 * playbooks: A playbook to run inside of the launched instance

Set the FEDORA_TEST_DIAGNOSE=1 environment variable to diagnose
the launch instance when it fails.
