from Model import db_model
from View import db_view
from Controller import db_controller

m = db_model("postgres", "postgres", "anonimus", "127.0.0.1")
v = db_view()
c = db_controller(m, v)
