__author__ = 'Anjana R'


import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import xml.etree.ElementTree as ET
from pathlib import Path
import xmltodict
import os
from xml.dom import minidom
from Library.Utils.Logger import Logger

class XML_Parser:
    """
        This class deals with parsing XML files and conatins methods that simplify XML handling.
        class XML_Parser:
            def xml_to_dictionary
            def xml_to_excel
            def get_tag_value
            def get_multi_tag_values
            def plotgraphfromexcel
    """

    def __init__(self):
        """
            This is a initiator function which initiates the following variables
            file_path -> Path of the given Xml file
            file_name -> Name of the Excel file to be generated
            output_excel_file -> Path of the Excel file to be stored after generating
            root -> Root element of the Xml file
        """
        # self.file_path = Path(__file__).parent.parent.parent / 'Data_resources/Sample_xml_file.xml'
        # self.file_name = str(self.file_path).split('\\')[-1].split(".")[0]
        # path = Path(__file__).parent.parent.parent / 'Excel'
        # os.makedirs(Path(__file__).parent.parent.parent / 'Excel', exist_ok=True)
        # self.output_excel_file = path / f"{self.file_name}.xlsx"
        # self.tree = ET.parse(self.file_path)
        # self.root = self.tree.getroot()
        self.logger = Logger()

    def xml_to_dictionary(self, file_path, root=None):
        """
            This method converts the given Xml file to a dictionary.
            :param root: specify root(default None) else class self.root (object/variable) will be picked
            :return: returns Dictionary representation of the XML file,else False
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            if root is None:
                root = self.root
            if len(root) == 0:
                return root.text
            xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
            data_dict = xmltodict.parse(xml_string)
            return data_dict
        except Exception as e:
            self.logger.log_error(f"Error generated,{e}\n")
            return False

    def xml_to_excel(self, file_path, output_excel_file):
        """
            This method helps in converting the Xml file to Excel file
            :param file_path : specify  path of xml file to be converted
            :param output_excel_file : specifies  path where excel file should be placed
            :return: returns converted Excel file path, False if any error
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = []
            first_child = root.find('*').tag
            book_ids = []
            for book_element in root.findall(f"{first_child}"):
                book_id = book_element.get("id")
                book_ids.append(book_id)
            for element in root.findall(f"{first_child}"):
                data.append(self.extract_data(element))
            df = pd.DataFrame(data)
            df.insert(0, "ID", book_ids)
            df.to_excel(output_excel_file, index=False)
            self.logger.log_info("XML converted to Excel successfully.\n")
            return output_excel_file
        except Exception as error:
            self.logger.log_error(f"Error occured,{error}\n")
            return False

    def extract_data(self, element):
        """
            Extention method to recursively extracts data from given element and its child elements
            :parameter element -> the element in the xml file
            :return : returns the dictionary of all the elements and its child elements, else False
        """
        try:
            data = {}
            for child in element:
                if len(child) > 0:
                    child_data = self.extract_data(child)
                    data.update(child_data)
                else:
                    data[child.tag] = child.text
                    for attr_name, attr_value in child.attrib.items():
                        attr_tag = f"{child.tag}_{attr_name}"
                        data[attr_tag] = attr_value
            return data
        except Exception as error:
            self.logger.log_error(f"Error occured, {error}\n")
            return False

    def get_tag_value(self, tag_id, tag_name):
        """
            This method helps in fetching the tag value by using tag name & id from the Xml file
            :param  tag_name: tag name
            :param tag_id: tag ID of required xml
            :return: returns list of tag value of given tag id & name else False
        """
        try:
            section = self.root.find(f'book[@id="{tag_id}"]')
            if section:
                tag_value = section.find(tag_name)
                if tag_value:
                    childtags=[child.text for child in tag_value.iter() if child.text.strip()]
                    return childtags
                elif tag_value != None:
                    for sub_child in section.iter():
                        if sub_child.tag==tag_name:
                            for sub in sub_child.iter():
                                return sub.text
                else:
                    self.logger.log_error(f"{tag_name}: tag name not found\n")
                    return False
            else:
                self.logger.log_error(f"{tag_id}: tag ID Not found\n")
                return False
        except Exception as e:
            self.logger.log_error(f"Error fetching tag value:,{e}\n")
            return False

    def get_multi_tag_values(self, tag_name):
        """
            This method fetches multiples tag values exists in the given Xml file
            :param tag_name: tag name of the self.root
            :return: list of tag values found in the xml file, else false
        """
        try:
            tag_elements = self.root.findall(f".//{tag_name}")
            if tag_elements == None:
                self.logger.log_error(f"{tag_name} Not found\n")
            else:
                list_ = []
                for element in tag_elements:
                    [list_.append(child.text.strip("\t\n")) for child in element.iter() if child.text.strip("\t\n")]
                return list_
        except Exception as e:
            self.logger.log_error(f"Error fetching tag value:,{e}\n")
            return False

    def plotgraphfromexcel(self, x_axis, y_axis,file_path,output_excel_file):
        """
            This method plots a graph from using given Excel data
            :param x_axis: x-axis value to be plotted
            :param y_axis: y-axis value to be plotted
            :return: returns True if graph has been plotted, else False
        """
        try:
            excel_file_path = self.xml_to_excel(file_path,output_excel_file)
            df = pd.read_excel(excel_file_path)
            x_values = df[x_axis]
            y_values = df[y_axis]
            plt.plot(x_values, y_values)
            plt.xlabel(f'X Label -->{x_axis}')
            plt.ylabel(f'Y Label -->{y_axis}')
            plt.title('Xml to graph')
            plt.grid(True)
            plt.scatter(x_values, y_values, c='red', marker='o')
            plt.savefig(Path(__file__).parent.parent.parent / "Graph/graph.png")
            self.logger.log_info("Graph plotted with provided data\n")
            return True
        except Exception as e:
            self.logger.log_error(f"Error generated while plotting graph,{e}\n")
            return False

    def update_tag_values(self, file_path, tag_name, new_value, occurence="all"):
        """ This method updates the existing tag name with a specified value
            :param file_path : File path of the required xml file
            :param new_tag: new tag name to be added
            :param new_value: new value for the newly added tag name
            :param occurrence: by default it will change all occurrence else takes integer or str value of occurrence
            :return: True if updation is successful ,else False
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            counter = 0
            for elem in root.iter(tag_name):
                if occurence == "all":
                    elem.text = str(new_value)
                    counter += 1
                    tree.write(file_path, encoding='utf-8', xml_declaration=True)
                else:
                    counter += 1
                    if counter == occurence:
                        elem.text = str(new_value)
                        tree.write(file_path, encoding='utf-8', xml_declaration=True)
                        break
            if counter == 0 and counter != "all":
                self.logger.log_error("no tag found...\n")
                return False
            else:
                self.logger.log_info("File updated successfully...\n")
                return True
        except Exception as e:
            self.logger.log_error(f"{e}\n")
            return False
