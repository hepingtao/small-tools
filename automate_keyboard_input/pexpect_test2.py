import pexpect

vpn_connect_config = [
    {
        'name': 'test',
        'spaw_cmd': 'vpn_test.sh'
    },
    {
        'name': 'prod',
        'spaw_cmd': 'vpn_prod.sh'
    }
]

vpn_username, vpn_password = '', ''

for env in vpn_connect_config:
    env_name, spaw_cmd = env['name'], env['spaw_cmd']
    print(f'env: {env_name}, spaw_cmd: {spaw_cmd}')

    for action_id in range(1, 3):
        child_process = pexpect.spawnu('bash', ['-c', spaw_cmd])

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

        # First time, fetch the SMS verification code
        if action_id == 1:
            print(child_process.after, end='')
            child_process.sendline('')
            child_process.expect(pexpect.EOF)
            print(child_process.before, end='')
            child_process.close()
        # Second time, use the verification code to connect OpenVPN
        elif action_id == 2:
            print(child_process.after, end='\n')
            sms_verify_code = input("sms_verify_code: ")
            child_process.sendline(sms_verify_code)
            child_process.expect('Initialization Sequence Completed', timeout=30)
            print(child_process.before, end='')
            print(child_process.after, end='\n')
        print('is alive:', child_process.isalive())
