import c4d
from c4d import gui, PLUGINFLAG_COMMAND_OPTION_DIALOG, PLUGINFLAG_HIDEPLUGINMENU
from c4d.gui import GeDialog

PLUGIN_ID = 1060707
# PLUGIN_GROUP_ID = c4d.plugins.MENUPRIORITY_PYTHON_PLUGINS_START + 1

class TakeBatcherDialog(c4d.gui.GeDialog):
    
    def __init__(self):
      super(TakeBatcherDialog, self).__init__()
      self.materials = [] 

    # vytvoření dialogového okna
    # tenhle soubor prepisuje vsechny ostatni, tzn. ze napr nazvy v tomto souboru budou k zobrazeni v pluginu
    def CreateLayout(self):
        self.SetTitle("Take Batcher")
        
        # první řádek
        self.GroupBegin(1000, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 3, 1, "")
        self.AddStaticText(1001, c4d.BFH_LEFT, name = "General resource path")
        self.AddEditText(1002, c4d.BFH_SCALEFIT, initw=400)
        self.AddButton(1003, c4d.BFH_SCALEFIT, name="...")
        self.GroupEnd()

        # druhý řádek
        self.GroupBegin(1004, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,3,1,"")
        self.AddStaticText(1005,c4d.BFH_LEFT, name = "Relative resource path")
        self.AddEditText(1006,  c4d.BFH_SCALEFIT, initw=400)
        self.AddButton(1007, c4d.BFH_SCALEFIT, name="...")
        self.GroupEnd()

        # třetí řádek
        self.GroupBegin(1008, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,2,2,"")
        self.AddCheckbox(1009, c4d.BFH_SCALEFIT, name = "Corona render multipass")
        self.AddButton(1010, c4d.BFH_SCALEFIT | c4d.BFV_CENTER, name = "Create takes for selected materials")
        self.GroupEnd()

        # čtvrtý řádek

        return True
    
    def Command(self, id, msg):
        if id == 1003:
            print("KLIK KLIK KLIK")
        elif id  == 1007:
            print("NECUM")
        elif id == 1010:
            print("KLIKACKA")
        return True
    
    def CoreMessage(self, id, msg):
        if id == c4d.EVMSG_CHANGE:
            if msg.GetId() == 1002:
                print("EDITITITIT")
            elif msg.GetId() == 1006:
                print("Resource editeretet")
        return True

class TakeBatcherPlugin(c4d.plugins.CommandData):

    def __init__(self):
        super(TakeBatcherPlugin, self).__init__()

    def Execute(self, doc):
        dialog = TakeBatcherDialog()
        dialog.Open(c4d.DLG_TYPE_MODAL, defaultw= 450, defaulth=150)
        return True

if __name__ == '__main__':
    # Register the plugin with a unique ID and group ID
    c4d.plugins.RegisterCommandPlugin(
        id=PLUGIN_ID,
        str='Take Batcher',
        info= PLUGINFLAG_COMMAND_OPTION_DIALOG,
        icon=None,
        help='HELP',
        dat=TakeBatcherPlugin(),
    )