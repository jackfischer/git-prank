from git import Repo, Actor
import git.exc as GitExceptions
import os, signal, sys, time
import datetime
from isoweek import Week
import itertools


name = "Example Name"
email = "email@example.com"
commit_message = "Wow such git"


def manager():
  pid = os.fork()
  if pid == 0: #child, displays spinner
    show_spinner()
  if pid != 0: #parent, do git work
    write_commits()
    os.kill(pid, signal.SIGKILL)
    print "You're good!"

    
def write_commits():
  current_week_num = datetime.date.isocalendar(datetime.date.today())[1]
  current_year_num = datetime.date.today().year

  make_year()
  for _ in range(10):
    make_p(current_year_num, current_week_num - 41) #left p
    make_p(current_year_num, current_week_num - 14) #right p
    make_o(current_year_num, current_week_num - 32) #left o
    make_o(current_year_num, current_week_num - 23) #right o


def show_spinner():
  sys.stdout.write("Writing commits. This could take a bit... ")
  spinner = itertools.cycle(['- ', '/ ', '| ', '\\ '])
  while True:
    sys.stdout.write(spinner.next())
    sys.stdout.flush()
    time.sleep(0.05)
    sys.stdout.write('\b\b')


def make_year():
  #today = datetime.datetime.today()
  today = make_today_object()
  for i in range(366):
    delta = datetime.timedelta(days=i)
    target_day = today - delta
    commit(target_day)

def make_today_object():
  """bc today() gives seconds etc that throws off brittle formatting"""
  y = datetime.datetime.today().year
  m = datetime.datetime.today().month
  d = datetime.datetime.today().day
  today = datetime.date(y,m,d)
  return today


def make_o(current_year_num, begin_week_num):
  current_week = Week(current_year_num, begin_week_num)
  commit(current_week.wednesday())
  commit(current_week.thursday())
  current_week = Week(current_year_num, begin_week_num + 1 )
  commit(current_week.tuesday())
  commit(current_week.friday())
  current_week = Week(current_year_num, begin_week_num + 2 )
  commit(current_week.tuesday())
  commit(current_week.friday())
  current_week = Week(current_year_num, begin_week_num + 3 )
  commit(current_week.wednesday())
  commit(current_week.thursday())


def make_p(current_year_num, begin_week_num):
  current_week = Week(current_year_num, begin_week_num)
  commit(current_week.monday())
  commit(current_week.tuesday())
  commit(current_week.wednesday())
  commit(current_week.thursday())
  commit(current_week.friday())
  current_week = Week(current_year_num, begin_week_num + 1 )
  commit(current_week.monday())
  commit(current_week.wednesday())
  current_week = Week(current_year_num, begin_week_num + 2 )
  commit(current_week.monday())
  commit(current_week.wednesday())
  current_week = Week(current_year_num, begin_week_num + 3 )
  commit(current_week.monday())
  commit(current_week.tuesday())
  commit(current_week.wednesday())



def commit(dt_obj):
  respository_directory = "."
  new_file_path = "readme.md"

  action_date = dt_obj.isoformat()
  action_date += " 12:00:00"
  message = commit_message
  actor = Actor(name, email)

  try:
      repo = Repo(respository_directory)
  except GitExceptions.InvalidGitRepositoryError:
      print "Error: %s isn't a git repo" % respository_directory
      sys.exit(5)

  os.environ["GIT_AUTHOR_DATE"] = action_date
  os.environ["GIT_COMMITTER_DATE"] = action_date
  repo.index.add([new_file_path])
  repo.index.commit(message, author=actor, committer=actor)


if __name__ == "__main__":
  manager()

