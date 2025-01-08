from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import (
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem
)
from ParamDialog import ParamDialog
from Commands import MoveItemCommand


class MusicItem(QGraphicsRectItem):
    def __init__(self, x, y, width, name="Clip", settings = None, track_height=40):
        width = float(width) if isinstance(width, (int, float)) else float(width[0])
        super().__init__(x, y, width, track_height)
        self.settings = settings  # Salva il riferimento alle settings
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # Abilita la selezione
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.color = QColor(100, 150, 200)  # Default color
        self.setBrush(self.color)
        self.setPen(QPen(Qt.black))
        self.track_index = 0  # inizializza
        self.name = name
        self.text = QGraphicsTextItem(self.name, self)
        self.text.setPos(5, track_height/4)
        self.drag_start = None
        self.track_index = 0  # inizializza
        self.setAcceptHoverEvents(True)  # Aggiungi questa riga
        self.is_hovered = False  # Aggiungi questa riga
        
        self.params = {
            "cAttacco": 0,
            "durataArmonica": 26,
            "ritmo": [7,15],
            "durata": 5,
            "ampiezza": [-30,-0.25],
            "frequenza": [6,1],
            "posizione": -8
        }

    def updateHeight(self, new_height):
        """
        Aggiorna l'altezza dell'item e scala il testo proporzionalmente
        Args:
            new_height: nuova altezza dell'item
        """
        current_rect = self.rect()
        self.setRect(0, 0, current_rect.width(), new_height)
        
        # Calcola la dimensione del testo proporzionale all'altezza
        base_text_size = self.settings.get('item_text_size', 12)
        height_ratio = new_height / 50  # 50 è l'altezza di default
        new_text_size = max(8, min(base_text_size * height_ratio, 24))  # Limita tra 8 e 24
        
        # Aggiorna il font del testo
        font = self.text.font()
        font.setPointSize(int(new_text_size))
        self.text.setFont(font)
        
        # Centra verticalmente il testo nel nuovo spazio
        text_height = self.text.boundingRect().height()
        vertical_center = (new_height - text_height) / 2
        self.text.setPos(5, vertical_center)
        
        # Se il testo è troppo largo, aggiungi dei puntini di sospensione
        text_width = self.text.boundingRect().width()
        available_width = current_rect.width() - 10  # 10 pixel di margine
        
        if text_width > available_width:
            original_text = self.text.toPlainText()
            # Trova la lunghezza massima del testo che si adatta
            ellipsis = "..."
            i = len(original_text)
            while i > 0 and self.text.boundingRect().width() > available_width:
                i -= 1
                self.text.setPlainText(original_text[:i] + ellipsis)  

    def updateTextStyle(self):
        if self.settings:
            font = self.text.font()
            font.setPointSize(self.settings.get('item_text_size', 12))
            self.text.setFont(font)
            self.text.setDefaultTextColor(QColor(self.settings.get('text_color', '#000000')))

    def mouseDoubleClickEvent(self, event):
        self.showParamDialog()

    def showParamDialog(self):
        dialog = ParamDialog(self.params, self.color)
        if dialog.exec_():
            for key, input_field in dialog.inputs.items():
                try:
                    if isinstance(self.params[key], list):
                        input_text = input_field.text()
                        try:
                            # Preprocessa il testo per gestire valori senza apici
                            processed_text = input_text
                            if not (input_text.startswith('[') and input_text.endswith(']')):
                                processed_text = f"[{input_text}]"
                            
                            # Aggiungi apici temporanei alle parole senza apici
                            import re
                            def add_quotes(match):
                                word = match.group(0)
                                # Non aggiungere apici se è già un numero
                                try:
                                    float(word)
                                    return word
                                except ValueError:
                                    return f"'{word}'"
                            
                            # Trova parole che contengono lettere e non sono tra apici
                            processed_text = re.sub(r'[a-zA-Z]\w*(?=[\s,\]]|$)', add_quotes, processed_text)
                            
                            # Ora fai il parsing con literal_eval
                            from ast import literal_eval
                            parsed_value = literal_eval(processed_text)
                            
                            # Convert all numbers to float in the nested structure
                            def convert_numbers(val):
                                if isinstance(val, (int, float)):
                                    return float(val)
                                elif isinstance(val, str):
                                    # Rimuovi eventuali apici dalla stringa
                                    val = val.strip('"\'')
                                    # Se la stringa contiene lettere, mantienila come stringa raw (senza apici)
                                    if any(c.isalpha() for c in val):
                                        return val  # Ritorna la stringa senza apici
                                    # Altrimenti prova a convertirla in float
                                    try:
                                        return float(val)
                                    except ValueError:
                                        return val
                                elif isinstance(val, list):
                                    return [convert_numbers(x) for x in val]
                                return val
                            
                            processed_value = convert_numbers(parsed_value)
                            self.params[key] = processed_value
                            
                        except (ValueError, SyntaxError) as e:
                            print(f"Error parsing list value for {key}: {e}")
                            continue
                    else:
                        try:
                            # Se il valore contiene almeno una lettera, mantienilo come stringa
                            text_value = input_field.text()
                            if any(c.isalpha() for c in text_value):
                                self.params[key] = text_value
                            else:
                                self.params[key] = float(text_value)
                        except ValueError as e:
                            print(f"Error parsing value for {key}: {e}")
                            continue
                        
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing parameter {key}: {e}")
                    continue
            
            self.color = dialog.color
            self.setBrush(self.color)
            
            if self.scene():
                new_x = self.params['cAttacco'] * self.scene().pixels_per_beat * self.scene().zoom_level
                # Gestione della durata come lista o valore singolo
                duration = self.params['durata']
                if isinstance(duration, list):
                    new_width = float(duration[0]) * self.scene().pixels_per_beat * self.scene().zoom_level
                else:
                    new_width = float(duration) * self.scene().pixels_per_beat * self.scene().zoom_level

                self.setPos(new_x, self.pos().y())
                self.setRect(0, 0, new_width, self.rect().height())
                self.text.setPos(5, self.rect().height()/4)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            newPos = value
            grid_size = (self.scene().pixels_per_beat * self.scene().zoom_level) / 16

            if newPos.x() < grid_size:
                grid_x = 0
            else:
                grid_x = round(newPos.x() / grid_size) * grid_size

            # Calcola la nuova traccia basata sulla posizione Y
            new_track = max(0, min(
                int(newPos.y() / self.scene().track_height),
                self.scene().num_tracks - 1
            ))
            track_y = new_track * self.scene().track_height
            self.track_index = new_track  # Aggiorna il track_index

            # Update cAttacco
            self.params['cAttacco'] = float(round(grid_x / (self.scene().pixels_per_beat * self.scene().zoom_level), 3))
            
            if self.isSelected() and not hasattr(self, '_updating_group'):
                delta_x = round(grid_x - self.pos().x(),3)
                delta_y = newPos.y() - self.pos().y()
                delta = QPointF(delta_x, delta_y)
                
                self._updating_group = True
                try:
                    for item in self.scene().selectedItems():
                        if item != self and isinstance(item, MusicItem):
                            new_item_pos = item.pos() + delta
                            new_item_track = max(0, min(
                                int(new_item_pos.y() / self.scene().track_height),
                                self.scene().num_tracks - 1
                            ))
                            new_item_y = new_item_track * self.scene().track_height

                            item.setPos(QPointF(new_item_pos.x(), new_item_y))
                            item.track_index = new_item_track
                            item.params['cAttacco'] = new_item_pos.x() / (self.scene().pixels_per_beat * self.scene().zoom_level)
                finally:
                    delattr(self, '_updating_group')
            
            return QPointF(grid_x, track_y)
            
        return super().itemChange(change, value)


    def mouseMoveEvent(self, event):
        if not self.drag_start:
            return
            
        # Calcola il delta rispetto all'ultimo movimento
        delta = event.scenePos() - self.drag_start
        grid_size = (self.scene().pixels_per_beat * self.scene().zoom_level) / 16
        
        if not self.isSelected():
            return
            
        selected_items = [item for item in self.scene().selectedItems() if isinstance(item, MusicItem)]
        
        # Calcola la posizione più a sinistra tra tutti gli item selezionati dopo il movimento
        leftmost_position = float('inf')
        for item in selected_items:
            proposed_x = item.pos().x() + delta.x()
            if proposed_x < grid_size:
                proposed_x = 0
            else:
                proposed_x = round(proposed_x / grid_size) * grid_size
            leftmost_position = min(leftmost_position, proposed_x)
        
        # Se la posizione più a sinistra è <= 0, permetti solo movimento verticale
        if leftmost_position <= 0:
            for item in selected_items:
                current_y = item.pos().y()
                new_track = max(0, min(
                    int((current_y + delta.y()) / self.scene().track_height),
                    self.scene().num_tracks - 1
                ))
                new_y = new_track * self.scene().track_height
                item.setPos(item.pos().x(), new_y)
        else:
            # Movimento normale in entrambe le direzioni
            for item in selected_items:
                current_x = item.pos().x()
                current_y = item.pos().y()
                
                # Calcola nuova posizione x con snap alla griglia
                proposed_x = current_x + delta.x()
                if proposed_x < grid_size:
                    new_x = 0
                else:
                    new_x = round(proposed_x / grid_size) * grid_size
                
                # Calcola la nuova traccia
                new_track = max(0, min(
                    int((current_y + delta.y()) / self.scene().track_height),
                    self.scene().num_tracks - 1
                ))
                new_y = new_track * self.scene().track_height
                
                # Applica la nuova posizione
                item.setPos(new_x, new_y)
                item.params['cAttacco'] = round(new_x / (self.scene().pixels_per_beat * self.scene().zoom_level), 3)
        
        # Aggiorna il punto di riferimento per il prossimo movimento
        self.drag_start = event.scenePos()

    def mousePressEvent(self, event):
        if event.modifiers() & Qt.MetaModifier:  # Command/Meta key
            self.showParamDialog()
            return 
        self.drag_start = event.scenePos()
        self.initial_pos = self.pos()  # Salva la posizione iniziale
        
        if not event.modifiers() & Qt.ControlModifier:
            if not self.isSelected():
                scene = self.scene()
                if scene:
                    for item in scene.selectedItems():
                        item.setSelected(False)
            self.setSelected(True)
            
        # Salva la posizione iniziale per tutti gli item selezionati
        if self.scene():
            for item in self.scene().selectedItems():
                if isinstance(item, MusicItem):
                    item.initial_drag_pos = item.pos()
        
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Rimuovi le posizioni iniziali salvate
        if self.scene():
            for item in self.scene().selectedItems():
                if isinstance(item, MusicItem) and hasattr(item, 'initial_drag_pos'):
                    delattr(item, 'initial_drag_pos')
                    
        if hasattr(self, 'initial_pos') and self.pos() != self.initial_pos:
            # Trova la MainWindow per accedere al command_manager
            main_window = None
            view = self.scene().views()[0]
            if view:
                main_window = view.window()
            
            if main_window and hasattr(main_window, 'command_manager'):
                command = MoveItemCommand(self, self.initial_pos, self.pos())
                main_window.command_manager.execute(command)
                main_window.update_undo_redo_actions()

        self.drag_start = None
        super().mouseReleaseEvent(event)
    
    def hoverEnterEvent(self, event):
        """Chiamato quando il mouse entra nell'item"""
        self.is_hovered = True
        self.update()  # Forza il ridisegno
        super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        """Chiamato quando il mouse esce dall'item"""
        self.is_hovered = False
        self.update()  # Forza il ridisegno
        super().hoverLeaveEvent(event)
        
    def paint(self, painter, option, widget):
        # Salva il colore originale
        original_brush = self.brush()
        
        if self.isSelected():
            # Se selezionato, molto più chiaro (70% più luminoso)
            lighter_color = self.color.lighter(140)
            self.setBrush(lighter_color)
        elif self.is_hovered:
            # Se hover, leggermente più chiaro (20% più luminoso)
            lighter_color = self.color.lighter(110)
            self.setBrush(lighter_color)
            
        # Disegna l'item
        super().paint(painter, option, widget)
        
        # Ripristina il colore originale
        self.setBrush(original_brush)
        
        if hasattr(self, 'highlighted') and self.highlighted:
            # Disegna l'evidenziazione della ricerca
            pen = QPen(QColor(255, 165, 0), 3)
            painter.setPen(pen)
            painter.drawRect(self.rect())
        elif self.isSelected():
            # Disegna il bordo di selezione
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.rect())