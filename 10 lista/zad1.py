#encoding: utf-8
import gobject
import gtk
import datetime
import database
import xmlrpclib

class PyApp(gtk.Window):
    
    timeout = {}

    def __init__(self):
        super(PyApp, self).__init__()

        self.set_title("Terminarz")
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        self.resize(900, 600)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#DBDBDB'))

        self.database = database.Database()
        self.database.connect()
        self.database.prepare_database()

        self.server = xmlrpclib.Server("http://localhost:8002", allow_none=True)
        try:
            self.server.ping()
        except Exception as ex:
            print "Nie udało się nawiązać połączenia z serwerem: " + str(ex)
            raise SystemExit


        #self.sound = sound.Audio()
        #self.sound.playSound()

        lblAddAppointment = gtk.Label()
        lblAddAppointment.set_padding(0, 10)
        lblAddAppointment.set_justify(gtk.JUSTIFY_CENTER)
        lblAddAppointment.set_markup("<span size='15000'><b>Dodaj wpis</b></span>")


        lblName = gtk.Label("Tytuł")
        self.entryName = gtk.Entry()

        lblText = gtk.Label("Tekst")
        self.entryText = gtk.TextView()
        self.text = gtk.TextBuffer()
        self.entryText.set_buffer(self.text)
        self.entryText.set_editable(True)

        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolledwindow.add(self.entryText)

        now = datetime.datetime.now()

        lblStartDate = gtk.Label("Data startowa")
        self.entryStartDate = gtk.Entry()
        self.entryStartDate.set_text(now.strftime("%Y-%m-%d %H:%M"))

        now = now + datetime.timedelta(hours=1)

        self.lblEndDate = gtk.Label("Data końcowa")
        self.entryEndDate = gtk.Entry()
        self.entryEndDate.set_text(now.strftime("%Y-%m-%d %H:%M"))

        self.checkboxType = gtk.CheckButton("Sprawa")
        self.checkboxType.connect("clicked", self.checked_type, self.lblEndDate, self.entryEndDate)

        button = gtk.Button("Dodaj", gtk.STOCK_ADD)
        button.connect("clicked", self.add_appointment)
        button.set_size_request(80, 25)

        button2 = gtk.Button("Odśwież", gtk.STOCK_REFRESH)
        button2.connect("clicked", self.refresh_appointments_and_show_them)
        button.set_size_request(80, 25)
        
        table = gtk.Table(6, 2, False)

        table.attach(lblAddAppointment, 0, 2, 0 , 1)

        table.attach(lblName, 0, 1, 1, 2)
        table.attach(self.entryName, 1, 2, 1, 2)

        table.attach(lblText, 0, 1, 2, 3)
        entryTextBox = gtk.HBox()
        entryTextBox.pack_start(scrolledwindow) 
        entryTextBox.set_size_request(70, 100)
        table.attach(entryTextBox, 1, 2, 2, 3)

        table.attach(self.checkboxType, 1, 2, 3, 4)

        table.attach(lblStartDate, 0, 1, 4, 5)
        table.attach(self.entryStartDate, 1, 2, 4, 5)

        table.attach(self.lblEndDate, 0, 1, 5, 6)
        table.attach(self.entryEndDate, 1, 2, 5, 6)

        lblSearch = gtk.Label()
        lblSearch.set_padding(0, 10)
        lblSearch.set_justify(gtk.JUSTIFY_CENTER)
        lblSearch.set_markup("<span size='15000'><b>Przeszukaj</b></span>")

        self.entrySearch = gtk.Entry()
        self.entrySearch.connect('key-press-event', self.pressedEnterToSearch)
        self.buttonSearch = gtk.Button("Szukaj…", gtk.STOCK_FIND)
        self.buttonSearch.connect("clicked", self.search_appointments)

        searchBox = gtk.VBox()
        searchBox.pack_start(lblSearch)
        searchBox.pack_start(self.entrySearch)
        searchBox.pack_start(self.buttonSearch)
        searchBox.pack_end(gtk.Label("\n"), True)

        smallHBox = gtk.HBox(False)
        smallHBox.pack_end(button, False)
        smallHBox.pack_end(button2, False)

        vBox = gtk.VBox()
        vBox.pack_start(table, False)
        vBox.pack_start(smallHBox, False)
        vBox.pack_end(searchBox, False)

        self.refresh_appointments()
        self.scrolledwindow = gtk.ScrolledWindow()
        self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolledwindow.add_with_viewport(self.table2)
        self.scrolledwindow.get_child().modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFFFFF'))
        

        hBox = gtk.HBox()
        hBox.pack_start(vBox, False)
        hBox.add(self.scrolledwindow)
        

        self.add(hBox)
        self.show_all()

    def add_appointment(self, widget):
        if self.checkboxType.get_active():
            type = 1
        else:
            type = 0
        self.server.add_appointment([unicode(self.entryName.get_text()), unicode(self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter())), type, self.entryStartDate.get_text(), self.entryEndDate.get_text()])
        app_id = self.server.get_last_appointment()
        self.refresh_appointments_and_show_them(None)      
        if type == 1:
            time = datetime.datetime.strptime(self.entryStartDate.get_text(), "%Y-%m-%d %H:%M")
        else:
            time = datetime.datetime.strptime(self.entryEndDate.get_text(), "%Y-%m-%d %H:%M")
        self.timeout[app_id[0]] = gobject.timeout_add_seconds(4, self.show_reminder, self.entryName.get_text(), self.text.get_text(self.text.get_start_iter(), self.text.get_end_iter()), time)    

    
    def show_reminder(self, name, content, end_date):
        if end_date.date() <= datetime.datetime.now().date():
            if end_date.time() < datetime.datetime.now().time():
                dia = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, 'Przypomnienie o ' + name)
                dia.format_secondary_text(content)
                dia.run()
                dia.destroy()
                return False
        return True


    def refresh_appointments_and_show_them(self, widget, search = False):
        self.scrolledwindow.get_child().remove(self.table2)
        self.refresh_appointments(search)
        self.scrolledwindow.add_with_viewport(self.table2)
        self.show_all()
        self.checked_type(self.checkboxType, self.lblEndDate, self.entryEndDate)
        self.table2.show()

    def refresh_appointments(self, search = False):
        rows = self.server.get_appointments(search)
        self.table2 = gtk.Table(len(rows)*2+1, 2, False)
        counter = 0
        for row in rows:
            label = gtk.Label()
            label.set_alignment(0, 0)
            label.set_padding(5, 10)
            label.set_markup("<span size='15000'><b>" + row[1] + "</b></span>")
            textbox = gtk.TextView()
            text = gtk.TextBuffer()
            text.set_text(row[2])
            textbox.set_buffer(text)
            textbox.set_editable(False)
            textbox.set_wrap_mode(gtk.WRAP_WORD)
            hbox = gtk.HBox()
            hbox.pack_start(label, False)
            hbox.pack_start(gtk.Label())
            # Edit button
            b = gtk.Button("Zmień", gtk.STOCK_EDIT)
            b.set_size_request(80, 20)
            b.connect("clicked", self.edit_appointment, row[0])
            hbox.pack_start(b, False)
            # Remove button
            b = gtk.Button("Usuń", gtk.STOCK_REMOVE)
            b.set_size_request(60, 20)
            b.connect("clicked", self.remove_appointment, row[0])


            # Layout for appointments list
            hbox.pack_start(b, False)
            vbox = gtk.VBox()
            vbox.pack_start(hbox, False)
            if row[3] == 1:
                l = gtk.Label(row[4][:-3])
            else:
                l = gtk.Label(row[4][:-3] + " do " + row[5][:-3])
            l.set_alignment(0, 0)
            l.set_padding(0, 10)
            vbox.pack_start(l, False)
            vbox.pack_start(textbox, False)
            self.table2.attach(vbox, 0, 2, counter, counter+1)
            self.table2.attach(gtk.Label(""), 0, 2, counter+1, counter+2)
            counter += 2

            self.removeTimeout(row[0])
            time = datetime.datetime.strptime(row[4][:-3], "%Y-%m-%d %H:%M")
            if time.date() >= datetime.datetime.now().date():
                if time.time() > datetime.datetime.now().time():
                    self.timeout[id] = gobject.timeout_add_seconds(4, self.show_reminder, row[1], row[2], time)    



    def remove_appointment(self, widget, id):
        self.server.remove_appointment(id)
        self.removeTimeout(id)
        self.refresh_appointments_and_show_them(None)
    
    def edit_appointment(self, widget, id):
        
        appointment = self.server.get_appointment(id)

        dia = gtk.Dialog('Zmień ' + appointment[1], self,  gtk.DIALOG_MODAL  | gtk.DIALOG_DESTROY_WITH_PARENT)
        dia.set_size_request(500, 300)
        lblName = gtk.Label("Tytuł")
        entryName = gtk.Entry()
        entryName.set_text(appointment[1])

        lblText = gtk.Label("Tekst")
        entryText = gtk.TextView()
        text = gtk.TextBuffer()
        text.set_text(appointment[2])
        entryText.set_buffer(text)
        entryText.set_editable(True)

        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolledwindow.add(entryText)

        now = datetime.datetime.now()

        lblStartDate = gtk.Label("Data startowa")
        entryStartDate = gtk.Entry()
        entryStartDate.set_text(appointment[4][:-3])

        now = now + datetime.timedelta(hours=1)

        lblEndDate = gtk.Label("Data końcowa")
        entryEndDate = gtk.Entry()
        entryEndDate.set_text(appointment[5][:-3])

        checkboxType = gtk.CheckButton("Sprawa")
        if appointment[3] == 1:
            checkboxType.set_active(True)
        else:
            checkboxType.set_active(False)
        checkboxType.connect("clicked", self.checked_type, lblEndDate, entryEndDate)

        table = gtk.Table(5, 2, False)

        table.attach(lblName, 0, 1, 0, 1)
        table.attach(entryName, 1, 2, 0, 1)

        table.attach(lblText, 0, 1, 1, 2)
        table.attach(scrolledwindow, 1, 2, 1, 2)

        table.attach(checkboxType, 1, 2, 2, 3)

        table.attach(lblStartDate, 0, 1, 3, 4)
        table.attach(entryStartDate, 1, 2, 3, 4)

        table.attach(lblEndDate, 0, 1, 4, 5)
        table.attach(entryEndDate, 1, 2, 4, 5)

        dia.vbox.pack_start(table)
        dia.show_all()
        if checkboxType.get_active():
            lblEndDate.hide()
            entryEndDate.hide()

        dia.add_button(gtk.STOCK_SAVE, 1)
        dia.add_button(gtk.STOCK_CANCEL, 0)

        result = dia.run()
        if result == 1:
            with self.database.con:
                if checkboxType.get_active():
                    type = 1
                else:
                    type = 0
                self.server.update_appointment([unicode(entryName.get_text()), unicode(text.get_text(text.get_start_iter(), text.get_end_iter())), type, entryStartDate.get_text(), entryEndDate.get_text(), id])
                
                self.removeTimeout(id)
                if type == 1:
                    time = datetime.datetime.strptime(entryStartDate.get_text(), "%Y-%m-%d %H:%M")
                else:
                    time = datetime.datetime.strptime(entryEndDate.get_text(), "%Y-%m-%d %H:%M")
                self.timeout[id] = gobject.timeout_add_seconds(4, self.show_reminder, entryName.get_text(), text.get_text(text.get_start_iter(), text.get_end_iter()), time)    
                self.refresh_appointments_and_show_them(widget)
        dia.destroy()

    def checked_type(self, widget, label, field):
        if widget.get_active():
            label.hide()
            field.hide()
        else:
            label.show()
            field.show()

    def search_appointments(self, widget):
        search = 'SELECT * FROM appointments WHERE name LIKE "%' + self.entrySearch.get_text() + '%" OR content LIKE "%' + self.entrySearch.get_text() + '%"'
        self.refresh_appointments_and_show_them(widget, search)

    def pressedEnterToSearch(self, widget, event):
        if event.keyval == 65293:
            self.search_appointments(self.entrySearch)

    def removeTimeout(self, id):
        try:
            gobject.source_remove(self.timeout[id])
            del self.timeout[id]
        except:
            pass



PyApp()
gtk.main()