import json
import os


def open_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines


def open_all_files(folder, file_endings):
    # The folder containing the text files
    # folder = '/path/to/folder'

    # The list to store the contents of the text files
    text_files = []
    file_names = []

    # List the files in the folder
    for file in os.listdir(folder):
        # Check if the file is a text file
        if file.endswith(file_endings):
            # Store the file name
            file_names.append(file)
            # The list to store the lines of the text file
            lines = []
            # Open the file and read the contents
            with open(os.path.join(folder, file), 'r') as f:
                for line in f:
                    lines.append(line)
            # Append the list of lines to the list of text files
            text_files.append(lines)

    return file_names, text_files  # A list containing the contents of the text files


def create_json(file_names, summarys, name_of_output, name_of_instance):
    outputDict = []
    for i in range(len(summarys[0])):
        output_Temp = {'instance_id': name_of_instance + "-" + str(i)}
        for j, fn in enumerate(file_names):
            # Add to dict for json
            output_Temp[fn] = summarys[j][i]

        outputDict.append(output_Temp)

    jsonString = json.dumps(outputDict)
    jsonFile = open(name_of_output, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


# Create Json out of source PyrXSum source data

#file_names, list_of_summarys = open_all_files('data/PyrXSum(Source)/summaries', '.summary')
#create_json(file_names, list_of_summarys, 'eval_interface/src/data/pyrxsum/pyrxsum-system-summary.json', 'pyrxsum')

#file_names, list_of_labels = open_all_files('data/PyrXSum(Source)/labels', '.label')
#create_json(file_names, list_of_labels, 'eval_interface/src/data/pyrxsum/pyrxsum-golden-labels.json', 'pyrxsum')

# Create Json out of source REALSumm data

#file_names, list_of_summarys = open_all_files('data/REALSumm(Source)/summaries', '.summary')
#create_json(file_names, list_of_summarys, 'eval_interface/src/data/realsumm/realsumm-system-summary.json', 'realsumm')

#file_names, list_of_labels = open_all_files('data/REALSumm(Source)/labels', '.label')
#create_json(file_names, list_of_labels, 'eval_interface/src/data/realsumm/realsumm-golden-labels.json', 'realsumm')