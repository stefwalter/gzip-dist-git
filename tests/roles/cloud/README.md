# Ansible role for the test_cloud.yml

Include this role in your test_cloud.yml playbook. You'll need
to have the following variables defined:

 subjects: A cloud qcow2 or raw image
 artifacts: An artifacts directory
 tests: A playbook to run inside of the launched instance
