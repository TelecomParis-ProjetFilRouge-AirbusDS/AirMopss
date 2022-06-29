# AirMopss

<table>
  <tr>
    <td align="middle">   Telecom Paris</td>
    <td align="middle"> Airbus Space & Defence </td>
  </tr>
  <tr>
    <td valign="top"><img src="https://upload.wikimedia.org/wikipedia/fr/thumb/d/d9/Logo_T%C3%A9l%C3%A9com_ParisTech.svg/219px-Logo_T%C3%A9l%C3%A9com_ParisTech.svg.png"></td>
    <td valign="middle"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Airbus_Defense_and_Space.svg/320px-Airbus_Defense_and_Space.svg.png"></td>
  </tr>
 </table>

## How to launch airmopss [Read Full Documentation : https://morango.fr/airmopss/] : 
### 1 -  From Terminal
`$ python main.py [-h] [--csv_file CSV_FILE] [--pkl_file PKL_FILE] [--labels_file LABELS_FILE] [--spacy_pipeline SPACY_PIPELINE] [--task TASK] [--split SPLIT] [--labelled_only LABELLED_ONLY]`

#### optional arguments:  
`-h`, `--help`              :  show this help message and exit  
`--csv_file` **CSV_FILE**   : file of news wires (api format), default: data/newsdata.txt  
`--pkl_file` **PKL_FILE**   
`--labels_file` **LABELS_FILE**  file of labeled articles, default: data/newsdata_labels.txt  
`--spacy_pipeline` **SPACY_PIPELINE**  chose spacy pipeline to use [en_core_web_sm], default: en_core_web_sm  
`--task` **TASK**           task to run [qa|generate_pickle|summarize|extract_np|version], default: qa  
`--split` **SPLIT**         splitting mode of content [article|paragraph], default: article  
`--labelled_only` **LABELLED_ONLY**   loads all data or labelled ones only, default: True  

### 2 - From WebApp
`$ ./launch_server.sh`
