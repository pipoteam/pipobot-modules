from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import backref, relationship

from pipobot.lib.bdd import Base


def strptime(string, fmt='%Y-%m-%dT%H:%M:%S.%fZ'):
    return datetime.strptime(string, fmt)


class GitLabProject(Base):
    __tablename__ = 'gitlab_project'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(Text(1000))
    web_url = Column(String(100))
    last_commit = Column(String(40))
    issues = relationship('GitLabIssue', back_populates='project')

    def update_from_gitlab(self, project):
        self.id = project.id
        self.name = project.name
        self.description = project.description
        self.web_url = project.web_url
        self.last_commit = project.commits.list()[0].id


class GitLabUser(Base):
    __tablename__ = 'gitlab_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    web_url = Column(String(100))
    kuid = Column(Integer, ForeignKey('knownuser.kuid'), unique=True)
    knownuser = relationship('KnownUser', backref=backref("user", uselist=False))


class GitLabIssue(Base):
    __tablename__ = 'gitlab_issue'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('gitlab_project.id'))
    author_id = Column(Integer, ForeignKey('gitlab_user.id'))
    assignee_id = Column(Integer, ForeignKey('gitlab_user.id'))
    project = relationship('GitLabProject', back_populates='issues')
    author = relationship('GitLabUser', foreign_keys=[author_id])
    assignee = relationship('GitLabUser', foreign_keys=[assignee_id])
    title = Column(String(100))
    description = Column(Text(1000))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    state = Column(String(10))

    def update_from_gitlab(self, issue):
        updated = strptime(issue.updated_at)
        if self.updated_at and updated == self.updated_at:
            return
        self.id = issue.id
        self.updated_at = updated
        self.created_at = strptime(issue.created_at)
        self.project_id = issue.project_id
        self.author_id = issue.author.id
        if issue.assignee is not None:
            self.assignee_id = issue.assignee.id
        self.title = issue.title
        self.description = issue.description
        self.state = issue.state
