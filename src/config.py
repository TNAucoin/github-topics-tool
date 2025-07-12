"""
Configuration Management
Handles loading and parsing configuration files.
"""

from pathlib import Path

import yaml


def load_config(config_path: str | None = None) -> dict:
	if config_path is None:
		possible_paths = [
			Path.cwd() / "github-topics.yml",
			Path.cwd() / "github-topics.yaml",
			Path.cwd() / ".github-topics.yml",
			Path.home() / ".github-topics.yml",
		]
		config_path = next((p for p in possible_paths if p.exists()), None)

	if config_path and Path(config_path).exists():
		with open(config_path) as f:
			return yaml.safe_load(f) or {}
	return {}


def create_sample_config():
	sample_config = {
		"global_owner": "your-github-username",
		"repositories": [
			{
				"owner": "username",
				"repo": "repository-name",
				"topics": ["python", "cli", "automation"],
			},
			{
				"repo": "another-repo",
				"topics": ["docker", "kubernetes"],
			},
		],
		"global_topics": ["open-source", "github"],
		"settings": {"replace_existing": False, "dry_run": False},
	}

	config_path = Path.cwd() / "github-topics.yml"
	with open(config_path, "w") as f:
		yaml.dump(sample_config, f, default_flow_style=False, sort_keys=False)

	print(f"Sample configuration created at: {config_path}")
	print("Please edit the file to add your GitHub token and repository details.")


def load_repos_from_file(file_path: str) -> list[str]:
	repos = []
	try:
		with open(file_path) as f:
			for line in f:
				line = line.strip()
				if line and not line.startswith("#"):
					repos.append(line)
	except FileNotFoundError:
		print(f"Error: Repository file not found: {file_path}")
		import sys

		sys.exit(1)
	return repos
