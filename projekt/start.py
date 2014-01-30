#!/usr/bin/env python
import gobject
import gtk
from image_retriver_app import ImageRetriverApp

ImageRetriverApp()
gobject.threads_init()
gtk.threads_enter()
gtk.main()
gtk.threads_leave()
