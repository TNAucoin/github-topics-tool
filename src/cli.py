"""
Command Line Interface
Handles argument parsing and CLI interactions.
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from config import create_sample_config, load_config, load_repos_from_file
from topics import GitHubTopicsManager


def parse_arguments():
	parser = argparse.ArgumentParser(description="Manage GitHub repository topics")
	parser.add_argument("--config", "-c", help="Configuration file path")
	parser.add_argument("--repo", "-r", help="Repository in format owner/repo")
	parser.add_argument("--repos", nargs="+", help="Multiple repositories in format owner/repo")
	parser.add_argument("--repos-file", help="File containing list of repositories (one per line)")
	parser.add_argument("--topics", nargs="+", help="Topics to add")
	parser.add_argument(
		"--replace", action="store_true", help="Replace existing topics instead of adding"
	)
	parser.add_argument(
		"--dry-run", action="store_true", help="Show what would be done without making changes"
	)
	parser.add_argument("--init", action="store_true", help="Create a sample configuration file")

	return parser.parse_args()


def get_github_token() -> str:
	load_dotenv()

	token = os.getenv("GITHUB_TOKEN")
	if not token:
		print("Error: GITHUB_TOKEN environment variable is required.")
		print("Please set it in one of these ways:")
		print("  1. export GITHUB_TOKEN=ghp_YourGitHubTokenHere")
		print("  2. Create a .env file with: GITHUB_TOKEN=ghp_YourGitHubTokenHere")
		print("\nFor security reasons, tokens are not stored in config files.")
		sys.exit(1)

	return token


def build_repos_list(args, config: dict) -> list[dict]:
	repos_to_process = []

	if args.repo and args.topics:
		owner, repo = args.repo.split("/", 1)
		repos_to_process.append(
			{"owner": owner, "repo": repo, "topics": args.topics, "replace": args.replace}
		)
	elif args.repos and args.topics:
		for repo_str in args.repos:
			owner, repo = repo_str.split("/", 1)
			repos_to_process.append(
				{"owner": owner, "repo": repo, "topics": args.topics, "replace": args.replace}
			)
	elif args.repos_file and args.topics:
		repo_list = load_repos_from_file(args.repos_file)
		for repo_str in repo_list:
			if "/" in repo_str:
				owner, repo = repo_str.split("/", 1)
				repos_to_process.append(
					{"owner": owner, "repo": repo, "topics": args.topics, "replace": args.replace}
				)
			else:
				print(f"Warning: Skipping invalid repo format: {repo_str}")
	elif config.get("repositories"):
		global_topics = config.get("global_topics", [])
		global_owner = config.get("global_owner")
		replace_mode = config.get("settings", {}).get("replace_existing", False)

		for repo_config in config["repositories"]:
			owner = repo_config.get("owner", global_owner)
			if not owner:
				print(
					f"Error: No owner specified for repo {repo_config.get('repo', 'unknown')}. "
					"Specify 'owner' in repo config or set 'global_owner' in config file."
				)
				continue

			topics = repo_config.get("topics", []) + global_topics
			repos_to_process.append(
				{
					"owner": owner,
					"repo": repo_config["repo"],
					"topics": topics,
					"replace": repo_config.get("replace_existing", replace_mode),
				}
			)
	else:
		print("Error: No repositories specified.")
		print("Options:")
		print("  - Single repo: --repo owner/repo --topics topic1 topic2")
		print("  - Multiple repos: --repos owner/repo1 owner/repo2 --topics topic1 topic2")
		print("  - From file: --repos-file repos.txt --topics topic1 topic2")
		print("  - Config file: provide github-topics.yml")
		print("Run with --init to create a sample config file.")
		sys.exit(1)

	return repos_to_process


def process_repositories(
	manager: GitHubTopicsManager, repos_to_process: list[dict], dry_run: bool = False
) -> list[dict]:
	results = []
	total_repos = len(repos_to_process)

	if total_repos > 5:
		print(f"Processing {total_repos} repositories...")

	for i, repo_info in enumerate(repos_to_process, 1):
		if total_repos > 5:
			print(f"[{i}/{total_repos}] Processing {repo_info['owner']}/{repo_info['repo']}...")

		if dry_run:
			print(
				f"DRY RUN: Would add topics {repo_info['topics']} to {repo_info['owner']}/{repo_info['repo']}"
			)
			continue

		result = manager.add_topics(
			repo_info["owner"], repo_info["repo"], repo_info["topics"], repo_info["replace"]
		)
		results.append(result)

		if result["success"]:
			status = "✅" if total_repos <= 5 else "✅"
			print(f"{status} {result['repo']}: Added topics {result['added']}")
		else:
			status = "❌" if total_repos <= 5 else "❌"
			print(f"{status} {result['repo']}: {result['error']}")

	return results


def print_summary(results: list[dict]):
	if results:
		successful = sum(1 for r in results if r["success"])
		total = len(results)
		print(f"\nCompleted: {successful}/{total} repositories updated successfully")

		if successful < total:
			failed_repos = [r["repo"] for r in results if not r["success"]]
			print(f"Failed repositories: {', '.join(failed_repos)}")


def run_cli():
	args = parse_arguments()

	if args.init:
		create_sample_config()
		return

	config = load_config(args.config)
	token = get_github_token()
	manager = GitHubTopicsManager(token)

	repos_to_process = build_repos_list(args, config)
	dry_run = args.dry_run or config.get("settings", {}).get("dry_run", False)
	results = process_repositories(manager, repos_to_process, dry_run)

	print_summary(results)
