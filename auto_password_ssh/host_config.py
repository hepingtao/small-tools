# coding=utf-8

userpass = {
    'test': {
        'username': '',
        'password': ''
    },
    'prod': {
        'username': '',
        'password': ''
    }
}

port = 22
hosts = [
    {
        ('test', ('/data/bigdata/v1/bin',)): [
            '192.168.*.*',
        ]
    },
]

host_ip_env = {}
for env_hosts in hosts:
    for env, host_ips in env_hosts.items():
        for host_ip in host_ips:
            short_host_ip_1 = host_ip.split('.')[-1]
            short_host_ip_2 = '.'.join(host_ip.split('.')[-2:])
            short_host_ip_3 = '.'.join(host_ip.split('.')[-3:])
            host_ip_env[short_host_ip_1] = (host_ip, env[0], env[1][0])
            host_ip_env[short_host_ip_2] = (host_ip, env[0], env[1][0])
            host_ip_env[short_host_ip_3] = (host_ip, env[0], env[1][0])
            host_ip_env[host_ip] = (host_ip, env[0], env[1][0])
