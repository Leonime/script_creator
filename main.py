import argparse
from pathlib import Path


def main(main_path, default=None, audio_track=None, sub_track=None, no_sub=None, fonts=None, video_tack=None, test=None,
         keep_audio=None):
    current_path = Path(main_path)
    output = current_path / 'output'
    suffix_index = ['.mkv', '.mp4']

    if not output.exists():
        Path(output).mkdir(parents=True, exist_ok=True)

    if default:
        audio_track = '' if audio_track is None else audio_track
        no_sub = True if no_sub else False
        sub_track = '' if sub_track is None else sub_track
        fonts = True if fonts else False

        with open(current_path / 're-encode.sh', 'w') as f:
            for file in sorted(current_path.iterdir()):
                if file.is_file and file.suffix in suffix_index:
                    command = f'ffmpeg -i "{current_path}/{file.name}" -map_metadata 0 '
                    if fonts:
                        command += '-map 0:t '
                    command += '-map 0:v:0 ' if video_tack else '-map 0:v '
                    if keep_audio:
                        command += f'-map 0:a -disposition:a:{audio_track} default '
                    else:
                        command += f'-map 0:a:{audio_track} -disposition:a:0 default '\
                            if audio_track >= 0\
                            else '-map 0:a -disposition:a:0 default '

                    command += '-map 0:s -disposition:s:0 0 ' \
                        if no_sub\
                        else f'-map 0:s -disposition:s:{sub_track} default '
                    command += f'-c copy "{current_path}/output/{file.name}"\n'
                    f.write(command)
                if test:
                    break
    else:
        params_index = {
            'seiya': '-map 0:v -map_metadata 0 -map 0:a:5 -map 0:a:0 -disposition:a:0 default '
                     '-map 0:s -disposition:s:0 0 -c copy',
            'sailor_moon': '-map_metadata 0 -map 0:t -map 0:v -map 0:a:2 -disposition:a:0 default '
                           '-map 0:s:0 -disposition:s:0 default -c copy',
        }

        with open(current_path / 're-encode.sh', 'w') as f:
            for file in sorted(current_path.iterdir()):
                if file.is_file and file.suffix in suffix_index:
                    command = f'ffmpeg -i "{current_path}/{file.name}" {params_index["sailor_moon"]} ' \
                              f'"{current_path}/output/{file.name}"\n'
                    f.write(command)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(prog='script_creator',
                                        usage='%(prog)s [options] --path',
                                        description='Generates a script to edit vidio files')
    my_parser.add_argument('-p', '--path', action='store', type=str, required=True, help='Path to work on')
    my_parser.add_argument('-a', '--audio_track', action='store', type=int, required=False, help='Audio to default')
    my_parser.add_argument('-ka', '--keep_audios', action='store_true', required=False,
                           help='Don\'t delete extra audio tracks')
    my_parser.add_argument('-s', '--sub_track', action='store', type=int, required=False, help='Sub to default')
    my_parser.add_argument('-n', '--no_sub', action='store_true', help='No default sub')
    my_parser.add_argument('-d', '--default', action='store_true', help='Default script')
    my_parser.add_argument('-f', '--fonts', action='store_true', help='Load fonts')
    my_parser.add_argument('-v', '--video_tack', action='store_true', help='fix video track')
    my_parser.add_argument('-t', '--test', action='store_true', help='fix video track')
    args = my_parser.parse_args()
    main(args.path, args.default, args.audio_track, args.sub_track, args.no_sub, args.fonts, args.video_tack, args.test,
         args.keep_audios)
