# rcdgla

This is a lightweight utility for converting OT-Soft style tableaux into a format that Praat can read. Your OT-Soft tableaux should be in .txt format (and have a .txt extension). The format is described in more detail at:

https://linguistics.ucla.edu/people/hayes/otsoft/
and:
https://people.umass.edu/othelp/manual.html#manual

To use the script, you need to have Python3 installed. Run it as follows:

$ python3 converter.py path_to_file/fielname.txt

The script will create filename.OTGrammar and filename.PairDistribution. They will be placed in the same directory as the original file. There are examples in sample_files in this repository.

