import webserver
import utils
import db_access

crossings = [
    { "crossingId": 1, "state": False },
    { "crossingId": 2, "state": False, "disabled": True },
    { "crossingId": 3, "state": False, "disabled": True }
]

db_access.create_table()

webserver.crossings = crossings
webserver.start()