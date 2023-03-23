import c4d
import os.path
from c4d import gui, PLUGINFLAG_COMMAND_OPTION_DIALOG, PLUGINFLAG_HIDEPLUGINMENU, bitmaps, FILESELECTTYPE_ANYTHING, PH_2D_TRACK_USER_trackWindowSizeActive_STR_DEPRECATED, documents
from c4d.gui import GeDialog
import os

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
        self.AddStaticText(1001, c4d.BFH_LEFT, name = "General output path")
        self.AddEditText(1002, c4d.BFH_SCALEFIT, initw=400)
        self.AddButton(1003, c4d.BFH_SCALEFIT, name="...")
        self.GroupEnd()

        # druhý řádek
        self.GroupBegin(1004, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,3,1,"")
        self.AddStaticText(1005,c4d.BFH_LEFT, name = "Relative output path")
        self.AddEditText(1006,  c4d.BFH_SCALEFIT, initw=400)
        self.AddButton(1007, c4d.BFH_SCALEFIT, name="...")
        self.GroupEnd()

        # třetí řádek
        self.GroupBegin(1008, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 2, 1, "")
        self.AddStaticText(1009, c4d.BFH_LEFT, name = "Save Corona multi-pass")
        self.AddCheckbox(1010, c4d.BFH_LEFT,initw=10, inith=10, name = "")
        self.GroupEnd()

        # čtvrtý řádek
        self.GroupBegin(1011, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, 1, "")
        self.AddButton(1012, c4d.BFH_LEFT,initw=300, name = "Create takes for selected materials")
        self.GroupEnd()

        return True
    
    def InitValues(self):
        self.Enable(1010, False)

        return True
    
    def Command(self, id, msg):
        doc = c4d.documents.GetActiveDocument()
        if id == 1003:
            generalPath = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Select directory", c4d.FILESELECT_DIRECTORY)
            if generalPath:
                self.SetString(1002, generalPath)
                self.Enable(1007, False)
                self.Enable(1006, False)
                self.Enable(1005, False)
                self.Enable(1010, True)
        elif id  == 1007:
            relativePath = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Select directory", c4d.FILESELECT_DIRECTORY)
            if relativePath:
                self.SetString(1006, relativePath)
                self.Enable(1003, False)
                self.Enable(1001, False)
                self.Enable(1002, False)
                self.Enable(1010, True)
        elif id == 1012:
            materials = doc.GetActiveMaterials()
            generalPath = self.GetString(1002)
            relativePath = self.GetString(1006)
            if not generalPath and not relativePath:
                c4d.gui.MessageDialog("Choose either general or output path.", type=c4d.GEMB_ICONEXCLAMATION)
                return
            # pokud se vybere General output path
            if generalPath:
                # provadeni akce u aktivnich materialu
                if not materials:
                    c4d.gui.MessageDialog("You have not selected any materials", type=c4d.GEMB_ICONEXCLAMATION)
                    return
                for material in materials:
                    renderData = c4d.documents.RenderData()
                    renderData.SetName(material.GetName())
                    renderData[c4d.RDATA_PATH] = generalPath + "\\" + material.GetName()
                    renderData[c4d.RDATA_SAVEIMAGE] = True
                    renderData[c4d.RDATA_FORMAT] = c4d.FILTER_PNG
                    # doc.SetActiveRenderData(renderData)
                    if self.GetBool(1010):
                        renderData[c4d.RDATA_MULTIPASS_FILENAME] = generalPath + "\\" + material.GetName()
                        renderData[c4d.RDATA_MULTIPASS_SAVEIMAGE] = True
                        renderData[c4d.RDATA_MULTIPASS_ENABLE] = True
                        corona_render_id = None
                        for renderer in c4d.plugins.FilterPluginList(c4d.PLUGINTYPE_ANY, True):
                            if "Corona" in renderer.GetName():
                                corona_render_id = renderer.GetID()
                                break
                        renderData[c4d.RDATA_RENDERENGINE] = corona_render_id
                    # vytvoreni taku
                    takeData = doc.GetTakeData()                    
                    take = takeData.AddTake(material.GetName(), None, None)
                    take.SetRenderData(takeData, renderData)
                    doc.InsertRenderData(renderData)


            elif relativePath:
                naming = c4d.gui.InputDialog("Choose a naming", "Naming")
                materials = doc.GetActiveMaterials()
                subfolders = []
                if not materials:
                    c4d.gui.MessageDialog("You have not selected any materials", type=c4d.GEMB_ICONEXCLAMATION)
                    return
                # vyhledani slozek u kterych se bude akce provadet
                for material in materials:
                    for folderName in os.listdir(relativePath):
                        if folderName.startswith(material.GetName()):
                            subfolders.append(os.path.join(relativePath, folderName))
                # provadeni akce u vybranych slozek
                for subfolder in subfolders:
                    previewFolder = os.path.join(subfolder,"PREVIEW")
                    if os.path.isdir(previewFolder):
                        # ovladani render settings
                        renderDataRP = c4d.documents.RenderData()
                        # vymazani napr "_F03" koncovky u slozek
                        renderDataRP.SetName(os.path.basename(subfolder[:-4]))
                        renderDataRP[c4d.RDATA_PATH] = previewFolder + "\\" + naming
                        renderDataRP[c4d.RDATA_SAVEIMAGE] = True
                        renderDataRP[c4d.RDATA_FORMAT] = c4d.FILTER_PNG
                        # render settings pokud je checkbox zaskrtnuty
                        if self.GetBool(1010):
                            renderDataRP[c4d.RDATA_MULTIPASS_FILENAME] = previewFolder + "\\" + naming
                            renderDataRP[c4d.RDATA_MULTIPASS_SAVEIMAGE] = True
                            renderDataRP[c4d.RDATA_MULTIPASS_ENABLE] = True
                            corona_render_id = None
                            for renderer in c4d.plugins.FilterPluginList(c4d.PLUGINTYPE_ANY, True):
                                if "Corona" in renderer.GetName():
                                    corona_render_id = renderer.GetID()
                                    break
                            renderDataRP[c4d.RDATA_RENDERENGINE] = corona_render_id
                        # vytvoreni taku
                        takeDataRP = doc.GetTakeData()
                        # vymazani napr "_F03" koncovky u slozek
                        takeRP = takeDataRP.AddTake(os.path.basename(subfolder[:-4]), None, None)
                        takeRP.SetRenderData(takeDataRP, renderDataRP)
                        doc.InsertRenderData(renderDataRP)
            self.Close()

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

    icon_absolute_path = os.path.join(os.path.dirname(__file__), "res", "images", "ikonka.png")
    plugin_icon = bitmaps.BaseBitmap()
    plugin_icon.InitWith(icon_absolute_path)

    c4d.plugins.RegisterCommandPlugin(
        id=PLUGIN_ID,
        str='Take Batcher',
        info= PLUGINFLAG_COMMAND_OPTION_DIALOG,
        icon=plugin_icon,
        help='HELP',
        dat=TakeBatcherPlugin(),
    )