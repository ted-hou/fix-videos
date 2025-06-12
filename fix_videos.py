# Import modules
import os, subprocess
from tkinter import filedialog, Tk

# Ask for a root directory
tk = Tk()
tk.withdraw()
selected_dir = filedialog.askdirectory()

# Template file with good header
if not os.path.isfile('video.hdr'):
	template_file = 'E:/desmond38_20250403_laser_3.mp4'
	subprocess.call('recover_mp4 "' + template_file + '" --analyze', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Find all mp4 files in dir and subdirs
for root, dirs, files in os.walk(selected_dir):
	for file in files:
		if file.lower().endswith('.mp4'):
			fullpath = os.path.realpath(os.path.join(root, file))
			is_corrupted = subprocess.call('ffprobe -i "' + fullpath + '"', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

			if is_corrupted:
				print('Fixing corrupted file: "' + fullpath + '", this could take a while...')
				if os.path.isfile('temp_result.h264'):
					os.remove('temp_result.h264')
				subprocess.call('recover_mp4 "' + fullpath + '" ' + 'temp_result.h264 --noaudio --ext', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
				subprocess.call('ffmpeg -r 30.000 -i temp_result.h264 -c:v copy "' + os.path.splitext(fullpath)[0] + '_fixed.mp4"', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			# Fix bad files
			else:
				print('Good file: "' + fullpath + '"')
