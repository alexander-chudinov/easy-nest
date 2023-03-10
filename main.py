# scan in directory for all .dxf files
# open each file
# remove Solidworks logo
# save new file as .dxf

import os
import ezdxf

INPUT_FOLDER_PATH = './dxf_in/'
OUTPUT_FOLDER_PATH = './dxf_out/'

# if the directory does not exist, create it
if not os.path.exists(INPUT_FOLDER_PATH):
    os.makedirs(INPUT_FOLDER_PATH)

if not os.path.exists(OUTPUT_FOLDER_PATH):
    os.makedirs(OUTPUT_FOLDER_PATH)

# scan in directory for all .dxf files
for filename in os.listdir(INPUT_FOLDER_PATH):
    if filename.lower().endswith(".dxf"):
        print("Reading :", filename)
        # open each file
        doc = ezdxf.readfile(INPUT_FOLDER_PATH+filename)

        FILE_IN_MODEL_SPACE = False
        FILE_IN_PAPER_SPACE = False

        # extract layers information
        msp = doc.modelspace()
        msp_grouped_layers = msp.groupby("layer")
        model_layers = msp_grouped_layers.keys()

        # get entities from each layer
        for layer in model_layers:
            print("Analyzing layer: ", layer)
            entities = msp_grouped_layers.get(layer)
            for entity in entities:
                # remove Solidworks logo if found
                if entity.dxftype() == 'MTEXT':
                    if entity.dxf.text == 'SOLIDWORKS Educational Product.' or entity.dxf.text == 'For Instructional Use Only.':
                        print("Found Solidworks logo")
                        msp.delete_entity(entity)
                        print("Deleted Solidworks logo")

        # # save new file as .dxf
        print("Writing :", filename)
        doc.saveas(OUTPUT_FOLDER_PATH+filename, encoding='utf-8')