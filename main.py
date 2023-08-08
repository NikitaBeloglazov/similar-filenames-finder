from similar_text import similar_text
import os
import time
import sys
import pprint

def update_msg(text):
	message = f'\r{text}'
	sys.stdout.write(message)
	sys.stdout.flush()

def sort_and_reverse_list(target_list):
	sorted_list = dict(sorted(target_list.items(), key=lambda item: item))
	reversed_list = dict(reversed(list(sorted_list.items())))
	return reversed_list

def balancer(text, target_len):
	new_text = text
	while len(new_text) < target_len:
		new_text = " " + new_text
	return new_text

filelist = os.listdir()
filelist_len = len(filelist)
filelist_len_str = str(filelist_len)

threshold = int(input("Threshold > "))

general_status = 0

already_logged_files_buffer = {}
reported_files = {}
for filee in filelist:
	general_status += 1

	local_status = 0

	for checking_file in filelist:
		local_status += 1
		similarity = similar_text(filee, checking_file)
		if similarity >= threshold:
			if filee == checking_file or already_logged_files_buffer.get(filee, "_") == checking_file:
				continue
			already_logged_files_buffer[checking_file] = filee
			if reported_files.get(similarity, "_") == "_":
				reported_files[str(similarity)] = []
			reported_files[str(similarity)].append(f" - = {similarity}% = -\n{filee}\n{checking_file}")
		update_msg(f"- ({balancer(str(round((local_status/filelist_len)*100)), 3)}%) {str(general_status)} / {filelist_len_str} ({str(round((general_status/filelist_len)*100))}%)") #| Local: {str(local_status)} / {filelist_len_str} ()")

print("\n")

reported_files = sort_and_reverse_list(reported_files)
for percent_in_dict in reported_files:
	for items_in_percent in reported_files[percent_in_dict]:
		print(items_in_percent, end="\n\n")

print(already_logged_files_buffer)