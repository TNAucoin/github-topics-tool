"""
GitHub Topics Manager
Handles all GitHub API interactions for topic management.
"""

import requests


class GitHubTopicsManager:
	def __init__(self, token: str):
		self.token = token
		self.session = requests.Session()
		self.session.headers.update(
			{
				"Authorization": f"token {token}",
				"Accept": "application/vnd.github.mercy-preview+json",
				"User-Agent": "GitHub-Topics-Manager",
			}
		)
		self.base_url = "https://api.github.com"

	def get_repo_topics(self, owner: str, repo: str) -> list[str]:
		url = f"{self.base_url}/repos/{owner}/{repo}/topics"
		response = self.session.get(url)
		response.raise_for_status()
		return response.json().get("names", [])

	def set_repo_topics(self, owner: str, repo: str, topics: list[str]) -> bool:
		url = f"{self.base_url}/repos/{owner}/{repo}/topics"
		data = {"names": topics}
		response = self.session.put(url, json=data)
		response.raise_for_status()
		return response.status_code == 200

	def add_topics(
		self, owner: str, repo: str, new_topics: list[str], replace: bool = False
	) -> dict:
		try:
			current_topics = [] if replace else self.get_repo_topics(owner, repo)

			all_topics = list(set(current_topics + new_topics))

			sanitized_topics = [self._sanitize_topic(topic) for topic in all_topics]
			sanitized_topics = [t for t in sanitized_topics if t]

			self.set_repo_topics(owner, repo, sanitized_topics)

			return {
				"success": True,
				"repo": f"{owner}/{repo}",
				"previous_topics": current_topics,
				"new_topics": sanitized_topics,
				"added": [t for t in sanitized_topics if t not in current_topics],
			}
		except requests.exceptions.RequestException as e:
			return {"success": False, "repo": f"{owner}/{repo}", "error": str(e)}

	def _sanitize_topic(self, topic: str) -> str:
		import re

		sanitized = re.sub(r"[^a-z0-9\-]", "-", topic.lower().replace("_", "-").replace(" ", "-"))
		sanitized = re.sub(r"-+", "-", sanitized).strip("-")
		return sanitized[:35] if sanitized else ""
