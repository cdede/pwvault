from lib_lewm.copy_clip import   CopyClip
from lib_lewm.export_db import   ExportDb
class Keepass(CopyClip):
    def __init__(self, db,sleep=0,islist = False):
        super(Keepass, self).__init__(sleep)
        self.islist = islist
        assert type(db) == type({})
        self._exp = db


