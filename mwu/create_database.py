from mwu.db import Base, engine


from categories.models import *
from expenses.models import *
from user.models import *
from report.models import *


Base.metadata.create_all(bind=engine)
