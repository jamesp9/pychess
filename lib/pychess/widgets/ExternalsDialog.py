import shutil
import os
import stat

from gi.repository import Gtk

from pychess.ic import TimeSeal
from pychess.Savers import pgn
from pychess.System import conf
from pychess.System import uistuff
from pychess.System import download_file
from pychess.System.prefix import getEngineDataPrefix


class ExternalsDialog():
    def __init__(self):
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL, title=_("Ask for permissions"))
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.props.margin_start = 9
        vbox.props.margin_end = 9
        vbox.props.margin_bottom = 9
        self.window.add(vbox)
        uistuff.keepWindowSize("externalsdialog", self.window, (320, 240), uistuff.POSITION_CENTER)

        label = Gtk.Label(_("Some of PyChess features needs your permission to download external programs"))
        vbox.pack_start(label, True, True, 0)

        box = Gtk.Box()
        check_button = Gtk.CheckButton(_("database querying needs scoutfish"))
        check_button.set_active(conf.get("download_scoutfish", False))
        check_button.connect("toggled", lambda w: conf.set("download_scoutfish", w.get_active()))
        box.add(check_button)
        link = "https://github.com/gbtami/scoutfish"
        link_button = Gtk.LinkButton(link, link)
        box.add(link_button)
        vbox.pack_start(box, False, False, 0)

        box = Gtk.Box()
        check_button = Gtk.CheckButton(_("database opening tree needs chess_db"))
        check_button.set_active(conf.get("download_chess_db", False))
        check_button.connect("toggled", lambda w: conf.set("download_chess_db", w.get_active()))
        box.add(check_button)
        link = "https://github.com/gbtami/chess_db"
        link_button = Gtk.LinkButton(link, link)
        box.add(link_button)
        vbox.pack_start(box, False, False, 0)

        box = Gtk.Box()
        check_button = Gtk.CheckButton(_("ICC lag compensation needs timestamp"))
        check_button.set_active(conf.get("download_timestamp", False))
        check_button.connect("toggled", lambda w: conf.set("download_timestamp", w.get_active()))
        box.add(check_button)
        link = "https://www.chessclub.com/user/resources/icc/timestamp"
        link_button = Gtk.LinkButton(link, link)
        box.add(link_button)
        vbox.pack_start(box, False, False, 0)

        check_button = Gtk.CheckButton(_("Don't show this dialog on startup."))
        check_button.set_active(conf.get("dont_show_externals_at_startup", False))
        check_button.connect("toggled", lambda w: conf.set("dont_show_externals_at_startup", w.get_active()))
        vbox.pack_start(check_button, True, True, 0)

        buttonbox = Gtk.ButtonBox()
        close_button = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        close_button.connect("clicked", self.on_close_clicked)
        self.window.connect("delete_event", lambda w, a: self.window.hide())
        buttonbox.add(close_button)
        vbox.pack_start(buttonbox, False, False, 0)

    def show(self):
        self.window.show_all()
        self.window.present()

    def on_close_clicked(self, button):
        altpath = getEngineDataPrefix()
        if pgn.scoutfish_path is None and conf.get("download_scoutfish", False):
            binary = "https://github.com/gbtami/scoutfish/releases/download/20170627/%s" % pgn.scoutfish
            filename = download_file(binary)
            if filename is not None:
                dest = shutil.move(filename, os.path.join(altpath, pgn.scoutfish))
                os.chmod(dest, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
                pgn.scoutfish_path = dest

        if pgn.chess_db_path is None and conf.get("download_chess_db", False):
            binary = "https://github.com/gbtami/chess_db/releases/download/20170627/%s" % pgn.parser
            filename = download_file(binary)
            if filename is not None:
                dest = shutil.move(filename, os.path.join(altpath, pgn.parser))
                os.chmod(dest, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
                pgn.chess_db_path = dest

        if TimeSeal.timestamp_path is None and conf.get("download_timestamp", False):
            binary = "https://www.chessclub.com/user/resources/icc/timestamp/%s" % TimeSeal.timestamp
            filename = download_file(binary)
            if filename is not None:
                dest = shutil.move(filename, os.path.join(altpath, TimeSeal.timestamp))
                os.chmod(dest, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
                TimeSeal.timestamp_path = dest

        self.window.emit("delete-event", None)


externals_dialog = ExternalsDialog()
