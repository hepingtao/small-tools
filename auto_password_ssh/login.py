#!/home/hepingtao/bin/anaconda3/envs/Py3.10/bin/python
# coding=utf-8
import re
import sys
import pexpect

from host_config import host_ip_env, userpass

PROMPT_COMMAND = r'(\[.*\][$#] )'
PROMPT_CONTINUE = r'Are you sure you want to continue connecting \(yes/no\)\?'
PROMPT_PASSWD = '[Pp]assword: '


def login(host):
    host = str(host)
    try:
        host_ip, env, root_path = host_ip_env[host]
    except:
        print(f"Host {host} is unknown.")
        return
    user_passwd = userpass[env]
    username, password = user_passwd['username'], user_passwd['password']
    child = pexpect.spawn(f'ssh {username}@{host_ip}')
    child.setwinsize(48, 200)
    i = child.expect([pexpect.TIMEOUT, PROMPT_CONTINUE, PROMPT_PASSWD])
    if i == 0:  # Timeout
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        sys.exit(1)
    elif i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.expect(PROMPT_PASSWD)
    # print(child.before.decode('utf-8'), end='')
    # print(child.after.decode('utf-8'), end='')
    child.sendline(password)
    child.expect(PROMPT_COMMAND)
    print(child.before.decode('utf-8').strip('\r\n'), end='')
    print(child.after.decode('utf-8').strip('\r\n'), end='')
    child.sendline(rf'export PS1="{host_ip} $PS1"')
    child.expect(PROMPT_COMMAND)
    print(child.before.decode('utf-8').strip('\r\n'), end='')
    print(child.after.decode('utf-8').strip('\r\n'), end='')
    child.sendline(f'cd {root_path}')

    cmd = ''
    while True:
        i = child.expect([PROMPT_COMMAND, pexpect.EOF])
        if i == 0:
            before = child.before.decode('utf-8')
            before = re.sub(cmd, '', before, flags=re.S)
            before = before.strip('\r\n')
            print(before, end='')
            after = child.after.decode('utf-8')
            # after = re.sub(PROMPT_COMMAND, f'{host_ip}' + r' \1', after)
            after = after.strip('\r\n')
            print(after, end='')
            cmd = input()
            child.sendline(f'{cmd}')
        else:
            child.close()
            break

    # Now we are either at the command prompt or
    # the login process is asking for our terminal type.
    # child.interact()
    # return child


def login_interactive(host):
    host = str(host)
    try:
        host_ip, env, root_path = host_ip_env[host]
    except:
        print(f"Host {host} is unknown.")
        return
    user_passwd = userpass[env]
    username, password = user_passwd['username'], user_passwd['password']
    child = pexpect.spawn(f'ssh {username}@{host_ip}')
    child.setwinsize(48, 200)
    i = child.expect([pexpect.TIMEOUT, PROMPT_CONTINUE, PROMPT_PASSWD])
    if i == 0:  # Timeout
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        sys.exit(1)
    elif i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.expect(PROMPT_PASSWD)
    # print(child.before.decode('utf-8'), end='')
    # print(child.after.decode('utf-8'), end='')
    child.sendline(password)
    child.expect(PROMPT_COMMAND)
    print(child.before.decode('utf-8').strip('\r\n'), end='')
    print(child.after.decode('utf-8').strip('\r\n'), end='')
    # child.sendline(r'export PS1="$(hostname -i) [\u@\h \W]\$"')
    child.sendline(rf'export PS1="{host_ip} $PS1"')
    child.sendline(f'cd {root_path}')
    child.interact()
    # return child


def scp(scp_args):
    *scp_opt, source, target = scp_args
    scp_opt = ' '.join(scp_opt)
    host = ''
    source_path = ''
    target_path = ''
    try:
        host, source_path = source.split(':')
    except ValueError:
        pass
    try:
        host, target_path = target.split(':')
    except ValueError:
        pass
    try:
        host_ip, env, root_path = host_ip_env[host]
    except:
        print(f"Host {host} is unknown.")
        return
    user_passwd = userpass[env]
    username, password = user_passwd['username'], user_passwd['password']
    if source_path:
        source = f'{username}@{host_ip}:{source_path}'
    if target_path:
        target = f'{username}@{host_ip}:{target_path}'
    if scp_opt:
        scp_full_cmd = f'scp {scp_opt} {source} {target}'
    else:
        scp_full_cmd = f'scp {source} {target}'
    print(scp_full_cmd)
    child = pexpect.spawn(scp_full_cmd)
    i = child.expect([pexpect.TIMEOUT, PROMPT_CONTINUE, PROMPT_PASSWD])
    if i == 0:  # Timeout
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        sys.exit(1)
    elif i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.expect(PROMPT_PASSWD)
    child.sendline(password)
    child.interact()


if __name__ == '__main__':
    try:
        target_host_ip = sys.argv[1]
    except IndexError:
        print("No target given.")
        sys.exit(1)
    login(target_host_ip)
