# Ansible role for RPM subjects

Put this role in your test_rpm.yml playbook. You'll need
to have the following variables defined:

 * subjects: Space separated list of RPMs to install
 * artifacts: An artifacts directory

Include any playbooks after this role with tests you want to
run. For example test_local.yml
