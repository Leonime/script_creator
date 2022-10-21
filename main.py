import argparse
from pathlib import Path


def main(main_path, default=None, audio_track=None, sub_track=None, no_sub=None, fonts=None, video_tack=None, test=None,
         keep_audio=None, default_audio=None, default_sub=None):
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

                    command += f'-disposition:a:{default_audio} 0 '\
                        if default_audio\
                        else '-disposition:a:0 0 '

                    command += '-map 0:s -disposition:s:0 0 ' \
                        if no_sub\
                        else f'-map 0:s -disposition:s:{sub_track} default '

                    command += f'-disposition:s:{default_sub} 0 ' \
                        if default_sub \
                        else '-disposition:s:0 0 '

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
    my_parser.add_argument('-p', '--path', action='store', type=str, required=True,
                           help='The path to where the videos are and where the script will be created')
    my_parser.add_argument('-a', '--audio_track', action='store', type=int, required=False,
                           help='The new default audio stream')
    my_parser.add_argument('-ka', '--keep_audios', action='store_true', required=False,
                           help='This will not delete extra audio streams')
    my_parser.add_argument('-da', '--default_audio', action='store', type=int, required=False,
                           help='In case the default audio stream isn\'t the first one please specify here')
    my_parser.add_argument('-s', '--sub_track', action='store', type=int, required=False, help='Sub to default')
    my_parser.add_argument('-ds', '--default_sub', action='store', type=int, required=False,
                           help='In case the default subtitle stream isn\'t the first one please specify here')
    my_parser.add_argument('-n', '--no_sub', action='store_true',
                           help='With this flag set up, there will be no sub selected by default')
    my_parser.add_argument('-d', '--default', action='store_true',
                           help='this is here because I\'m dumb and forgot his purpose, but it has been implemented on'
                                ' the code so it stays, because I\'m too lazy to refactor')
    my_parser.add_argument('-f', '--fonts', action='store_true',
                           help='Sometimes the container has fonts included, this will import them the new file, if the'
                                ' container has no fonts the script will fail, if that happens just remove this flag')
    my_parser.add_argument('-v', '--video_tack', action='store_true',
                           help='Sometimes without this option the script will fail, I think is because a poorly made'
                                ' container, leaving it on all the time affects nothing, but I leave it as an option so'
                                ' it can be removed, because it should not be required, but it fixes poorly made'
                                ' container')
    my_parser.add_argument('-t', '--test', action='store_true',
                           help='It will only create a single file script, so you can test if the generated script'
                                ' works')
    args = my_parser.parse_args()
    main(args.path, args.default, args.audio_track, args.sub_track, args.no_sub, args.fonts, args.video_tack, args.test,
         args.keep_audios, args.default_audio, args.default_sub)
