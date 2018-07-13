#!/usr/bin/env python3

import sys
import os
import subprocess
import glob


def main():
	if len(sys.argv) == 1 or sys.argv[1] in ('-h', '"-H', '/h', '/H', '--help', '--HELP', '?', '/?'):
		print('usage: py gitgc.py <path>')
		sys.exit()

	target_path = sys.argv[1]
	if not os.path.isdir(target_path):
		print(target_path + ' is not a path.')
		return

	work_dir = os.getcwd()

	target_path = os.path.abspath(sys.argv[1])  # converted to absolute path if the path is relative
	git_folders = get_git_folders(target_path, True)

	print_git_folders(git_folders)
	print('Total git folder: ' + str(len(git_folders)) + '\n')

	exec_git_gc(git_folders)
	os.chdir(work_dir)


def get_git_folders(cur_path, print_folder):
	if print_folder:
		print(cur_path)

	os.chdir(cur_path)
	folders = glob.glob("**/.git", recursive=True)

	git_folders = []
	for elem in folders:
		git_folders.append(os.path.dirname(os.path.abspath(elem)))

	return git_folders


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
	stdout_list = output.decode("ascii").split('\n')
	for elem in stdout_list:
		print(elem)


main()
