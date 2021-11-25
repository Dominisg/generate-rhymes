#!/usr/bin/env python3

from asciimatics.widgets import Frame, Layout, Divider, Text, \
    Button, TextBox, Widget, RadioButtons
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys

from rhymes import get_dictionary, rhymes

class RhymesView(Frame):
    def __init__(self, screen, dicts):
        super(RhymesView, self).__init__(screen,
                                          screen.height - 10,
                                          screen.width - 10,
                                          hover_focus=True,
                                          can_scroll=True,
                                          title="Find rhymes!",
                                          reduce_cpu=True)

        # Create the form for displaying the list of contacts.
        self.dicts = dicts
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Find rhyme to:", "search"))
        layout.add_widget(RadioButtons([('polish','pl'), ('english', 'en')], label="Language:", name='language'))
        layout.add_widget(RadioButtons([('1', 1),('2', 2),('3', 3)], label="Rhyme level:", name='level'))
        
        layout.add_widget(Divider())
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "", name="result", as_string=True, line_wrap=True, readonly=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Search", self._ok), 0)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(RhymesView, self).reset()
        self.data = {"search": "", "result": "", 'language': 'pl', 'level': '1'}

    def _ok(self):
        self.save()
        result = rhymes(self.dicts[self.data['language']], self.data['search'], int(self.data['level']), self.data['language'])
        self.data['result'] = ' '.join(result)
        self.data = self.data.copy()
        super(RhymesView, self).reset()


    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


def demo(screen, scene):
    dicts = {
        'en':get_dictionary('en'),
        'pl':get_dictionary('pl')
    }

    scenes = [
        Scene([RhymesView(screen, dicts)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene], unicode_aware=True)
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
