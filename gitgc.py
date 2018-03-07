#!/usr/bin/env python3

import sys
import os
import subprocess


def main():
	if len(sys.argv) == 1 or sys.argv[1] in ('-h', '"-H', '/h', '/H', '--help', '--HELP', '?', '/?'):
		print('usage: py gitgc.py <path>')
		sys.exit()

	target_path = sys.argv[1]
	if not os.path.isdir(target_path):
		print(target_path + ' is not a path.')
		return

	work_dir = os.getcwd()
	git_folder_list = []
	get_git_folders(target_path, git_folder_list, False)

	print_git_folders(git_folder_list)
	print('Total git folder: ' + str(len(git_folder_list)) + '\n')

	exec_git_gc(git_folder_list)
	os.chdir(work_dir)


def get_git_folders(cur_path, git_folder_list, print_folder):
	if print_folder:
		print(cur_path)

	item_list = os.listdir(cur_path)

	is_git = False
	sub_folder_list = []
	for elem in item_list:
		fullpath = os.path.join(cur_path, elem)
		if elem == '.git':
			is_git = True

		if os.path.isdir(fullpath):
			sub_folder_list.append(fullpath)

	if is_git:
		git_folder_list.append(cur_path)
		return

	for elem in sub_folder_list:
		get_git_folders(elem, git_folder_list, False)


def print_git_folders(git_folder_list):
	print(' git folder list '.center(31, '='))
	for elem in git_folder_list:
		print(elem)


def exec_git_gc(git_folder_list):
	print('Starting git garbage collection ...\n')
	for elem in git_folder_list:
		os.chdir(elem)
		print(os.getcwd())
		exec_cmd(["git", "gc"])

	print('git garbage collection finished...\n')


def exec_cmd(args):
	output = subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
#	print(type(output))
#	print(output)
	stdout_list = output.decode("ascii").split('\n')
	for elem in stdout_list:
		print(elem)


main()
