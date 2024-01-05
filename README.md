# readability_assessment    
22 english text samples are used to assess 9 readability measures.    

The text samples are in file sample_engl_texts.tar.gz.    
The extracted texts should be placed in directory sample_engl_texts.
. 
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

