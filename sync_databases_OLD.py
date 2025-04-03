import os
import subprocess
import atexit
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

env_local = {"PGPASSWORD": os.getenv("POSTGRES_PASSWORD_LOCAL")}
env_docker = {"PGPASSWORD": os.getenv("POSTGRES_PASSWORD")}


def sync_dbs():
    print("Syncing local → Docker...")

    # Create temp files in a cross-platform way
    local_dump = Path("/tmp/local_dump.dump")

    try:
        # fmt: off
        subprocess.run(
            [
                "pg_dump",
                "-U", "postgres",
                "-h", "host.docker.internal",
                "-p", "5432",
                "-F", "c",
                "-f", str(local_dump),
                "contacts",
            ],
            check=True,
            env=env_local,
        )

        subprocess.run(
            [
                "pg_restore",
                "-U", "postgres",
                "-h", "postgres",
                "-p", "5432",
                "-d", "contacts_docker",
                "-c", str(local_dump),
                "--no-comments",
            ],
            check=True,
            env=env_docker,
        )
        # fmt: on

        # Register shutdown hook
        atexit.register(sync_docker_to_local)

    except subprocess.CalledProcessError as e:
        print(f"Sync failed: {e}")


def sync_docker_to_local():
    print("Syncing Docker → local before shutdown...")

    docker_dump = Path("/tmp/docker_dump.dump")

    try:
        # fmt: off
        subprocess.run(
            [
                "pg_dump",
                "-U", "postgres",
                "-h", "postgres",
                "-p", "5432",
                "-F", "c",
                "-f", str(docker_dump),
                "contacts_docker",
            ],
            check=True,
            env=env_docker,
        )

        subprocess.run(
            [
                "pg_restore",
                "-U", "postgres",
                "-h", "host.docker.internal",
                "-p", "5432",
                "-d", "contacts",
                "-c", str(docker_dump),
                "--no-comments",
            ],
            check=True,
            env=env_local,
        )
        # fmt: on

    except subprocess.CalledProcessError as e:
        print(f"Shutdown sync failed: {e}")


if __name__ == "__main__":
    sync_dbs()
