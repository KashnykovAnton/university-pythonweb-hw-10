import os
import subprocess
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

PG_DUMP_PATH = "/usr/bin/pg_dump"
PG_RESTORE_PATH = "/usr/bin/pg_restore"

env_local = {"PGPASSWORD": os.getenv("POSTGRES_PASSWORD_LOCAL")}
env_docker = {"PGPASSWORD": os.getenv("POSTGRES_PASSWORD")}


def run_command(cmd, env):
    try:
        result = subprocess.run(
            cmd,
            check=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return False


def sync_to_docker():
    print("Syncing local → Docker...")
    local_dump = Path("/tmp/local_dump.dump")

    # fmt: off
    dump_cmd = [
        PG_DUMP_PATH,
        "-U", "postgres",
        "-h", "host.docker.internal",
        "-p", "5432",
        "-F", "c",
        "-f", str(local_dump),
        "contacts"
    ]
    
    restore_cmd = [
        PG_RESTORE_PATH,
        "-U", "postgres",
        "-h", "postgres",
        "-p", "5432",
        "-d", "contacts_docker",
        "-c", str(local_dump),
        "--no-comments"
    ]
    # fmt: on

    if not run_command(dump_cmd, env_local):
        return False
    return run_command(restore_cmd, env_docker)


def sync_to_local():
    print("Syncing Docker → local...")
    docker_dump = Path("/tmp/docker_dump.dump")

    # fmt: off
    dump_cmd = [
        PG_DUMP_PATH,
        "-U", "postgres",
        "-h", "postgres",
        "-p", "5432",
        "-F", "c",
        "-f", str(docker_dump),
        "contacts_docker"
    ]
    
    restore_cmd = [
        PG_RESTORE_PATH,
        "-U", "postgres",
        "-h", "host.docker.internal",
        "-p", "5432",
        "-d", "contacts",
        "-c", str(docker_dump),
        "--no-comments"
    ]
    # fmt: on

    if not run_command(dump_cmd, env_docker):
        return False
    return run_command(restore_cmd, env_local)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "save":
        if not sync_to_local():
            sys.exit(1)
    else:
        if not sync_to_docker():
            sys.exit(1)
