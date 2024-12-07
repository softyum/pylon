# python3 or pypy3.10
import shlex
import argparse
import subprocess
import io
import datetime
import smtplib
from email.message import EmailMessage
from sys import stdout
import logging

log_buffer = io.StringIO()

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # datefmt='%Y-%m-%d %H:%M:%S'
    format="%(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(log_buffer),
        logging.StreamHandler(),
    ],
)


def testlogging():
    logging.info("hello")
    logging.info("world")
    print(log_buffer.getvalue())
    exit(0)


# testlogging()

# parse args
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-c", "--command")
parser.add_argument("-h", "--host")
parser.add_argument("-p", "--port", type=int, default=465)
parser.add_argument("-u", "--user")
parser.add_argument("-P", "--password", default="")
parser.add_argument("-t", "--to", required=False)
parser.add_argument("-s", "--subject")
parser.add_argument("--dry-run", action="store_true")  # # on/off flag
# parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag

parsed_args = parser.parse_args()
ssmtp_host = parsed_args.host
ssmtp_port = parsed_args.port
ssmtp_user = parsed_args.user
ssmtp_password = parsed_args.password
ssmtp_to = parsed_args.to if parsed_args.to else parsed_args.user
ssmtp_subject = parsed_args.subject
job_command = parsed_args.command
dry_run = parsed_args.dry_run


def send_email(recipient_email, subject, body):
    message = EmailMessage()
    message["From"] = ssmtp_user
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)
    if dry_run:
        logging.info(f"dry-run\nSubject: {subject}\nBody: {body}")
    else:
        with smtplib.SMTP_SSL(ssmtp_host, ssmtp_port) as smtp:
            # smtp.starttls(); smtp=smtplib.SMTP('host',587)
            smtp.login(ssmtp_user, ssmtp_password)
            smtp.send_message(message)


def exec_job_command():
    print("\n-- execute job --\n")
    command = job_command
    if isinstance(command, str):
        args = shlex.split(command)
    elif isinstance(command, list):
        args = command

    logging.info(f"cmd: {args}")
    start_at = datetime.datetime.now()
    logging.info(f"start job at: {start_at}")

    result = ""
    if dry_run:
        args = ["echo", "-e", f"'-c = {job_command}'"]

    try:
        proc = subprocess.Popen(
            args,
            cwd="/tmp",
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # set stderr to stdout, then to PIPE by stdout
            bufsize=4096,
        )
        for line in iter(proc.stdout.readline, b""):
            output = line.decode("utf-8")
            logging.info(output)
    except Exception as e:
        # the fetch will handle the error message
        logging.error(e)
        result = "ERROR"
    finally:
        proc.kill()
        return_code = proc.wait(5)
        logging.info(f"Kill code={return_code}")
        result = "Success" if return_code == 0 else "Failed"
        end_at = datetime.datetime.now()
        logging.info(f"finish job at: {end_at}")

    print("\n-- send mail --\n")
    send_email(ssmtp_to, f"[{result}] - {ssmtp_subject}", log_buffer.getvalue())
    # print(log_buffer.getvalue())


if __name__ == "__main__":
    if dry_run:
        print("\n-- args --\n")
        logging.info(parsed_args)
        logging.info(
            f"smtp={ssmtp_host}:{ssmtp_port}, from={ssmtp_user}, to={ssmtp_to}"
        )
    exec_job_command()