#!/usr/bin/env python

import os
import shutil
import signal
import subprocess
import sys
import tempfile

# HACK: Ansible requires this exact string to be here
from ansible.module_utils.basic import *

#
# Test this module like this
#
# echo '{ "ANSIBLE_MODULE_ARGS": { "subjects": "cloud.qcow2", "playbooks": "test/test_local.yml" } }' \
#        | python tests/library/qemu-playbook.py
#

WANT_JSON = True

USER_DATA ="""#cloud-config
user: root
password: foobar
ssh_pwauth: True
chpasswd:
 expire: False
"""

INVENTORY = "localhost ansible_ssh_port=2222 ansible_ssh_host=127.0.0.3 ansible_ssh_user=root ansible_ssh_pass=foobar ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'"

def main(argv):
    module = AnsibleModule(argument_spec = {
        "subjects": { "required": True, "type": "str" },
        "playbooks": { "required": True, "type": "str" },
        "log": { "required": False, "type": "str" },
    })

    null = open(os.devnull, 'w')

    directory = tempfile.mkdtemp(prefix="launch-cloud")

    metadata = os.path.join(directory, "meta-data")
    with open(metadata, 'w') as f:
        f.write("")

    userdata = os.path.join(directory, "user-data")
    with open(userdata, 'w') as f:
        f.write(USER_DATA)

    cloudinit = os.path.join(directory, "cloud-init.iso")
    subprocess.check_call(["/usr/bin/genisoimage", "-input-charset", "utf-8",
                           "-volid", "cidata", "-joliet", "-rock", "-quiet",
                           "-output", cloudinit, userdata, metadata], stdout=null)

    log = module.params.get("log") or os.devnull

    inventory = os.path.join(directory, "inventory")
    with open(inventory, 'w') as f:
        f.write(INVENTORY)

    pid = os.path.join(directory, "pid")
    subprocess.check_call(["/usr/bin/qemu-system-x86_64", "-m", "1024", module.params["subjects"],
        "-enable-kvm", "-snapshot", "-cdrom", cloudinit,
	"-net", "nic,model=virtio", "-net", "user,hostfwd=tcp:127.0.0.3:2222-:22",
	"-device", "isa-serial,chardev=pts2", "-chardev", "file,id=pts2,path=" + log,
	"-daemonize", "-display", "none", "-pidfile", pid], stdout=null)

    try:

        # wait for ssh to come up
        for tries in range(0, 30):
            try:
                subprocess.check_call(["/usr/bin/ansible", "-i", inventory, "localhost", "-m", "ping"],
                                      stdout=null, stderr=null)
                break
            except subprocess.CalledProcessError:
                time.sleep(3)
        else:
            module.fail_json(msg="Couldn't connect to qemu host: {subjects}".format(**module.params))
            return 0

        cmd = [
            "/usr/bin/ansible-playbook", "-i", inventory, "--skip-tags", "prepare",
            "--extra-vars", "artifacts=/tmp/artifacts"
        ]

        playbooks = module.params["playbooks"]
        if isinstance(playbooks, (list, tuple)):
            cmd += playbooks
        else:
            cmd.append(playbooks)

        proc = subprocess.Popen(cmd, stdin=null, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = proc.communicate()

        if os.getenv("FEDORA_TEST_DIAGNOSE"):
            tty = os.open("/dev/tty", os.O_RDWR)
            os.write(tty, output + "\n\nDIAGNOSE 'foobar': ssh -p 2222 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@127.0.0.3\n")
            os.read(tty, 100)
    finally:

        with open(pid, 'r') as f:
            try:
                os.kill(int(f.read().strip()), signal.SIGTERM)
            except OSError:
                pass

    with open(log, "a") as f:
        f.write(output)

    if proc.returncode == 0:
        shutil.rmtree(directory)
        module.exit_json(changed=False)
    else:
        module.fail_json(msg="The playbook failed on qemu host: {playbooks}".format(**module.params))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
