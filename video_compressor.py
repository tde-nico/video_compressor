import os, ffmpeg


def compress_video(video_full_path, output_file_name, target_size):
	min_audio_bitrate = 32000
	max_audio_bitrate = 256000

	probe = ffmpeg.probe(video_full_path)
	duration = float(probe['format']['duration'])
	audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])

	#best_min_size = (32000 + 100000) * (1.073741824 * duration) / (8 * 1024)
	#target_size = best_min_size

	target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)
	if 10 * audio_bitrate > target_total_bitrate:
		audio_bitrate = target_total_bitrate / 10
		if audio_bitrate < min_audio_bitrate < target_total_bitrate:
			audio_bitrate = min_audio_bitrate
		elif audio_bitrate > max_audio_bitrate:
			audio_bitrate = max_audio_bitrate
	video_bitrate = target_total_bitrate - audio_bitrate

	i = ffmpeg.input(video_full_path)
	ffmpeg.output(i, os.devnull,
				  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
				  ).overwrite_output().run()
	ffmpeg.output(i, output_file_name,
				  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'libvo_aacenc', 'b:a': audio_bitrate}
				  ).overwrite_output().run()


if __name__ == "__main__":

	# ffmpeg -i input.mp4 -vcodec h264 -acodec libvo_aacenc output.mp4

	compress_video('input.mp4', 'output.mp4', 50 * 1000) # 50 MB

