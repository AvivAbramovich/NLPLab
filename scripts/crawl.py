from crawler import find_all_debates, fetch_single_debate
from schema import dump_debate
from argparse import ArgumentParser
from os.path import join, exists


def __fetch_single_debate__(url, dir_path):
    name = url.split('/')[-1]
    path = (join(dir_path, '%s') if dir_path else '%s') % ('%s.xml' % name)
    if exists(path):
        print('Already successfully parsed and dumped "%s"' % url)
        return

    try:
        debate = fetch_single_debate(url)
    except Exception as e:
        print('Failed to parse "%s": %s' % (url, e))
    else:
        print('Successfully parsed "%s"' % url)
        __dump__(debate, url, path)


def __dump__(debate, url, path):
    # get debate name from url
    dump_debate(debate, path, url)


if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument('p', help='Directory path to save the XMLs', default=None)
    args_parser.add_argument('--url', help='specific url to parse and dump', default=None)
    args = args_parser.parse_args()

    if args.url is None:
        for debate_url in find_all_debates():
            __fetch_single_debate__(debate_url, args.p)
    else:
        __fetch_single_debate__(args.url, args.p)