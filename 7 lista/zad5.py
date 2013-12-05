import gtk
import math
import compiler
import datetime

class PyApp(gtk.Window):

    x0 = -1.0
    x1 = 1.0
    y0 = -1.0
    y1 = 1.0
    maxIt = 50 # max iterations allowed
    ds = 0.002e-1# step size for numerical derivative
    eps = 5e-19 # max error allowed
    c0 = -0.73
    c1 = 0.19

    imgx = 600
    imgy = 600

    def __init__(self):
        super(PyApp, self).__init__()

        self.set_title("Fraktale")
        #self.resize(400, 400)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)

        x0Label = gtk.Label("x0")
        self.x0Entry = gtk.Entry()
        self.x0Entry.set_text(str(self.x0))
        x1Label = gtk.Label("x1")
        self.x1Entry = gtk.Entry()
        self.x1Entry.set_text(str(self.x1))
        y0Label = gtk.Label("y0")
        self.y0Entry = gtk.Entry()
        self.y0Entry.set_text(str(self.y0))
        y1Label = gtk.Label("y1")
        self.y1Entry = gtk.Entry()
        self.y1Entry.set_text(str(self.y1))
        maxItLabel = gtk.Label("Max iterations")
        self.maxItEntry = gtk.Entry()
        self.maxItEntry.set_text(str(self.maxIt))
        dsLabel = gtk.Label("Numerical derivative")
        self.dsEntry = gtk.Entry()
        self.dsEntry.set_text(str(self.ds))
        epsLabel = gtk.Label("Max error")
        self.epsEntry = gtk.Entry()
        self.epsEntry.set_text(str(self.eps))
        c0Label = gtk.Label("c0 (Julia)")
        self.c0Entry = gtk.Entry()
        self.c0Entry.set_text(str(self.c0))
        c1Label = gtk.Label("c1 (Julia")
        self.c1Entry = gtk.Entry()
        self.c1Entry.set_text(str(self.c1))

        darea = gtk.DrawingArea()
        darea.set_size_request(self.imgx, self.imgy)

        self.generowanie = gtk.Label()

        button = gtk.Button("Generuj")
        button.connect("clicked", self.draw_again, darea)

        self.functionEntry = gtk.combo_box_entry_new_text()
        self.functionEntry.append_text('Julia')
        self.functionEntry.append_text('z*z**3 - 0.23')
        self.functionEntry.append_text('z**3 - 1.0')
        self.functionEntry.append_text('z**5 - 1')
        self.functionEntry.append_text('z**8 - 1')
        self.functionEntry.append_text('4*z**3-15*z**2+17*z-6')
        self.functionEntry.append_text('-12*z**4+4*z**3-15*z**2+17*z-6')
        self.functionEntry.set_active(0)

        table = gtk.Table(10, 2, True)

        table.attach(x0Label, 0, 1, 0, 1)
        table.attach(self.x0Entry, 1, 2, 0, 1)

        table.attach(x1Label, 0, 1, 1, 2)
        table.attach(self.x1Entry, 1, 2, 1, 2)

        table.attach(y0Label, 0, 1, 2, 3)
        table.attach(self.y0Entry, 1, 2, 2, 3)

        table.attach(y1Label, 0, 1, 3, 4)
        table.attach(self.y1Entry, 1, 2, 3, 4)

        table.attach(maxItLabel, 0, 1, 4, 5)
        table.attach(self.maxItEntry, 1, 2, 4, 5)

        table.attach(dsLabel, 0, 1, 5, 6)
        table.attach(self.dsEntry, 1, 2, 5, 6)

        table.attach(epsLabel, 0, 1, 6, 7)
        table.attach(self.epsEntry, 1, 2, 6, 7)

        table.attach(c0Label, 0, 1, 7, 8)
        table.attach(self.c0Entry, 1, 2, 7, 8)

        table.attach(c1Label, 0, 1, 8, 9)
        table.attach(self.c1Entry, 1, 2, 8, 9)

        table.attach(self.generowanie, 0, 1, 9, 10)
        table.attach(button, 1, 2, 9, 10)

        hBox = gtk.HBox()
        hBox.add(table)
        hBox.add(darea)

        vBox = gtk.VBox()
        vBox.add(self.functionEntry)
        vBox.add(hBox)
        self.add(vBox)
        self.show_all()

    def draw_again(self, button, darea):
        self.start = datetime.datetime.now()

        self.generowanie.set_text("Generuje...")
        while gtk.events_pending():
            gtk.main_iteration_do(True)
        self.x0 = float(self.x0Entry.get_text())
        self.x1 = float(self.x1Entry.get_text())
        self.y0 = float(self.y0Entry.get_text())
        self.y1 = float(self.y1Entry.get_text())
        self.maxIt = int(self.maxItEntry.get_text())
        self.ds = float(self.dsEntry.get_text())
        self.eps = float(self.epsEntry.get_text())
        self.c0 = float(self.c0Entry.get_text())
        self.c1 = float(self.c1Entry.get_text())
        if self.functionEntry.get_active_text() == 'Julia':
            self.func = 'Julia'
        else:
            self.func = compiler.compile(self.functionEntry.get_active_text(), '<string>', 'eval') # Wtedy eval dziala szybciej :)
        darea.connect("expose-event", self.expose)
        darea.queue_draw()
    
    def julia(self, cr):
        c = complex(self.c0, self.c1)
        for y in xrange(self.imgy):
            zy = y * (self.y1 - self.y0) / (self.imgy - 1)  + self.y0
            for x in xrange(self.imgx):
                zx = x * (self.x1 - self.x0) / (self.imgx - 1)  + self.x0
                z = zx + zy * 1j
                for i in xrange(self.maxIt):
                    if abs(z) > 2.0:
                        break 
                    z = z * z + c
                self.draw_point(cr, x, y, i)
    
    def newton_raphston(self, cr, ds):
        def f(z):
            return eval(self.func)
        for y in xrange(self.imgy):
            zy = y * (self.y1 - self.y0) / (self.imgy - 1) + self.y0
            for x in xrange(self.imgx):
                zx = x * (self.x1 - self.x0) / (self.imgx - 1) + self.x0
                z = complex(zx, zy)
                for i in xrange(self.maxIt):
                    #calculates derivative
                    dz = (f(z + ds) - f(z)) / ds
                    if dz == 0:
                        break
                    z0 = z - f(z) / dz # Newton iteration
                    if abs(z0 - z) < self.eps: # stop when close enough to any root
                        break
                    z = z0
                self.draw_point(cr, x, y, i)
                
    
    def draw_point(self, cr, x, y, i):
        cr.save()
        cr.rectangle(x, y, 1, 1)
        cr.restore()
        cr.set_source_rgb(i % 8 * 16 / 255.0, i % 4 * 32 / 255.0, i % 2 * 64 / 255.0)
        cr.fill()
    
    def expose(self, widget, event):

        cr = widget.window.cairo_create()
        ds = complex(self.ds, self.ds)

        if self.func == 'Julia':
            self.julia(cr)
        else:
            self.newton_raphston(cr, ds)
        self.generowanie.set_text(str(datetime.datetime.now() - self.start))
        

PyApp()
gtk.main()