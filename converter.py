#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools, os


def read_tableau(path):
    '''
    returns a python dictionary of inputs with output candidates, along with information 
    about winner/loser status and violation marks for each constraint
    '''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n').split('\t') for line in f.readlines() if not line.strip()=='']
            tabdic = {}
            con_names = [x for x in lines[1] if x != '']
            for line in lines[2:]:
                if line[0].startswith('['): #in case OTHelp format is used, [end of tableaux] and [minimal weight] lines
                    pass
                else:
                    inform = line[0]
                    cand = line[1]
                    if line[2] in['1', 1]:
                        iswinner=True
                    else: 
                        iswinner=False
                    freq = line[2]
                    num_violations = dict(zip(con_names, [x for x in line[3:]]))
                    if not inform=='':
                        curr_input = inform
                    if freq=='':
                        freq = '0'
                    tabdic[(curr_input,cand)] = {'winner':iswinner, 'num_viol':num_violations, 'freq': freq}
            for cand in tabdic:
                for c in con_names:
                    if tabdic[cand]['num_viol'][c] == '':
                        tabdic[cand]['num_viol'][c] = 0
                    else:
                        tabdic[cand]['num_viol'][c] = abs(int(tabdic[cand]['num_viol'][c]))
            return (tabdic, con_names)
    except IOError:
        print("please make sure your file is in plain text format and is correctly formatted. See the OTHelp manual, https://people.umass.edu/othelp/OTHelp.pdf, section 3")
       

def make_condic(tabdic, con_names):
    '''
    returns a dictionary with constraints as keys, and W and L preferences as applicable along with  pairs of winners and losers supporting each 
    '''
    condic = {}.fromkeys(con_names)
    winners = [x for x in tabdic if tabdic[x]['winner']]
    losers = [x for x in tabdic if not tabdic[x]['winner']]
    for cons in condic:
        condic[cons] = {'w_preferred': [], 'l_preferred': []}
        for win in winners:
            for los in losers:
                if win[0]==los[0]:
                    if tabdic[win]['num_viol'][cons]<tabdic[los]['num_viol'][cons]:
                        if not (win, los) in condic[cons]['w_preferred']:
                            condic[cons]['w_preferred'].append((win, los))
                    elif tabdic[los]['num_viol'][cons]<tabdic[win]['num_viol'][cons]:
                        if not (win, los) in condic[cons]['l_preferred']:
                            condic[cons]['l_preferred'].append((win, los))
    return condic

def make_support_table(tabdic, con_names):
    '''
    for any pair of candidates derived from the same input, find the constraints that prefer the first cand in the pair, and the constraints that prefer the 2nd cand in the pair 
    '''
    support = {}
    for pair in itertools.permutations(tabdic, 2):
        if pair[0][0]==pair[1][0]: #only forms derived from the same input are compared
            support[pair] = {'w_pref_constraints':'', 'l_pref_constraints':''}
            support[pair]['w_pref_constraints']= [x for x in con_names if tabdic[pair[0]]['num_viol'][x]<tabdic[pair[1]]['num_viol'][x]] 
            support[pair]['l_pref_constraints']= [x for x in con_names if tabdic[pair[0]]['num_viol'][x]>tabdic[pair[1]]['num_viol'][x]]
    return support

def convert_to_praat(inpath):
    '''
    this function takes in an OT-Soft tableau and converts it to Praat's format.
    The 'path' argument is for the input file. 
    The output file will be given a default name, depending on the input file's name.
    this assumes that the file ends in .txt.
    '''
    if not(inpath.endswith('.txt')):
        print('Please make sure your input file ends in .txt.')
    else:
        newname = os.path.splitext(inpath)[0] +'.OTGrammar'
        pairdist = os.path.splitext(inpath)[0]+'.PairDistribution'
        overwrite = "y"
        if os.path.isfile(newname):
            overwrite = input('file ' + newname + ' exists. Ovewrite? [y/n] ')
            if overwrite == 'n':
                print("exiting")
                exit()
            else:
                print('overwriting your file')
        if overwrite == 'y': 
            (tabdic, con_names) = read_tableau(inpath)
            with open(newname, 'w', encoding='utf-8') as f:
                f.write('File type = "ooTextFile"\nObject class = "OTGrammar 2"\n\ndecisionStrategy = <OptimalityTheory>\nleak = 0\n'+str(len(con_names)) + ' constraints\n')
                counter = 1
                for cons in con_names:
                    #f.write('constraint [%s]: "%s" 100 100 1 ! %s\n' % (counter, cons, cons))
                    f.write('constraint [%s]: "%s" 100 100 1\n' % (counter, cons))
                    counter+=1
                f.write('\n0 fixed rankings\n\n' + str(len(tabdic)) + ' tableaus\n')
                counter = 1 #for inputs
                inputs = list(set([x[0] for x in tabdic]))
                for inp in inputs:
                    candidates = [x[1] for x in tabdic if x[0] == inp]
                    f.write('input [%s]: "%s" %s\n' % (counter, inp, len(candidates)))
                    counter2=1
                    for cand in candidates:
                        f.write('   candidate [%s]: "%s" %s\n' % (counter2, cand, ' '.join([str(tabdic[(inp, cand)]['num_viol'][cons]) for cons in con_names])))
                        counter2 += 1
                    counter+=1
            print('Done writing .OTGrammar file')
        overwrite2='y'
        if os.path.isfile(pairdist):
            overwrite2 = input('file '+ pairdist + ' exists. Overwrite? [y/n] ')
            if overwrite2== 'n':
                print('exiting')
                exit()
            else:
                print('overwriting your file')
        if overwrite2 == 'y':
            tabdic = read_tableau(inpath)[0]
            with open(pairdist, 'w', encoding='utf-8') as f:
                f.write('"ooTextFile"\n"PairDistribution"\n\n')
                f.write(str(len(tabdic)) + ' pairs\n\n')
                for pair in tabdic:
                    f.write('"%s"\t"%s"\t%s\n' % (pair[0], pair[1], tabdic[pair]['freq']))
            print("Done writing .PairDistribution file")



if __name__=='__main__':
    '''
    command line instructions:
    
    $python3 converter.py path-to-your-textfile

    The input file should follow OT-Soft format (also OT-Help, etc.)

    converts the file ending in .txt to a Praat-compatible GLA OTGrammar and PairDistribution files. They will be placed in the same directory as the input file.
    '''
    import sys
    try:
        convert_to_praat(sys.argv[1])
    except IOError:
        print('please make sure that ' + sys.argv[1] + ' exists')
        print('please also make sure that there is no file that would be overwritten by conversion.')
