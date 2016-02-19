# Tacosdetection
Contains the supplementary materials from the paper: "A Dictionary-based Approach to Racism Detection in Dutch Social Media", under review for the TACOS workshop at LREC 2016.

## license

The dictionaries in this repository are available under a CC BY-SA 3.0 License. 
If you use the dictionaries in your work, please cite:

@inproceedings{tulkens2016a,
  title={A Dictionary-based Approach to Racism Detection in Dutch Social Media},
  author={Tulkens, St\'{e}phan and Hilte, Lisa and Lodwyckx, Elise and Verhoeven, Ben and Daelemans, Walter},
  booktitle={Language Resources and Evaluation Conference},
  year={2016},
  organization={European Language Resources Association (ELRA)}
}

## usage

The dictionaries are in .csv format. The first word of each line is the category name, while the other words are words in that category. You can easily automatically create regexes using the '+' and '*' symbols to account for the wildcards.
