from ATE.spyder.widgets.actions_on.model.BaseItem import BaseItem
from ATE.spyder.widgets.actions_on.model.Constants import MenuActionTypes

from ATE.spyder.widgets.actions_on.utils.ExceptionHandler import (handle_excpetions,
                                                                  ExceptionTypes)
from ATE.spyder.widgets.actions_on.protocol.NewProtocolWizard import new_protocol_dialog


class ProtocolItem(BaseItem):
    def __init__(self, name, project_info):
        super().__init__(project_info, name, project_info.parent)

    def new_item(self):
        handle_excpetions(self.project_info.parent,
                          lambda: new_protocol_dialog(self.project_info),
                          ExceptionTypes.Protocol())

    def clone_from_item(self):
        pass

    @staticmethod
    def _get_menu_items():
        return [MenuActionTypes.Add(),
                MenuActionTypes.CloneFrom()]


class ProtocolItemChild(BaseItem):
    def __init__(self, name, path, project_info, parent=None):
        super().__init__(name, path, project_info, parent=parent)

    def delete_item(self):
        pass

    @staticmethod
    def _get_menu_items():
        return [MenuActionTypes.DeleteFile()]
