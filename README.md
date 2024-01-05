# readability_assessment    
22 english text samples are used to assess 9 readability measures.    

The text samples are in file sample_engl_texts.tar.gz.    
The sample text files should be placed in directory sample_engl_texts after untaring and unzipping.    
     
The program file, calc_samples_rblty.py, should reside at the same level as directory sample_engl_texts.   

9 readability measures are calculated for each of the 22 sample texts.    
The readability measures are taken from https://pypi.org/project/py-readability-metrics/    
They are:    
fle_k,	Flesch Kincaid Grade Level    
fle,	Flesch Reading Ease    
dal,	Dale Chall Readability    
ari,	Automated Readability Index   
col,	Coleman Liau Index    
gun,	Gunning Fog    
smo,	SMOG (Simple Measure of Gobbledygook)    
spa,	Spache
lin,	Linsear Write    

Running the program, calc_samples_rblty.py, will create tables as shown in readability_table.png and statistics_tables.png.    
The readability table provides 9 measures for each of the 22 samples.    
The statistics tables provide average, minimum, and maximum values for each of the 9 measures and correlations between the measures.    

Additional texts may be added in the sample_engl_textsa directory.    
Each text file should be named sequentially, starting with s023_ then s024_ etc.    
    
The sample texts have been arbitrarily chosen, but are meant to represent varieties in the english language.    
The names are descriptive of the texts.        
Here are the text names:    
s001_st_john.txt    
s002_US_Constitution.txt    
s003_Hamlet.txt    
s004_Lincoln_Gettysburg.txt    
s005_Python_sec5doc.txt    
s006_Ada_Limon_Sharks_in_the_Rivers.txt    
s007_Feynman_room_at_the_bottom.txt    
s008_Hawking_BHofT.txt    
s009_Covey_7habits.txt    
s010_Klara_and_the_Sun.txt    
s011_BGates_Avoid_Climate_Disaster.txt    
s012_BDylan_Murder_Most_Foul.txt    
s013_Britannica_Pyth_Thm.txt    
s014_ToniM_bluest_eye.txt    
s015_Frankenstein.txt    
s016_Emma_G.txt    
s017_Steinem.txt    
s018_Rowling.txt    
s019_ZSmith.txt    
s020_MayaA.txt    
s021_HLammar_pat.txt    
s022_BDylan_Murder_Most_Foul_fixed_punctuation.txt    
     
All measures have a positive pairwise correlation, except for fle, which has negative correlations.    
This is explained as follws.    
The fle measure gives the highest score to its most readable text.    
The other measures give the highest score to the least readable text.    
The scores of these other measure values can be thought of as the grade level needed to understand the text.    
For example, a score of 20 by ari would mean you need 20 years of schooling, a PhD, to understand the text.

Punctuation has a significant impact on the readability measures.    
Text s012 has very little punctuation and scores as almost unreadable.    
Text s022 is the same as s012 but with punctuation added and corrected. It scores as very readable.   

Note: All copyrights to any text here used remain with their respective owners.    
Texts are used under the assumption of fair use. Respect all copyrights.   


