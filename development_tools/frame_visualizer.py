# This module is responsible for drawing a game frame by frame.
# TODO: Add scrolling of a single frame and some more useful functions.
import tkinter as tk
from PIL import Image, ImageTk
import imghdr
import config
from io import BytesIO


class _NamedTempFile:
    ''' Represents a named file in memory '''
    closed = closefd = False
    mode = 'rb'
    pos = 0

    def __init__(self, bytes, name):
        self.bytes = BytesIO(bytes).getvalue()
        self.name = name

    def readall(self):
        self.pos = len(self.bytes)
        return self.bytes

    def read(self, i=None):
        if i is None:
            i = len(self.bytes)
        self.pos += i
        return self.bytes[self.pos - i:self.pos]

    def readable(self):
        return self.pos < len(self.bytes)

    def writable(self):
        return False

    def close(self):
        self.closed = True

    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        self.pos = offset

    def tell(self):
        return self.pos


def _bytes2image(bytes):
    ''' Converts a file-like byte stream (not raw image data!)
    into a ``PIL.Image.Image`` object (from Python Imaging Library).
        ``bytes`` - a byte stream to receive image data from. '''

    header = imghdr.what(None, h=bytes)
    if header:
        temp_file = _NamedTempFile(bytes, 'frame.' + header)
        return Image.open(temp_file)
    else:
        raise Exception('''Unknown image format!
I can only read bytestreams with file-like headers of such formats:
jpeg, png, gif, tiff, SGI rgb, pbm, pgm, ppm, rast, xbm and bmp.''')


def _resize(image):
    ''' Resizes image to fit in 800x600 area. '''
    ratio = min(800 / image.size[0], 600 / image.size[1])
    return image.resize((int(image.size[0] * ratio), int(image.size[1] * ratio)),
                        Image.ANTIALIAS)


class FrameVisualizer(tk.Frame):
    ''' This class represents a ``FrameVisualizer`` - a GUI,
    which allows to view frames of an already played game. '''

    class _ControlPanel(tk.Frame):
        ''' This class represents a panel, placed in the bottom
        of the window, which is responsible for scrolling between
        frames and displaying the name of current name '''
        def __init__(self, master=None):
            ''' ``master`` - widget, owner of the current one '''
            tk.Frame.__init__(self, master, width=300)
            self.back_button = tk.Button(
                master=self, text='back', command=master._back)
            self.back_button.pack(anchor='w', side='left')
            self.forward_button = tk.Button(
                master=self, text='forward', command=master._forward)
            self.forward_button.pack(anchor='e', side='right')
            self.num_label = tk.Label(self, width=50)
            self.num_label.pack(anchor='center')

        def _set_frame_number(self, frame_number):
            ''' Assigns a new frame number to the label,
            which shows current frame number. It uses numeration from zero
            and adds one to the argument before putting it to the label.
                ``frame_number`` - a number of new frame, starting from 0 '''
            self.num_label['text'] = 'Frame #' + str(frame_number + 1)

    def __init__(self, game_controller):
        ''' ``game_controller`` - an object, which has a ``jury_states`` field,
        that is either a list or a tuple of ``JuryState`` objects, that are
        going to be passed to the painter in order to draw frames'''
        tk.Frame.__init__(self, tk.Tk())
        self.game_controller = game_controller
        self.painter_factory = config.Painter
        self.frame_number = 0
        self.control_panel = self._ControlPanel(master=self)
        self.control_panel.pack(side='bottom')
        self.frame_label = tk.Button(
            self, borderwidth=0, command=self._forward)
        self.frame_label.pack(side='top')

    def _back(self):
        ''' Switches to the previous frame if there is one. '''
        if self.frame_number > 0:
            self._draw_frame(self.frame_number - 1)

    def _forward(self):
        ''' Switches to the next frame if there is one. '''
        if self.frame_number < len(self.game_controller.jury_states) - 1:
            self._draw_frame(self.frame_number + 1)

    def _draw_frame(self, new_frame_number):
        ''' Paints a frame, corresponding with ``JuryState``,
        that has the given number.
            ``new_frame_number`` - number of a ``JuryState`` in the
            ``game_controller.jury_states`` enumeration of ``JuryState``
        to be used to draw the image.'''
        self.frame_number = new_frame_number
        self.img = ImageTk.PhotoImage(image=_resize(_bytes2image(
            self.painter_factory(self.game_controller.get_players()).paint(
                self.game_controller.jury_states[self.frame_number]))))
        self.frame_label['image'] = self.img
        self.control_panel._set_frame_number(self.frame_number)

    def mainloop(self):
        ''' Inherited from ``tkinter.Frame``.
        This method is used to show the window. '''
        self.pack()
        self._draw_frame(0)
        tk.Frame.mainloop(self)
