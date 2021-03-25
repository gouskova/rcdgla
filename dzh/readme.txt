prepare the tableau in normal (Ot-soft) format; that's voice_tableau.txt.

convert using rcdgla converter.py utility (on xcarbon1, should be in bin as a python excecutable; converter voice_tavbleau.txt)

edit file manually to remove a few garbage lines (not crucial; it seems this learner just ignores them.)

the PairDistribution file needs a bit more work. Each input is paired with a surface form that it maps to, not every candidate. each morpheme needs to be given a unique number identifier, which is matched to the morphs in the dzh_urdist.txt file.

NOTE: the converter utility does not print the tableaux in the same order as in the input, so you have to check that the inputs match the right forms in the tableaux.

once the PairDistribution file is manually edited, i copied it to dzh_dist.txt

that format is idiosyncratic and require binary numbering

