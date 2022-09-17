import xml.etree.ElementTree as ET
from xml.dom import minidom

class annotation:

    def __init__ (self):
        self.folder = ''
        self.filename = ''
        self.path = ''
        self.size = (0,0,0)
        self.segmented = 0
        self.lighting = []
        self.objects = []

    def meta_init(self,folder='',filename='',path='',size=(),segmented=0,lighting=[]):
        self.folder = folder
        self.filename = filename
        self.path = path
        self.size = size
        self.segmented = segmented
        self.lighting = lighting

    def add_object(self,name,bndbox,pose='Unspecified',truncated=0,difficult=0):
        self.objects.append([name,bndbox,pose,truncated,difficult])

    def objects_to_file(self,path,file_index):
        annot = ET.Element('annotation')
        annot_folder = ET.SubElement(annot,'items')
        annot_filename = ET.SubElement(annot,'filename')
        annot_path = ET.SubElement(annot,'path')
        annot_source = ET.SubElement(annot,'source')
        annot_source_database = ET.SubElement(annot_source,'database')
        annot_size = ET.SubElement(annot,'size')
        annot_size_width = ET.SubElement(annot_size,'width')
        annot_size_height = ET.SubElement(annot_size,'height')
        annot_size_depth = ET.SubElement(annot_size,'depth')
        annot_segmented = ET.SubElement(annot,'segmented')
        annot_lighting = ET.SubElement(annot,'lighting')

        annot_folder.text = self.folder
        annot_filename.text = self.filename
        annot_path.text = self.path
        annot_source_database.text = 'Unspecified'
        annot_size_width.text,annot_size_height.text,annot_size_depth.text = str(self.size[0]),str(self.size[1]),str(self.size[2])
        annot_segmented.text = '0'
        annot_lighting.text = str(self.lighting)
        
        for index,obj in enumerate(self.objects):
            instance = ET.SubElement(annot,'object')
            instance_name = ET.SubElement(instance,'name')
            instance_pose = ET.SubElement(instance,'pose')
            instance_truncated = ET.SubElement(instance,'truncated')
            instance_difficult = ET.SubElement(instance,'difficult')
            instance_bndbox = ET.SubElement(instance,'bndbox')
            instance_bndbox_xmin = ET.SubElement(instance_bndbox,'xmin')
            instance_bndbox_ymin = ET.SubElement(instance_bndbox,'ymin')
            instance_bndbox_xmax = ET.SubElement(instance_bndbox,'xmax')
            instance_bndbox_ymax = ET.SubElement(instance_bndbox,'ymax')
            
            instance_name.text = str(obj[0])
            instance_pose.text = str(obj[2])
            instance_truncated.text = str(obj[3])
            instance_difficult.text = str(obj[4])

            instance_bndbox_xmin.text = str(obj[1][0])
            instance_bndbox_ymin.text = str(obj[1][1])
            instance_bndbox_xmax.text = str(obj[1][2])
            instance_bndbox_ymax.text = str(obj[1][3])
        
        file_data = minidom.parseString(ET.tostring(annot,method='xml',encoding='unicode')).toprettyxml(indent='   ')
        file = open(path,'w')
        file.write(file_data)
