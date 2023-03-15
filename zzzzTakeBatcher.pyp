import c4d
from c4d import gui

PLUGIN_ID = 1
PLUGIN_GROUP_ID = c4d.plugins.MENUPRIORITY_PYTHON_PLUGINS_START + 1

class TakeBatcherDialog(c4d.gui.GeDialog):
    # vytvoření dialogového okna
    def CreateLayout(self):
        self.SetTitle("Take Batcher")
        
        # první řádek
        self.GroupBegin(1000, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 2, 1, "")
        self.AddStaticText(1001, c4d.BFH_LEFT, name = "General resource path")
        self.AddEditText(1002, c4d.BFH_SCALEFIT, initw= 200)
        self.AddButton(1003, c4d.BFH_SCALEFIT, name = "...")
        self.GroupEnd()

        # druhý řádek
        self.GroupBegin(1004, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,2,1,"")
        self.AddStaticText(1005,c4d.BFH_LEFT, name = "Relative resource path")
        self.AddEditText(1006,  c4d.BFH_SCALEFIT, initw=200)
        self.AddButton(1007, c4d.BFH_LEFT, name="...")
        self.GroupEnd()

        # třetí řádek
        self.GroupBegin(1008, c4d.BFH_SCALEFIT | c4d.BFV_TOP, 1, 1,"")
        self.AddCheckbox(1009, c4d.BFH_BFH_LEFT, name = "Corona render multipass")
        self.GroupEnd()

        # čtvrtý řádek
        self.AddButton(1010, c4d.BFH_SCALEFIT | c4d.BFV_CENTER, name = "Create takes for selected materials")
        
        return True


class TakeBatcherPlugin(c4d.plugins.CommandData):

    def __init__(self):
        super(TakeBatcherPlugin, self).__init__()

    def Execute(self, doc):
        return True

if __name__ == '__main__':
    # Register the plugin with a unique ID and group ID
    c4d.plugins.RegisterCommandPlugin(
        id=PLUGIN_ID,
        str='TakeBatcher',
        info='Creates Takes from Materials',
        icon=None,
        help='HELP',
        dat=TakeBatcherPlugin(),
    )