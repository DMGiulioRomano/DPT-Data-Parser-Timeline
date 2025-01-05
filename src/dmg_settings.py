# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path

# Nome del file .dmg da creare
format = 'UDZO'
size = '1g'

# Definisci il nome dell'app
application = 'dist/DPT.app'

# Nome del volume che apparirà una volta montato il DMG
volume_name = 'Delta Parser Timeline'

# Posizione delle icone nel DMG
icon_locations = {
    'DPT.app': (140, 120),
    'Applications': (500, 120)
}

# Dimensione della finestra
window_rect = ((100, 100), (640, 280))

# Background
background = 'builtin-arrow'

# Simbolico link ad Applications
symlinks = {'Applications': '/Applications'}

# Icone da includere
files = [application]

# Opzioni di visualizzazione del Finder
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False

# Impostazioni di visualizzazione
arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
show_icon_preview = False
show_item_info = False
label_pos = 'bottom'
icon_size = 128