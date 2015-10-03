from git import Repo, Actor # GitPython
import git.exc as GitExceptions # GitPython
import os
import datetime
from isoweek import Week


name = "Itai Ferber"
email = "itai@itaiferber.net"
name = "dank kush"
email = "jack.fischer11@gmail.com"


def write_commits():
  current_week_num = datetime.date.isocalendar(datetime.date.today())[1]
  current_year_num = datetime.date.today().year

  #make_p(current_year_num, current_week_num - 41) #left p
  #make_p(current_year_num, current_week_num - 14) #right p
  #make_o(current_year_num, current_week_num - 32) #left o
  #make_o(current_year_num, current_week_num - 23) #right o
  #make_year()


def make_year():
  #today = datetime.datetime.today()
  today = make_today_object()
  for i in range(365):
    delta = datetime.timedelta(days=i)
    target_day = today - delta
    commit(target_day)

def make_today_object():
  """bc today() gives seconds etc that throws off brittle formatting, yolo"""
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
  message = "Sweg 420"
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
  write_commits()

