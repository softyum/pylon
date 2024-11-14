#!/usr/bin/env python
#!/var/jenkins_home/go/pypy/bin/pypy
# -*- coding: utf-8 -*-

"""
TO run a job in container
1. Loading Job Settings 
2. Ensure Image Match The new version from Git-Server
3. Run job in container with the Image
"""
import shlex
import ast
import json
import os
import sys
import subprocess
import re
import signal
from typing import Union
import urllib

_CONTAINER_CPU = "CONTAINER_CPU"
_CONTAINER_MEMORY = "CONTAINER_MEMORY"
_JOB_NAME = "JOB_NAME"
_BUILD_NUMBER = "BUILD_NUMBER"
_GIT_SERVER = "https://ci.sdinc.cn"
_GIT_BRANCH = "GIT_BRANCH"
_DOCKER_FILE = "DOCKER_FILE"
_POD_CLI = "podman"  # docker


def log(val: object):
    print(val)


def excepthook(exctype, value, traceback):
    print("🔴 An error has been raised:")
    print(value)
    exit(1)
    # sys.__excepthook__(exctype, value, traceback)


sys.excepthook = excepthook


def get_host_by_balance(job_id: int, task_id: int):
    """
    dispatch by the job_id or task_id % count_of_hosts
    """
    hosts = ["etl11", "etl12", "etl31"]
    ix = job_id % hosts.__len__()
    host = hosts[ix]
    print("job %s run on %s" % (job_id, host))
    return host  # default


def getEnv(key: str, default: Union[str, None] = None):
    val = os.getenv(key)
    if val == None:
        if default == None:
            print(">> no env: " + key)
            exit("1")
        return default
    return val


def append_env(cmd: list[str]):  # append environment
    # etl python start command `$run index.py -d dev -u test`
    zyb_pypy_cmd = sys.argv.copy()
    zyb_pypy_cmd.pop(0)
    cmd.append("-e")
    cmd.append("zyb_pypy_cmd=" + zyb_pypy_cmd.__str__())
    # arg_xxxx, ci_xxx
    for k, v in os.environ.items():
        if k.startswith(("arg_", "ci_", "zyb_")) and k != "zyb_pypy_cmd":
            cmd.append("-e")
            cmd.append(k + "=" + v.__str__())


class JobContainer:

    def __init__(self):
        """
        `Run a Job In Container`
        - env.JOB_NAME = path/job_name
        - env.GIT_BRANCH = https://git-server/usr/repos.git#branch_ref:dir
        - env.DOCKER_FILE = https://docs.docker.com/build/concepts/context/#git-repositories
        """
        self.build_number = getEnv(_BUILD_NUMBER, "0")
        self.job_name = getEnv(_JOB_NAME, "debug/job01").lower()
        self.image_name = "img.local/" + self.job_name
        self.container_name = re.sub("[^a-zA-Z0-9\n.]", "-", self.job_name)
        self.container_cpu = getEnv(_CONTAINER_CPU, "1")
        self.container_memory = getEnv(_CONTAINER_MEMORY, "1024MB")

        # https://git-server/usr/repos.git#branch
        self.git_branch = getEnv(_GIT_BRANCH)
        if not self.git_branch.startswith(_GIT_SERVER):
            self.git_branch = _GIT_SERVER + self.git_branch

        self.dockerfile = getEnv(_DOCKER_FILE, "remote-dockerfile")

    def run(self):
        # ensure stop the running container
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def ensure_image(self):
        commit_id = self.get_git_last_commit()
        tag = commit_id[:10]
        image = f"{self.image_name}/{tag}"
        hasImage = self.get_git_commit_id(commit_id)
        aa = JobContainer()
        if not hasImage:
            print("build iamge")
        else:
            pass

    def get_image_by_commit_label(self, git_commit_id):
        # docker image ls --filter "label=org.opencontainers.name=Jenkins project"
        cmd = "docker image ls --format=json --filter label=git.commit.id={git_commit_id}'"
        print(cmd)
        return "image-name:tag"

    def get_git_last_commit(self):
        """
        git ls-remote https://git-server/group/project.git branch
        xxxxx-commit-id-xxxx	refs/heads/branch
        """
        git_branch = "http://git/group/project.git#branch"
        cmd = "git ls-remote" + git_branch.replace("#", " ")
        print(shlex.split(cmd))
        return "xxxxx-commit-id-xxxx"

    def load_env(self):  # load env config
        env_vars = dict()
        # settle __pycache__
        env_vars["PYTHONPYCACHEPREFIX"] = "$HOME/.cache/cpython/"
        # env_vars["PYTHONPATH"] = WORK_DIR
        env_vars["profile"] = "env"  # for zyb run on server
        with open("ENV_CFG/env.prod") as f:  # read env from cfg file
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                key, value = line.strip().split("=", 1)
                env_vars[key] = value
        for k, v in os.environ.items():  # read some args from process-envs
            if not k.startswith("ci_"):  # hidden ci_xxx
                env_vars[k] = v
        # return vars
        return env_vars

    def abort_job_pod(self):
        rtKill = subprocess.call([_POD_CLI, "rm", "-f", "-i", "-t", "1", self.app_name])
        if rtKill == 0:
            print("Abort the job, and success.")
        else:
            print("🔴 Failed to abort job, error=" + rtKill.__str__())
        exit(0)

    def signal_handler(self, signal, frame):
        print("kill job....")
        self.abort_job_pod()
        print("Job aborted!")
        exit(0)


# os.environ["PYTHONUNBUFFERED"] = "1"
# sys.stdout.flush()


if __name__ == "__main__":
    job = JobContainer()
