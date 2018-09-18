import os, re, time

def StageRequest(message):
    ts = time.time()
    tmpfile = '/tmp/{ts}.grpc.log'.format(ts=ts)

    if re.match(r'^tail', message):
        tail_cmd = tail(message.split(' ', 1)[1], tmpfile)
        os.system(tail_cmd)

    if re.match(r'^supervisor', message):
        supervisor_cmd = supervisorctl(message.split(' ', 1)[1], tmpfile)
        os.system(supervisor_cmd)

    if re.match(r'^git', message):
        git_cmd = git(message.split(' ', 1)[1], tmpfile)
        os.system(git_cmd)

    if re.match(r'^pip', message):
        pip_cmd = pip(message.split(' ', 1)[1], tmpfile)
        os.system(pip_cmd)

    results = open(tmpfile, 'r').read()

    if os.path.exists(tmpfile):
        os.remove(tmpfile)

    return results

def pip(message, tmpfile):
    result = ''
    if ('-r' in message):
        repo = re.findall(r'-r\s+\w+-?\w+', message)[0].split(' ', 1)[1]
        repo_app = repo
        if (repo == 'edx-platform'):
            if ('freeze' in message):
                result = '/edx/app/edxapp/venvs/edxapp/bin/pip freeze > {tmpfile}'.format(tmpfile=tmpfile)
    return result

def git(message, tmpfile):
    result = ''
    if ('-r' in message):
        repo = re.findall(r'-r\s+\w+-?\w+', message)[0].split(' ', 1)[1]
        repo_app = repo
        if (repo == 'edx-platform'):
            repo_app = 'edxapp'

        if ('status' in message):
            result = 'git -C /edx/app/{repo_app}/{repo}/ status > {tmpfile}'.format(repo_app=repo_app, repo=repo, tmpfile=tmpfile)

        if ('remote' in message):
            result = 'git -C /edx/app/{repo_app}/{repo}/ remote -v > {tmpfile}'.format(repo_app=repo_app, repo=repo, tmpfile=tmpfile)

        if ('log' in message):
            log_commits_num = '-10'
            if (len(re.findall(r'log\s+-\d+', message)) !=0):
                log_commits_num = re.findall(r'log\s+-\d+', message)[0].split(' ', 1)[1]
            result = 'git -C /edx/app/{repo_app}/{repo}/ log {log_commits_num} > {tmpfile}'.format(
                                                                                                repo_app=repo_app,
                                                                                                repo=repo,
                                                                                                log_commits_num=log_commits_num,
                                                                                                tmpfile=tmpfile)
    return result

def supervisorctl(message, tmpfile):
    result = ''
    if ('status' in message):
        result = '/edx/bin/supervisorctl status > {tmpfile}'.format(tmpfile=tmpfile)
    return result

def tail(message, tmpfile):
    result = ''
    service_variant = message.split(' ', 1)[0]
    log_name_pref = 'edx'
    if ('nginx' in service_variant):
        log_name_pref = '*'
    linenum = 50
    if ('-n' in message):
        linenum = re.findall(r'-n\s+\d+', message)[0].split(' ', 1)[1]
    result = 'tail /edx/var/log/{service_variant}/{log_name_pref}.log -n {linenum} > {tmpfile}'.format(
                                                                                                    service_variant=service_variant,
                                                                                                    log_name_pref=log_name_pref,
                                                                                                    linenum=linenum,
                                                                                                    tmpfile=tmpfile)
    return result
