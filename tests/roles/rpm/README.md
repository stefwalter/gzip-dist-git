# Ansible role for the test_rpm.yml

Include this role in your test_rpm.yml playbook. You'll need
to have the following variables defined:

 subjects: Space separated list of RPMs to install
 artifacts: An artifacts directory
 tests: A playbook to run inside after installing
