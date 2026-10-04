from __future__ import annotations

import re
import unittest
from pathlib import Path

COLLECTION = Path(__file__).resolve().parents[1]
ROLES = COLLECTION / "roles"

CONTAINER_ROLES = ("consul", "gerbera", "haproxy", "jenkins", "n8n", "repotekne")


class HardeningRegressionTest(unittest.TestCase):
    def test_service_roles_use_declarative_containers(self) -> None:
        for role in CONTAINER_ROLES:
            tasks = (ROLES / role / "tasks").read_text() if (ROLES / role / "tasks").is_file() else ""
            if not tasks:
                tasks = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in sorted((ROLES / role / "tasks").glob("*.yml"))
                )
            self.assertIn(
                "community.docker.docker_container:",
                tasks,
                f"{role} must declare its container with community.docker",
            )
            self.assertNotRegex(tasks, r"\bdocker\s+(run|create|start|stop|restart|rm)\b")

    def test_container_images_are_pinned(self) -> None:
        for role in CONTAINER_ROLES:
            defaults = (ROLES / role / "defaults" / "main.yml").read_text(encoding="utf-8")
            image_lines = [
                line.split(":", 1)[1].strip()
                for line in defaults.splitlines()
                if re.match(r"^\w*(?:container|docker)_image:", line)
            ]
            self.assertTrue(image_lines, f"{role} has no image default")
            for image in image_lines:
                self.assertNotIn(":latest", image)
                self.assertRegex(image, r"(?:@sha256:[0-9a-f]{64}|:[A-Za-z0-9][A-Za-z0-9._-]*)$")

    def test_consul_acl_uses_collection_modules(self) -> None:
        tasks = (ROLES / "consul" / "tasks" / "main.yml").read_text(encoding="utf-8")
        for module in (
            "community.general.consul_acl_bootstrap:",
            "community.general.consul_policy:",
            "community.general.consul_role:",
            "community.general.consul_token:",
            "community.general.consul_kv:",
        ):
            self.assertIn(module, tasks)

    def test_kubernetes_downloads_have_sha256_checksums(self) -> None:
        defaults = (ROLES / "k8s" / "defaults" / "main.yml").read_text(encoding="utf-8")
        checksums = re.findall(r"^\s+(?:amd64|arm64):\s+([0-9a-f]{64})$", defaults, re.MULTILINE)
        self.assertGreaterEqual(len(checksums), 6)
        self.assertRegex(defaults, r"k8s_containerd_service_commit:\s+[0-9a-f]{40}")


if __name__ == "__main__":
    unittest.main()
