
# scan in directory for all .dxf files
# open each file
# remove Solidworks logo
# save new file as .dxf
import os
import ezdxf

# TODO: ask for thickness of balsa at start of program

# Constants
INPUT_FOLDER_PATH = './dxf_in/'
OUTPUT_FOLDER_PATH = './dxf_out/'

# Initialize EasyNest file structure
def createFileStructure():
    # if the directory does not exist, create it
    if not os.path.exists(INPUT_FOLDER_PATH):
        os.makedirs(INPUT_FOLDER_PATH)

    if not os.path.exists(OUTPUT_FOLDER_PATH):
        os.makedirs(OUTPUT_FOLDER_PATH)

# Returns a list of files from input folder at INPUT_FOLDER_PATH
def getAllInputDXFs():
    filenames = []
    for filename in os.listdir(INPUT_FOLDER_PATH):
        if filename.lower().endswith(".dxf"):
            filenames.append(filename)
    return filenames

# MODIFIES INPUT DXF doc model space
# Finds and deletes SolidWorks logo entity from DXF model space
def removeAttribution(msp, entities):
    # get entities from layer
    for entity in entities:
        # remove Solidworks logo if found
        if entity.dxftype() == 'MTEXT':
            if entity.dxf.text == 'SOLIDWORKS Educational Product.' or entity.dxf.text == 'For Instructional Use Only.':
                print("Found Solidworks logo")
                msp.delete_entity(entity)
                print("Deleted Solidworks logo")

# MODIFIES INPUT DXF doc model space
def setLayerColor(entities, color):
    for entity in entities:
        # check if entity is not mtext
        if(entity.dxftype() != 'MTEXT'):
            entity.dxf.color = color

# Processes a single DXF file
def processFile(filename):
     # open file
    doc = ezdxf.readfile(INPUT_FOLDER_PATH+filename)

    # extract layers information
    msp = doc.modelspace()
    msp_grouped_layers = msp.groupby("layer")
    model_layers = msp_grouped_layers.keys()

    for layer in model_layers:
        entities = msp_grouped_layers.get(layer)
        removeAttribution(msp, entities)
        setLayerColor(entities, 256)

    # save file
    print("Processed file: " + filename)
    doc.saveas(OUTPUT_FOLDER_PATH+filename, encoding='utf-8')


# MAIN
if __name__ == "__main__":
    # Initialize EasyNest file structure
    createFileStructure()

    # scan in directory for all .dxf files
    filenames = getAllInputDXFs()

    for filename in filenames:
        processFile(filename)