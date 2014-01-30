#encoding: utf-8
import gtk
import gobject
import threading
import image_retriver
from image_retriver import ImageRetriver
import database
import os
import subprocess
import sys


class ImageRetriverApp(gtk.Window):
    """
    Graficzne GUI dla ImageRetriver
    """

    def __init__(self):
        """
        Rysowanie GUI, ustawianie zmiennych, wgranie obrazków jeśli już jakieś są
        """
        super(ImageRetriverApp, self).__init__()

        self.database = database.Database()
        self.database.connect()
        self.database.prepare_database()
        self.lblCountImagesInfo = gtk.Label("Tapet: ")
        self.lblCountImages = gtk.Label()
        self.refreshImagesCount()
        self.database.disconnect()

        self.threads_counter = 0
        self.refresh_all = True

        self.set_title("ImageRetriver from 4Chan")
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        self.resize(900, 600)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#DBDBDB'))

        self.create_menu()

        imgLogo = gtk.Image()
        imgLogo.set_from_file('logo.png')

        lblRetriveImages = gtk.Label()
        lblRetriveImages.set_padding(0, 10)
        lblRetriveImages.set_justify(gtk.JUSTIFY_CENTER)
        lblRetriveImages.set_markup("<span size='15000'><b>Pobierz tapety</b></span>")

        self.lblInfo = gtk.Label()

        self.cmbPages = gtk.combo_box_new_text()
        self.refreshPages()
        self.cmbPages.set_active(0)
        self.cmbPages.connect("changed", self.change_page)

        lblAbout = gtk.Label("Na jedną stronę przypada około 50-70 zdjęć. Miej to na uwadzę wskazując katalog zapisu i ilość stron do przetworzenia!")
        lblAbout.set_line_wrap(50)
        lblAbout.set_size_request(280, 200)

        lblUrl = gtk.Label("Adres URL")
        self.entryUrl = gtk.Entry()
        self.entryUrl.set_text('http://boards.4chan.org/wg/')

        lblPages = gtk.Label("Zakres stron")
        self.entryPages = gtk.Entry()
        self.entryPages.set_text('1')
        self.entryPages.set_width_chars(3)

        self.entryPagesEnd = gtk.Entry()
        self.entryPagesEnd.set_text('1')
        self.entryPagesEnd.set_width_chars(3)

        self.entryCatalogPath = gtk.Entry()
        self.entryCatalogPath.set_text(os.path.dirname(__file__))

        self.btnDownload = gtk.Button("Pobierz")
        self.btnDownload.connect("clicked", self.retrive_images)
        self.btnDownload.set_size_request(80, 25)

        self.btnCatalogChooser = gtk.Button("Wybierz katalog")
        self.btnCatalogChooser.connect("clicked", self.choose_catalog)
        self.btnCatalogChooser.set_size_request(80, 25)

        table = gtk.Table(5, 2, False)
        table.set_border_width(10)

        table.attach(lblRetriveImages, 0, 2, 0, 1)

        table.attach(lblUrl, 0, 2, 1, 2)
        table.attach(self.entryUrl, 0, 2, 2, 3)

        table.attach(lblPages, 0, 1, 3, 4)
        pagesHBox = gtk.HBox()
        pagesHBox.pack_start(self.entryPages, False, False)
        pagesHBox.pack_start(gtk.Label(" - "), False, False)
        pagesHBox.pack_start(self.entryPagesEnd, False, False)
        table.attach(pagesHBox, 1, 2, 3, 4)

        table.attach(self.btnCatalogChooser, 0, 1, 4, 5)
        table.attach(self.entryCatalogPath, 1, 2, 4, 5)

        smallHBox = gtk.HBox(False)
        smallHBox.pack_end(self.btnDownload, False)

        pagesHBox = gtk.HBox(False)
        pagesHBox.pack_start(gtk.Label("Strona: "))
        pagesHBox.pack_end(self.cmbPages)

        vBox = gtk.VBox()
        vBox.pack_start(imgLogo, False)
        vBox.pack_start(table, False)
        vBox.pack_start(smallHBox, False)
        vBox.pack_start(pagesHBox, False)
        vBox.pack_start(self.lblInfo, True)
        vBox.pack_start(lblAbout, False)

        countImagesHBox = gtk.HBox(False)
        countImagesHBox.pack_start(self.lblCountImagesInfo)
        countImagesHBox.pack_start(self.lblCountImages)

        vBox.pack_end(countImagesHBox, True)

        self.scrolledwindow = gtk.ScrolledWindow()
        self.refreshImagesTable()
        self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolledwindow.add_with_viewport(self.images_table)
        self.scrolledwindow.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))

        hBox = gtk.HBox()
        hBox.pack_start(vBox, False)
        hBox.add(self.scrolledwindow)

        vMainBox = gtk.VBox()
        vMainBox.pack_start(self.menu_bar)
        vMainBox.pack_end(hBox)

        self.add(vMainBox)
        self.show_all()

    def create_menu(self):
        """
        Tworzy menu, podpina akcje i skróty klawiszowe
        """
        agr = gtk.AccelGroup()
        self.add_accel_group(agr)

        self.menu_bar = gtk.MenuBar()
        menu = gtk.Menu()

        clear_database_item = gtk.ImageMenuItem(gtk.STOCK_CLEAR, agr)
        key, mod = gtk.accelerator_parse("<Control>D")
        clear_database_item.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)

        about_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT, agr)
        key, mod = gtk.accelerator_parse("<Control>O")
        about_item.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)

        clear_database_item.connect("activate", self.clear_database)
        about_item.connect("activate", self.show_about)
        quit_item.connect("activate", gtk.main_quit)

        menu.append(clear_database_item)
        menu.append(gtk.SeparatorMenuItem())
        menu.append(about_item)
        menu.append(quit_item)
        menu_item = gtk.MenuItem("Program")

        menu_item.set_submenu(menu)
        self.menu_bar.append(menu_item)

    def choose_catalog(self, widget):
        """
        Zmiana katalogu, gdzie zapisujemy pobrane tapety
        """
        dialog = gtk.FileChooserDialog(
            "Otwórz..",
            None,
            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.entryCatalogPath.set_text(dialog.get_filename())
        dialog.destroy()

    def retrive_images(self, widget):
        """
        Tworzy i uruchamia wątki, które ściągają kolejne tapety
        """
        gtk.threads_enter()
        threads = []
        self.lblInfo.set_text('Pobieranie...')
        self.set_sensitive_for_all(False)
        while gtk.events_pending():
            gtk.main_iteration_do(True)
        if int(self.entryPages.get_text()) < 1:
            self.entryPages.set_text('1')
        if int(self.entryPagesEnd.get_text()) < 1:
            self.entryPagesEnd.set_text('1')
        for page in xrange(int(self.entryPages.get_text())-1, int(self.entryPagesEnd.get_text())):
            with gtk.gdk.lock:
                threads.append(threading.Thread(target=self.retrive_page, args=(page,)))
                threads[-1].start()
                self.threads_counter += 1

    def retrive_page(self, page):
        """
        Pobiera obrazki z konkretnej strony, dodaje je do bazy danych i odpala funkcję odświeżającą listę obrazków
        """
        ir = ImageRetriver(self.entryUrl.get_text(), int(self.entryPages.get_text()), 100*page, self.entryCatalogPath.get_text())
        result = ir.retrive(page)
        self.database.connect()
        for image in result:
            self.database.add_image(self.entryCatalogPath.get_text() + '/' + image)
        self.database.disconnect()
        self.threads_counter -= 1
        gobject.idle_add(self.refreshImagesTableAndShowThem)

    def refreshImagesTableAndShowThem(self):
        """
        Odświeża listę tapet i wyświetla je
        """
        self.scrolledwindow.get_child().remove(self.images_table)
        self.refreshImagesTable()
        if self.threads_counter == 0:
            self.lblInfo.set_text('')
            self.set_sensitive_for_all()
        self.refreshImagesCount()
        self.scrolledwindow.add_with_viewport(self.images_table)
        self.show_all()
        self.images_table.show()
        self.lblCountImagesInfo.show()
        if self.threads_counter == 0:
            self.refresh_all = False
            self.refreshPages()
            return False

    def refreshImagesTable(self):
        """
        Odświeża listę obrazków
        """
        limit = self.how_many_pages()
        self.database.connect()
        rows = self.database.get_images_in_range(limit-250, limit)
        self.database.disconnect()
        self.images_table = gtk.Table(len(rows)*2+1, 2, False)
        counter = 0
        if rows is not None:
            for row in rows:
                label = gtk.Label(row[1])
                hbox = gtk.HBox()
                hbox.pack_start(label, False)
                hbox.pack_start(gtk.Label())

                b = gtk.Button("Usuń", gtk.STOCK_REMOVE)
                b.set_size_request(60, 25)
                b.connect("clicked", self.remove_image, row[0])

                c = gtk.Button("Otwórz", gtk.STOCK_OPEN)
                c.set_size_request(80, 25)
                c.connect("clicked", self.open_image, row[1])

                hbox.pack_start(c, False)
                hbox.pack_start(b, False)
                vbox = gtk.VBox()
                vbox.pack_start(hbox, False)
                photo = gtk.Image()
                pixbuf = gtk.gdk.pixbuf_new_from_file(row[1])
                scaled_buf = pixbuf.scale_simple(150, 150, gtk.gdk.INTERP_BILINEAR)
                photo.set_from_pixbuf(scaled_buf)
                vbox.pack_end(photo)
                self.images_table.attach(vbox, 0, 2, counter, counter+1)
                self.images_table.attach(gtk.Label(""), 0, 2, counter+1, counter+2)
                counter += 2

    def set_sensitive_for_all(self, sensitive=True):
        """
        Ustawia parametr sensitive dla wszystkich pól,
        które należy zablokować podczas pobierania obrazków
        """
        self.btnDownload.set_sensitive(sensitive)
        self.cmbPages.set_sensitive(sensitive)
        self.btnCatalogChooser.set_sensitive(sensitive)

    def how_many_pages(self):
        """
        Zwraca limity ile należy pobrać obrazków
        """
        if self.cmbPages.get_active_text() == None:
            limit = 250
        else:
            limit = int(self.cmbPages.get_active_text())*250
        return limit

    def open_image(self, widget, filename):
        """
        Otwiera tapetę w systemowym programie graficznym
        """
        if sys.platform.startswith('linux'):
            subprocess.call(['xdg-open', filename])
        # elif sys.platform.startswith('darwin'):
            subprocess.call(['open', filename])
        elif sys.platform.startswith('win'):
            subprocess.call(['start', filename], shell=True)
        else:
            md = gtk.MessageDialog(
                self,
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                gtk.BUTTONS_CLOSE, "Twój system nie jest obsługiwany. Tylko OS X, Linux i Windows.")
            md.run()
            md.destroy()

    def remove_image(self, widget, id):
        """
        Usuwa obrazek z bazy danych i z dysku (wpierw z dysku)
        """
        self.database.connect()
        file = self.database.get_image(id)
        try:
            os.remove(file[1])
        except OSError:
            pass
        self.database.remove_image(id)
        self.database.disconnect()
        self.refreshImagesCount()
        if int(self.lblCountImages.get_text()) % 250 == 0:
            self.refreshPages()
        self.refreshImagesTableAndShowThem()

    def refreshImagesCount(self):
        """
        Odświeża licznik pobranych tapet
        """
        self.database.connect()
        self.lblCountImages.set_text(str(self.database.count_images()[0]))
        self.database.disconnect()

    def refreshPages(self):
        """
        Odświeża listę dostępnych stron
        """
        current = self.cmbPages.get_active()
        self.cmbPages.get_model().clear()
        self.cmbPages.append_text("1")
        pages = 2
        self.database.connect()
        for i in xrange(250, self.database.count_images()[0], 250):
            self.cmbPages.append_text(str(pages))
            pages += 1
        self.database.disconnect()
        if pages-1 < current:
            self.cmbPages.set_active(0)
        else:
            self.cmbPages.set_active(current)
        self.refresh_all = True

    def show_about(self, widget):
        """
        Pokazuje okienko o autorze i programie
        """
        md = gtk.MessageDialog(
            self,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
            gtk.BUTTONS_CLOSE, "ImageRetriver for 4Chan\nMarcin Bratek\nInstytut Informatyki Uniwersytetu Wrocławskiego\nSemestr zimowy 2013/2014")
        md.run()
        md.destroy()

    def clear_database(self, widget):
        """
        Czyści bazę danych i usuwa wszystkie pobrane obrazki
        """
        self.lblInfo.set_text('Usuwanie...')
        while gtk.events_pending():
            gtk.main_iteration_do(True)
        self.database.connect()
        for file in self.database.get_images():
            try:
                os.remove(file[1])
            except OSError:
                pass
        self.database.clear_database()
        self.database.disconnect()
        self.refreshImagesTableAndShowThem()
        self.refreshImagesCount()
        self.refreshPages()
        md = gtk.MessageDialog(
            self,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
            gtk.BUTTONS_CLOSE, "Wszystkie grafiki zostały usunięte!")
        md.run()
        md.destroy()
        self.lblInfo.set_text('')
        self.refreshPages()

    def change_page(self, widget):
        """
        Jeśli zmienimy wyświetlaną stronę, odświeżamy listę obrazków
        """
        if self.refresh_all == True and self.cmbPages.get_active_text() != None:
            self.lblInfo.set_text("Wczytywanie...")
            while gtk.events_pending():
                gtk.main_iteration_do(True)
            self.refreshImagesTableAndShowThem()
            self.lblInfo.set_text("")
