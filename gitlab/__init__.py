from pipobot.lib.abstract_modules import NotifyModule

import gitlab

from .model import GitLabProject, GitLabUser, GitLabIssue


class GitLabModule(NotifyModule):
    """A module to follow gitlab's projects"""
    _config = (("url", str, ""), ("token", str, ""), ("ssl_verify", bool, True), ("max_commits", int, 10))

    def __init__(self, bot):
        NotifyModule.__init__(self,
                             bot,
                             name="gitlab",
                             desc="Gitlab Interface",
                             delay=60)
        self.gl = gitlab.Gitlab(self.url, self.token, ssl_verify=self.ssl_verify)
        self.gl.auth()

    def do_action(self):
        print('do action')
        issues = {i.id: i for i in self.bot.sesion.query(GitLabIssue).all()}
        for project in self.bot.session.query(GitLabProject).all():
            commits = project.commits.list(per_page=self.max_commits)
            while commits and commits[0].id != project.last_commit:
                commit = commits.pop(0)
                self.bot.say(_('New commit from %s: %s') % (commit.author_name, commit.title))
            for issue in project.issues.list(all=True):
                if issue.id not in issues.keys():
                    issues[issue.id] = GitLabIssue(id=issue.id)
                    self.bot.session.add(issues[issue.id])
                    self.bot.say(_('New Issue: %s (%s/%i)') % (issue.title, issue.project.web_url, issue.iid))
                issues[issue.id].update_from_gitlab(issue)
        self.bot.session.commit()
        print('done action')
