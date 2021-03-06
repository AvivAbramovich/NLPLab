from nlp_lab.crawler import find_all_debates, fetch_single_debate
from nlp_lab.schema import dump_debate
from argparse import ArgumentParser
from os.path import join, exists
from sys import stderr


def __fetch_single_debate__(url, dir_path):
    name = url.split('/')[-1]
    path = (join(dir_path, '%s') if dir_path else '%s') % ('%s.xml' % name)
    if exists(path):
        print('Already successfully parsed and dumped "%s"' % url)
        return

    try:
        debate = fetch_single_debate(url)
    except Exception as e:
        stderr.write('Failed to parse "%s": %s\n' % (url, e))
        # sleep(1)
        # print_exc()
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
    args_parser.add_argument('--fast', help='Find all debates fast', default=False, action='store_true')
    args = args_parser.parse_args()

    if args.url is None:
        g = find_all_debates()
        if args.fast:
            g = list(g)
        for debate_url in g:
            __fetch_single_debate__(debate_url, args.p)
    else:
        __fetch_single_debate__(args.url, args.p)
