import numpy as np
import matplotlib.pyplot as plt
from readability import Readability as rdbl
from tabulate import tabulate
from collections import defaultdict
from decimal import Decimal
import numpy as np

import os, shutil, copy
from pathlib import Path

class Newdict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
  
def calc_stats(xlist):
	x_avg = np.mean(xlist)
	x_min = np.min(xlist)
	x_max = np.max(xlist)
	x_std = np.std(xlist)
	return x_avg, x_min, x_max, x_std
	
def gen_plot(xlist, titlex, save_fname):
	plt.hist(xlist,bins=100, edgecolor='black')
	plt.title(titlex)
	plt.xlabel(' cosine similarity')
	plt.ylabel('count')
	plt.savefig(save_fname)
	plt.show(block=False)


def adjust_calc(len_html_list, calc):
	items = []
	items.append(len_html_list - calc[1])
	items[1:] = ["%.3f"%item for item in calc[2:]]
	return items
	
def mk_subdir(sub_dir):
	if os.path.exists(sub_dir):
		shutil.rmtree(sub_dir)
	os.makedirs(sub_dir)
	return

def calc_rdbility_txt(text, f_num, extractor, dictx, dict_nem):
	r = rdbl(text)
	try:
		fle_k = r.flesch_kincaid().score
	except:
		fle_k = None
	try:
		fle = r.flesch().score
	except:
		fle = None
	try:
		gun = r.gunning_fog().score
	except:
		gun = None
	try:
		col = r.coleman_liau().score
	except:
		col = None
	try:	
		dal = r.dale_chall().score
	except:
		dal = None
	try:
		ari = r.ari().score
	except:
		ari = None
	try:
		lin = r.linsear_write().score
	except:
		lin = None
	try:
		smo = r.smog(all_sentences=True).score
	except:
		smo = None
	try:
		spa = r.spache().score
	except:
		spa = None
		
	dictx[extractor]['fle_k'][f_num] = fle_k
	dictx[extractor]['fle'][f_num] = fle
	dictx[extractor]['gun'][f_num] = gun
	dictx[extractor]['col'][f_num] = col	
	dictx[extractor]['dal'][f_num] = dal
	dictx[extractor]['ari'][f_num] = ari
	dictx[extractor]['lin'][f_num] = lin
	dictx[extractor]['smo'][f_num] = smo
	dictx[extractor]['spa'][f_num] = spa

	dict_nem[f_num][extractor]['fle_k'] = fle_k
	dict_nem[f_num][extractor]['fle'] = fle
	dict_nem[f_num][extractor]['gun'] = gun
	dict_nem[f_num][extractor]['col'] = col
	dict_nem[f_num][extractor]['dal'] = dal
	dict_nem[f_num][extractor]['ari'] = ari
	dict_nem[f_num][extractor]['lin'] = lin
	dict_nem[f_num][extractor]['smo'] = smo
	dict_nem[f_num][extractor]['spa'] = spa
	

def get_text_in_dir(text_directory):
	path_list = []
	name_list = []
	cwd = os.getcwd()
	os.chdir(text_directory)
	for name in os.listdir("."):
		if os.path.isfile(name):
			name_list.append(name)
			path_list.append(os.path.abspath(name))
	os.chdir(cwd)
	return path_list, name_list


def get_f_names(dirx):
	f_list = []
	cwd = os.getcwd()
	os.chdir(dirx)
	for fname in os.listdir("."):
		if os.path.isfile(fname):
			f_list.append(fname)
	os.chdir(cwd)
	return f_list

def gen_readability_dicts(fp_list):
	dict_mn = Newdict() # dictionary[[measure][num]
	dict_nm = Newdict() # dictionary[num][measure]
	for fname in fp_list:
		f_stem = Path(fname).stem
		#print(f'processing {fname}')	
		f_int = f_stem[1:4]
		with open(fname, 'r') as file_in:
			text = file_in.read()
		extractor = "sample"
		calc_rdbility_txt(text, f_int, extractor, dict_mn, dict_nm)
	return dict_mn, dict_nm

def check_and_fix_dict(dictx):
	bad_keys = []
	for k, v in dict(dictx).items():
		if v is None:
			del dictx[k]
			bad_keys.append[k]
	for k, v in dict(dictx).items():
		if v>100:
			del dictx[k]
			bad_keys.append[k]
	return bad_keys

def get_bad_keys(dictx, dir_nlist, measures):
# use to get f_num keys with bad values from readability_dict[extractor][measures][f_num]
	bad_fnum = []
	for d in dir_nlist:
		for m in measures:
			for k, v in dictx[d][m].items():
				if v is None:
					print(f'{v} found at {d},{m},{k}, bad key {k}')
					if k not in bad_fnum:
						bad_fnum.append(k)
						
				elif v>100:
					print(f'{v} found at {d},{m},{k}, bad key {k}')
					if k not in bad_fnum:
						bad_fnum.append(k)
						
	return bad_fnum

def pairwise_merge(list1, list2):
  """
  Returns:
    list: A list of lists, where each sublist contains two elements, one from each input list.
  """
  merged_list = []
  for i in range(len(list1)):
    merged_list.append([list1[i], list2[i]])
  return merged_list

def get_lowest_level_keys(nested_dict):
	lowest_level_keys = []
	list_x = []
	done = 0

	def traverse(current_dict):
		nonlocal done
		nonlocal list_x
		nonlocal lowest_level_keys  # Access the outer variable
		for value in current_dict.values():
			if isinstance(value, dict):
				traverse(value)  # Recurse for nested dictionaries
				
			elif done == 0:
				list_x = list(current_dict.keys())[:]
				lowest_level_keys = list_x[:] # Add keys of lowest-level dict
				#print("added list: ", list_x)
				#print(*list_x)
				done = 1

	traverse(nested_dict)
	return lowest_level_keys

def compare_meas(measures, meas_list):
	k=0
	passok = 1
	for item in measures:
#		print(k," item: ",item,"meas_lis[k]: ",meas_list[k])
		if item != meas_list[k]:
			print(k, " measures: ",measures[k],"meas_list: ",meas_list[k])
			print(k, ' ',item, ' is not equal to ', meas_list[k])
			passok = 0
		k += 1
	if passok == 1:
		#print("PASSED measure check")
		return passok
	return passok
		

def gen_values_tbl(nem_sorted_dict, measures):
	table_x = []
	hdr = ["num"] + ["extractor"] + measures
	#print()
	#print(*hdr)
	meas_list = get_lowest_level_keys(nem_sorted_dict)
	#print(*meas_list)
	compare_meas(measures, meas_list)
	print()

	for k1, v1 in nem_sorted_dict.items():
		for k2, v2 in v1.items():
			row=[]
			row.append(k1)
			row.append(k2)
			for k3, v3 in v2.items():
				if v3 is None:
					v3 = 999999
				row.append(v3)
			#print(f'values_table, {k1} {k2} {k3} row is: {row}')
			table_x.append(row)
	print("Readability measures of text samples. None values have been replaced by 999999")
	print(tabulate(table_x, headers=hdr,  tablefmt="fancy_grid", numalign="decimal", floatfmt=".2f", showindex=False))

def get_top_level_vals(nested_dict):
	top_level_dicts = []
	for value in nested_dict.values():
		if isinstance(value, dict):
			for k, v in value.items():
				top_level_dicts.append(k)  # Add only top-level dictionaries
	return top_level_dicts


def gen_avg_min_max_values_tbl(emn_sorted_dict):
	table_avg = []
	table_min = []
	table_max = []
	tl_values = get_top_level_vals(emn_sorted_dict)
	#print()
	#print(*tl_values) # top level values of the emn dictionary are the measures, m
	print()
	hdr = ["extractor"] + tl_values

	for k1, v1 in emn_sorted_dict.items():
		row_avg = []
		row_avg.append(k1)
		row_min = []
		row_min.append(k1)
		row_max = []
		row_max.append(k1)
		for k2, v2 in v1.items():
			v_sum = 0.0
			v_min = 999999
			v_max = 0.0
			for k3, v3 in v2.items():
				if v3 is None:
					#v3 = 999999
					continue
				if v3 > v_max:
					v_max = v3
				if v3 < v_min:
					v_min =v3
				v_sum = v_sum + v3
				#print("k1:",k1,"k2:",k2,"k3:",k3," v: ",v3, " min: ",v_min, " max: ", v_max, " sum: ",v_sum)
			v_avg = v_sum/len(v2)
			row_avg.append(v_avg)
			row_min.append(v_min)
			row_max.append(v_max)
			#print(f'{k1} {k2} sum is: {v_sum}, num: {len(v2)}, avg is: {v_avg}, min: {v_min}, max: {v_max}' )
		table_avg.append(row_avg)
		table_min.append(row_min)
		table_max.append(row_max)
	print("AVERAGE VALUES")
	print(tabulate(table_avg, headers=hdr,  tablefmt="fancy_grid", numalign="decimal", floatfmt=".2f", showindex=False))
	print("MINIMUM VALUES")
	print(tabulate(table_min, headers=hdr,  tablefmt="fancy_grid", numalign="decimal", floatfmt=".2f", showindex=False))
	print("MAXIMUM VALUES")
	print(tabulate(table_max, headers=hdr,  tablefmt="fancy_grid", numalign="decimal", floatfmt=".2f", showindex=False))
	

def get_nth_level_keys(dictx, n):
	if n == 0:
		return list(dictx.keys())

	if isinstance(dictx, dict):
		for key in dictx:
			if isinstance(dictx[key], (dict, list)):
				result = get_nth_level_keys(dictx[key], n - 1)
				if result:
					return result
	return []


def dict_depth(dictx): # returns the depth of nested dictionary dictx
    if not isinstance(dictx, dict):
        return 0
    return 1 + max(map(dict_depth, dictx.values())) 


def copy_first_dict_at_depth(nested_dict, depth, current_depth=0):
	"""Copies the first dictionary found at a specific depth within nested_dict.
	   depth = 0 will provide the first nested dictionary
	   depth = 1 will provide the first nested dictionary within the first nested dictionary
	   etc.
	   depth should not exceed <max depth of nested dictionary - 1>, 1 less than max depth.
	"""		 
	if depth == current_depth:
		return copy.deepcopy(next(iter(nested_dict.values())))  # Create a deep copy at the target depth

	copied_dict = {}
	for key, value in nested_dict.items():
		if isinstance(value, dict):
			copied_value = copy_first_dict_at_depth(value, depth, current_depth + 1)
			if copied_value is not None: 
				return copied_value
		else:
			if current_depth != depth:
				copied_dict[key] = value
	return copied_dict

def cal_correlations(emn_sorted_dict):
	tl_values = get_top_level_vals(emn_sorted_dict)
	#print("tl_values")
	#print(*tl_values) # top level values of the emn dictionary are the measures, m
	#print()
	
	dict_mn = Newdict()
	for k1, v1 in emn_sorted_dict.items():
		dict_mn = copy.deepcopy(v1) # this removes the e from the emn dictionary and leaves mn, measures and numbers
	
	mn_keys = list(dict_mn.keys())
	if mn_keys != tl_values:
		print("ERROR keys do not match at top level")
		print("tl_values: ",tl_values)
		print("mn_keys: ", mn_keys)
		print()
		return None
		
	table_corr = []
	hdr = ["measure"] + tl_values
	#print("hdr")
	#print(hdr)
	print()
	corr_dict = Newdict()
	for m in dict_mn.keys():
		for kx in tl_values:
			corr_dict[m][kx] = 0.0
			
	for m in dict_mn.keys():
		for kx in tl_values:
			list_1 = dict_mn[m].values()
			list_2 = dict_mn[kx].values()
			filtered_data = list(zip(list_1, list_2))
			filtered_data = [pair for pair in filtered_data if None not in pair]
			list_1, list_2 = zip(*filtered_data)
			correlation = np.corrcoef(list_1, list_2)[0, 1]
			corr_dict[m][kx] = correlation
		table_row = list(corr_dict[m].values())
		table_row = [m] + table_row
		#print("table_row: ", table_row)
		table_corr.append(table_row)
	
	
	print("Correlation between readability measures")
	print(tabulate(table_corr, headers=hdr,  tablefmt="fancy_grid", numalign="decimal", floatfmt=".3f", showindex=False))

def add_values(list1, list2):
	"""Adds the values of two lists of equal length"""
	if len(list1) != len(list2):
		raise ValueError("Lists must be of equal length.")
	new_list = []
	for i in range(len(list1)):
		new_list.append(list1[i] + list2[i])
	return new_list

	
		
def sort_innermost_dicts(dictx):
	if isinstance(dictx, dict):
		for key, value in dictx.items():
			if isinstance(value, dict):
				dictx[key] = sort_innermost_dicts(value)
			else:
				dictx[key] = sorted(value) if isinstance(value, list) else value
	return dict(sorted(dictx.items()))

def sort_dict(dictx):
	"""Sorts a dictionary by keys."""
	sorted_dict = {}
	for key in sorted(dictx.keys()):
		sorted_dict[key] = dictx[key]
	return sorted_dict


def traverse_nested_dict(dict1, hierarchy=''):
	for key, value in dict1.items():
		if isinstance(value, dict):
			traverse_nested_dict(value, hierarchy + key + '.')
		else:
			print(hierarchy + key + ': ' + str(value) + '  hierarchy is ' + hierarchy)
			
def traverse_k1k2k3_dict(dictx, d_name):
	print(d_name)
	for k1, v1 in dictx.items():
		for k2, v2 in v1.items():
			row=[]
			row.append(k1)
			row.append(k2)
			print(k1,' ',k2,' ',end=' ')
			for k3, v3 in v2.items():
				row.append(v3)
				print(k3, ':  ', v3, ',',end=' ')
			print()
	print()


def check_emn_nem_dicts(emn_dict, nem_dict):
	passd = 1
	for k1, v1 in nem_dict.items():
		for k2, v2 in v1.items():
			for k3, v3 in v2.items():
				if nem_dict[k1][k2][k3] != emn_dict[k2][k3][k1]:
					passd=0
					print(f'not equal at [{k1}][{k2}][{k3}]; {str(v3)} ne {emn_dict[k2][k3][k1]}')
	if passd == 1:
		#print("check_emn_nem_dicts PASSED")
		return passd
	return passd

def main():

	measures = ['fle_k', 'fle', 'gun', 'col', 'dal', 'ari', 'lin', 'smo', 'spa']
	meas_names = ['flesch_kincaid', 'flesch', 'gunning', 'coleman_liau', 'dale_chall', 'ari', 'linsear_write', 'smog', 'spache']

	text_directory = "./sample_engl_texts"
	fp_list, name_list = get_text_in_dir(text_directory)

	name_list.sort()
	#print(*name_list)
	readability_mn_dict, rbly_nm_dict = gen_readability_dicts(fp_list)

	#traverse_k1k2k3_dict(readability_mn_dict, "readability_mn_dict")
	readability_mn_sorted_dict = sort_innermost_dicts(readability_mn_dict)
	#traverse_k1k2k3_dict(readability_mn_sorted_dict, "readability_mn_sorted_dict")

	#traverse_k1k2k3_dict(rbly_nm_dict, "rbly_nm_dict")
	rbly_nm_sorted_dict = sort_dict(rbly_nm_dict)
	#traverse_k1k2k3_dict(rbly_nm_sorted_dict, "rbly_nm_sorted_dict")

	check_emn_nem_dicts(readability_mn_sorted_dict, rbly_nm_sorted_dict)

	gen_values_tbl(rbly_nm_sorted_dict, measures)
	gen_avg_min_max_values_tbl(readability_mn_sorted_dict)

	print()
	cal_correlations(readability_mn_sorted_dict)
	print()
	

if __name__ == "__main__":
    main()
