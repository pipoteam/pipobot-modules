from pipobot.lib.abstract_modules import NotifyModule

from gitlab import Gitlab

from .model import GitLabProject, GitLabIssue
MSG = {
        'commit': _('New commit on %s from %s: %s'),
        'issue': _('New Issue in %s: %s (%s/issues/%i)'),
        }


class GitLabModule(NotifyModule):
    """A module to follow gitlab's projects"""
    _config = (("url", str, ""), ("token", str, ""),
            ("ssl_verify", bool, True), ("max_commits", int, 10))

    def __init__(self, bot):
        NotifyModule.__init__(self,
                             bot,
                             name="gitlab",
                             desc="Gitlab Interface",
                             delay=60)
        self.gl = Gitlab(self.url, self.token, ssl_verify=self.ssl_verify)
        self.gl.auth()

        # DEBUG
        p = GitLabProject(id=31)
        pr = self.gl.projects.get(31)
        p.update_from_gitlab(pr)
        self.bot.session.add(p)
        self.bot.session.commit()

    def do_action(self):
        issues = {i.id: i for i in self.bot.session.query(GitLabIssue).all()}
        for prj in self.bot.session.query(GitLabProject).all():
            gl_prj = self.gl.projects.get(prj.id)
            commits = gl_prj.commits.list(per_page=self.max_commits)
            last = commits[0].id
            while commits and commits[0].id != prj.last_commit:
                commit = commits.pop(0)
                self.bot.say(MSG['commit'] % (prj.name, commit.author_name, commit.title))
            prj.last_commit = last
            for issue in gl_prj.issues.list(all=True):
                if issue.id not in issues.keys():
                    issues[issue.id] = GitLabIssue(id=issue.id)
                    self.bot.session.add(issues[issue.id])
                    if issue.state == 'opened':
                        self.bot.say(MSG['issue'] % (prj.name, issue.title, prj.web_url, issue.iid))
                issues[issue.id].update_from_gitlab(issue)
        self.bot.session.commit()
