#!/home/hepingtao/bin/anaconda3/envs/Py3.10/bin/python
# coding-utf8
import sys

import pexpect

from vpn_config import vpn_connect_config, vpn_username, vpn_password


def conn_vpn(env):
    spaw_cmd = vpn_connect_config.get(env)
    if not spaw_cmd:
        print(f"Env name error, it must be the name in {set(vpn_connect_config)}")
        sys.exit(1)

    print(f'env: {env}, spaw_cmd: {spaw_cmd}')
    for action_id in range(1, 3):
        child_process = pexpect.spawnu(spaw_cmd)

        child_process.expect('Enter Auth Username:')
        print(child_process.before, end='')
        print(child_process.after, end='')
        child_process.sendline(vpn_username)

        child_process.expect('Enter Auth Password:')
        print(child_process.before, end='')
        print(child_process.after, end='')
        child_process.sendline(vpn_password)

        child_process.expect('Please input SMS verify code:')
        print(child_process.before, end='')
        print(child_process.after, end='')

        # First time, fetch the SMS verification code
        if action_id == 1:
            child_process.sendline('')
            child_process.interact()
            # child_process.close()
        # Second time, use the verification code to connect OpenVPN
        elif action_id == 2:
            child_process.interact()
        print('is alive:', child_process.isalive())


if __name__ == '__main__':
    try:
        env = sys.argv[1]
    except IndexError:
        print("Please input a env name")
        sys.exit(1)

    conn_vpn(env)
