from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, 
    QPushButton, QColorDialog
)

class ParamDialog(QDialog):
    def __init__(self, params, color=None, item=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Parameters")
        self.params = params  # Salviamo riferimento ai parametri originali
        self.color = color or QColor(100, 150, 200)
        self.item = item        
        # Setup layout
        layout = QFormLayout()
        self.inputs = {}
        
        # Crea input fields per ogni parametro
        for key, value in params.items():
            if isinstance(value, list):
                # Per le liste, formatta ogni elemento
                formatted_list = []
                for item in value:
                    if isinstance(item, str):
                        # Se è una stringa, non aggiungere apici
                        formatted_list.append(str(item))
                    else:
                        formatted_list.append(str(item))
                # Unisci gli elementi con virgole e metti tra parentesi quadre
                self.inputs[key] = QLineEdit('[' + ', '.join(formatted_list) + ']')
            else:
                self.inputs[key] = QLineEdit(str(value))
            layout.addRow(key, self.inputs[key])

        # Add color button
        self.colorButton = QPushButton("Choose Color")
        self.colorButton.clicked.connect(self.chooseColor)
        layout.addRow("Color", self.colorButton)
        self.updateColorButton()

        # Add dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)

    def chooseColor(self):
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.updateColorButton()
    
    def updateColorButton(self):
        """Aggiorna l'aspetto del pulsante colore"""
        self.colorButton.setStyleSheet(
            f"background-color: {self.color.name()}; "
            f"color: {'black' if self.color.lightness() > 128 else 'white'}"
        )

    def keyPressEvent(self, event):
        """Gestisce gli eventi da tastiera"""
        if (event.modifiers() & (Qt.ControlModifier | Qt.MetaModifier)) and event.key() == Qt.Key_W:
            self.reject()
        else:
            super().keyPressEvent(event)

    def accept(self):
        """Gestisce l'accettazione del dialog e l'aggiornamento dei parametri"""
        # Aggiorna i parametri originali con i nuovi valori
        for key, input_field in self.inputs.items():
            try:
                if isinstance(self.params[key], list):
                    input_text = input_field.text()
                    try:
                        # Preprocessa il testo per gestire valori senza apici
                        processed_text = input_text
                        if not (input_text.startswith('[') and input_text.endswith(']')):
                            processed_text = f"[{input_text}]"
                        
                        # Parsing con literal_eval
                        from ast import literal_eval
                        parsed_value = literal_eval(processed_text)
                        
                        # Converti numeri mantenendo il tipo corretto
                        def convert_numbers(val):
                            if isinstance(val, (int, float)):
                                return type(val)(val)  # mantiene il tipo originale
                            elif isinstance(val, str):
                                val = val.strip('"\'')
                                if any(c.isalpha() for c in val):
                                    return val
                                try:
                                    # Prova prima come int, poi come float
                                    try:
                                        return int(val)
                                    except ValueError:
                                        return float(val)
                                except ValueError:
                                    return val
                            elif isinstance(val, list):
                                return [convert_numbers(x) for x in val]
                            return val
                        
                        self.params[key] = convert_numbers(parsed_value)
                        
                    except (ValueError, SyntaxError) as e:
                        print(f"Error parsing list value for {key}: {e}")
                        continue
                else:
                    try:
                        text_value = input_field.text()
                        if isinstance(self.params[key], (int, float)):
                            try:
                                # Converti sempre prima in float per evitare perdita di precisione
                                float_value = float(text_value)
                                # Se il valore originale era int e il nuovo valore è un intero esatto,
                                # mantieni int, altrimenti usa float
                                if isinstance(self.params[key], int) and float_value.is_integer():
                                    self.params[key] = int(float_value)
                                else:
                                    self.params[key] = float_value
                            except ValueError:
                                print(f"Invalid numeric input for {key}: {text_value}")
                                continue
                        else:
                            # Per parametri non numerici
                            if any(c.isalpha() for c in text_value):
                                self.params[key] = text_value
                            else:
                                try:
                                    # Prova prima come int, poi come float se necessario
                                    try:
                                        self.params[key] = int(text_value)
                                    except ValueError:
                                        self.params[key] = float(text_value)
                                except ValueError:
                                    continue
                    except ValueError as e:
                        print(f"Error parsing value for {key}: {e}")
                        continue
                        
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing parameter {key}: {e}")
                continue
        # Aggiorna anche la posizione fisica dell'item nella timeline se il parametro cAttacco è stato modificato
        if hasattr(self, 'item') and 'cAttacco' in self.params:
            new_x = float(self.params['cAttacco']) * self.item.scene().pixels_per_beat * self.item.scene().zoom_level
            self.item.setPos(new_x, self.item.pos().y())
        

        super().accept()