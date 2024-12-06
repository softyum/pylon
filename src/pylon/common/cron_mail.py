import shlex
import argparse
import subprocess
import io
import datetime
import smtplib
from email.message import EmailMessage
from sys import stdout
import logging
from logging import getLogger, basicConfig, StreamHandler

basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", datefmt="%m-%d %H:%M"
)

log_buffer = io.StringIO()
__logger = logging.getLogger(__name__)
__logger.setLevel("INFO")

__file_handler = logging.StreamHandler(log_buffer)
__console_handler = logging.StreamHandler(stdout)
__logger.addHandler(__file_handler)
__logger.addHandler(__console_handler)


# parse args
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-c", "--command")  # positional argument
parser.add_argument("-h", "--host")  # option that takes a value
parser.add_argument("-p", "--port", type=int, default=465)  # option that takes a value
parser.add_argument("-u", "--user")  # option that takes a value
parser.add_argument("-P", "--password", default="")  # option that takes a value
parser.add_argument("-t", "--to", required=False)  # option that takes a value
parser.add_argument("-s", "--subject")  # option that takes a value
# parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag

parsed_args = parser.parse_args()
__logger.info(parsed_args)
ssmtp_host = parsed_args.host
ssmtp_port = parsed_args.port
ssmtp_user = parsed_args.user
ssmtp_password = parsed_args.password
ssmtp_to = parsed_args.to if parsed_args.to else parsed_args.user
ssmtp_subject = parsed_args.subject
job_command = parsed_args.command


def send_email(recipient_email, subject, body):
    message = EmailMessage()
    message["From"] = ssmtp_user
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL(ssmtp_host, ssmtp_port) as smtp:
        # smtp.starttls(); smtp=smtplib.SMTP('host',587)
        smtp.login(ssmtp_user, ssmtp_password)
        smtp.send_message(message)


def exec_job_command():
    command = job_command
    if isinstance(command, str):
        args = shlex.split(command)
    elif isinstance(command, list):
        args = command

    __logger.info(f">> cmd: {args}")
    start_at = datetime.datetime.now()
    __logger.info(f">> start job at: {start_at}")

    proc = subprocess.Popen(
        args,
        cwd="/tmp",
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # set stderr to stdout, then to PIPE by stdout
        bufsize=4096,
    )

    result = ""

    try:
        for line in iter(proc.stdout.readline, b""):
            output = line.decode("utf-8")
            __logger.info(output)
    except Exception as e:
        # the fetch will handle the error message
        logging.error(e)
        result = "ERROR"
    finally:
        proc.kill()
        return_code = proc.wait(5)
        __logger.info(f">> Kill code={return_code}")
        result = "Success" if return_code == 0 else "Failed"
        end_at = datetime.datetime.now()
        __logger.info(f">> finish job at: {end_at}")

    # send_email(ssmtp_to, f"[{result}] - {ssmtp_subject}", log_buffer.getvalue())
    print(log_buffer.getvalue())


if __name__ == "__main__":
    print(
        f">>args: {ssmtp_host}:{ssmtp_port}, from={ssmtp_user}, to={ssmtp_to}, command={job_command}"
    )
    exec_job_command()
