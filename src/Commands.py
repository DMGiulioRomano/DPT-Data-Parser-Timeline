from abc import ABC, abstractmethod
from typing import List, Dict, Any
from PyQt5.QtCore import QPointF

class Command(ABC):
    """Base abstract class for all commands"""
    @abstractmethod
    def execute(self):
        """Execute the command"""
        pass
        
    @abstractmethod
    def undo(self):
        """Undo the command"""
        pass
        
    def __str__(self):
        """String representation of the command"""
        return f"{self.__class__.__name__}"



class CommandManager:
    """Manages the undo/redo stack for all commands"""
    def __init__(self):
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        self._max_stack_size = 50  # Limita la dimensione dello stack per gestire la memoria

    def execute(self, command: Command):
        """Execute a new command and add it to the undo stack"""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()  # Svuota lo stack di redo quando viene eseguito un nuovo comando
        
        # Mantiene la dimensione dello stack sotto controllo
        if len(self._undo_stack) > self._max_stack_size:
            self._undo_stack.pop(0)

        # Notifica il cambio di stato dopo l'esecuzione
        self._notify_state_change()

    def undo(self):
        """Undo the last command"""
        if not self._undo_stack:
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        self._notify_state_change()
                
    def redo(self):
        """Redo the last undone command"""
        if not self._redo_stack:
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        self._notify_state_change()

    def clear(self):
        """Clear both undo and redo stacks"""
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._notify_state_change()
        
    def _notify_state_change(self):
        """Notify any listeners about state changes"""
        # Find the main window to update UI state
        for item in self._undo_stack + self._redo_stack:
            if hasattr(item, 'item') and hasattr(item.item, 'scene'):
                scene = item.item.scene()
                if scene and scene.views():
                    view = scene.views()[0]
                    if view and view.window():
                        main_window = view.window()
                        if hasattr(main_window, 'update_undo_redo_actions'):
                            main_window.update_undo_redo_actions()
                            break

    @property
    def can_undo(self) -> bool:
        """Check if there are commands that can be undone"""
        return len(self._undo_stack) > 0

    @property
    def can_redo(self) -> bool:
        """Check if there are commands that can be redone"""
        return len(self._redo_stack) > 0



class MoveItemCommand(Command):
    """Command for moving a single MusicItem"""
    def __init__(self, item, old_pos: QPointF, new_pos: QPointF):
        self.item = item
        self.old_pos = old_pos
        self.new_pos = new_pos
        # Calcola i valori di cAttacco
        self.old_attack = old_pos.x() / (item.scene().pixels_per_beat * item.scene().zoom_level)
        self.new_attack = new_pos.x() / (item.scene().pixels_per_beat * item.scene().zoom_level)

    def execute(self):
        """Esegue il movimento dell'item alla nuova posizione"""
        self.item.setPos(self.new_pos)
        self.item.params['cAttacco'] = self.new_attack
        
    def undo(self):
        """Ripristina l'item alla posizione precedente"""
        self.item.setPos(self.old_pos)
        self.item.params['cAttacco'] = self.old_attack