import shlex
import subprocess
import time


def exec_subproc(command: str | list):
    if isinstance(command, str):
        args = shlex.split(command)
    elif isinstance(command, list):
        args = command

    print(f">> cmd: {args}")
    try:
        result = subprocess.check_output(
            args,
            cwd="/tmp",
            shell=False,
        ).decode("utf-8")
        return result
    except Exception as e:
        return "$$Error: " + str(e)


"""
execute shell command, return yield for HttpStreaming
ex.
StreamingHttpResponse(exec_iter_subproc('echo 123'), "text/plain; charset=utf-8")
"""


def exec_iter_subproc(command: str | list, max_yield=20):
    if max_yield > 1000:
        max_yield = 1000
    if isinstance(command, str):
        args = shlex.split(command)
    elif isinstance(command, list):
        args = command

    print(f">> cmd: {args}")
    proc = subprocess.Popen(
        args,
        cwd="/tmp",
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # set stderr to stdout, then to PIPE by stdout
        bufsize=4096,
    )
    try:
        count1 = 0
        for line in iter(proc.stdout.readline, b""):
            yield line.decode("utf-8")
            count1 += 1
            # time.sleep(0.5)
            if count1 > max_yield:
                proc.terminate()
                print(f">> Overyeild: {max_yield} lines, Terminate code={proc.wait(5)}")
                break
    except Exception as e:
        # the fetch will handle the error message
        yield "$$Error: " + str(e)
    finally:
        proc.kill()
        print(f">> Kill code={proc.wait(5)}")
