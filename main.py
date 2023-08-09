import os
import sys
import time
from datetime import datetime
from similar_text import similar_text
from colorama import init, Fore, Style
init()

def update_msg(text):
	""" Puts a new line in place of the old one """
	sys.stdout.write(f'\r{text}')
	sys.stdout.flush()

def balancer(text, target_len):
	""" Aligns text to the specified height using spaces. Made to prevent the text from twitching """
	new_text = text
	while len(new_text) < target_len:
		new_text = " " + new_text
	return new_text

def sort_and_reverse_list(target_list):
	"""
		Sorts the list by keys (from the smallest percentage to the largest)
		And then reverse it (from a large percentage to a smallest)
	"""
	# ↓ Sort by keys, from the smallest percentage to the largest
	sorted_list = dict(sorted(target_list.items(), key=lambda item: item))

	# ↓ Reverses list, from a large percentage to a smallest
	reversed_list = dict(reversed(list(sorted_list.items())))
	return reversed_list

# ↓ Get a list of files in a directory
filelist = os.listdir()
filelist_len = len(filelist)
# ↓ Prepared conversion to a string so that each time the status is updated, do not make a string again
filelist_len_str = str(filelist_len)

threshold = int(input("Threshold > "))

# ↓ Variable where the number of already processed files is stored
general_status = 0

# To avoid duplicates. Example of duplicates:
#  - = 98% = -
# lol1.png
# lol2.png
#
#  - = 98% = -
# lol2.png
# lol1.png
already_logged_files_buffer = {}

# ↓ List where files are stored for output, for which duplicates were found
reported_files = {}

# ↓ List of elapsed time for each iteration
iteration_timings = []

# Stubs
average_format = "??:??"
eta_format = "??:??:??"

iterations_made = 0

try:
	# ↓ Process each file
	for filee in filelist:
		general_status += 1
		# ↓ Status of processed files FOR ONE file
		local_status = 0

		start_iteration_time = time.time()
		for checking_file in filelist:
			local_status += 1
			iterations_made += 1
			# ↓ Find the percentage of similarity between texts
			similarity = similar_text(filee, checking_file)

			# ↓ Filter
			if similarity >= threshold:
				if filee == checking_file or already_logged_files_buffer.get(filee, "_") == checking_file:
					continue # Next iteration, skip this file
				already_logged_files_buffer[checking_file] = filee

				# ↓ Create a list in an array if there is none
				if reported_files.get(str(similarity), "_") == "_":
					reported_files[str(similarity)] = []

				# ↓ Add the text of the found match
				reported_files[str(similarity)].append(f"{Fore.CYAN} - = {similarity}% = -{Style.RESET_ALL}\n{filee}\n{checking_file}")

			# ↓ DRAW STATUS
			update_msg(f"- ({balancer(str(round((local_status/filelist_len)*100)), 3)}%) {Fore.CYAN}{str(general_status)} / {filelist_len_str} ({str(round((general_status/filelist_len)*100))}%){Style.RESET_ALL} • ETA: {eta_format} {Style.DIM}• Iterations made: {iterations_made}{Style.RESET_ALL}") # | Average per file: {average_format} | Local: {str(local_status)} / {filelist_len_str} ()")

		iteration_timings.append(time.time() - start_iteration_time)

		# ↓ Find out the average value of time that takes one file
		average_time = sum(iteration_timings) / len(iteration_timings)

		# ↓ Calculate ETA by taking into account the average time spent per file and multiplying it by the files that are left in the queue
		eta_time = average_time * (filelist_len - general_status)

		# ↓ Make it human-readable
		average_format = datetime.utcfromtimestamp(average_time).strftime('%M:%S')
		eta_format = datetime.utcfromtimestamp(eta_time).strftime('%H:%M:%S')

except KeyboardInterrupt:
	# Do not crash, exit with output
	print("\n\nCtrl+C detected! Exiting..", end="")

print("\n")

reported_files = sort_and_reverse_list(reported_files)
#print(reported_files)

# ↓ Output of all found files
for percent_in_dict in reported_files:
	for items_in_percent in reported_files[percent_in_dict]:
		print(items_in_percent, end="\n\n")
