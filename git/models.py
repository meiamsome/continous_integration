from django.conf import settings
from django.db import models

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
REPO_FILE_PATH = getattr(settings, 'REPO_FILE_PATH', './repos/')


class Repository(models.Model):
    """Represents a git repository"""
    owner = models.ForeignKey(AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    mainline = models.ForeignKey("Branch", null=True, blank=True, related_name='__not_used')

    def get_name(self):
        return self.owner.username + "/" + self.name

    def __unicode__(self):
        return self.get_name()


class Commit(models.Model):
    """Represents a single commit. previous_commit_left is the last commit in this branch, previous_commit_right is the
    merged commit from a merge commit, if it exists."""
    repository = models.ForeignKey(Repository)
    hash = models.CharField(max_length=40)
    previous_commit_left = models.ForeignKey("Commit", null=True, blank=True, related_name="_next_left_set")
    previous_commit_right = models.ForeignKey("Commit", null=True, blank=True, related_name="_next_right_set")

    def next_commit_set(self):
        return Commit.objects.filter(
            models.Q(previous_commit_left__pk=self.pk) | models.Q(previous_commit_right__pk=self.pk)
        )

    def is_first_commit(self):
        return self.previous_commit_left is None

    def is_merge(self):
        return self.previous_commit_right is not None

    def __unicode__(self):
        return self.hash


class Branch(models.Model):
    """Represents a branch of a git tree, with it's own head"""
    repository = models.ForeignKey(Repository)
    ref = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    head = models.ForeignKey(Commit)

    def __unicode__(self):
        return self.name


class Push(models.Model):
    repository = models.ForeignKey(Repository)
    before = models.ForeignKey(Commit, related_name="pre_pushes")
    after = models.ForeignKey(Commit, related_name="post_pushes")
    time = models.DateTimeField()
    branch = models.ForeignKey(Branch)

    def __unicode__(self):
        return u"Push on %s/%s from %s to %s" % (self.repository, self.branch, self.before, self.after)