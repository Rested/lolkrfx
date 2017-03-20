import sys, getopt


def usage():
    print """
    Usage:
    lolkrfx.py -l [for language code e.g. ko_kr] -p [project version code e.g. 0.0.1.23] -s [solution version code e.g. 0.0.0.245]
    e.g.
    lolkrfx.py -l ko_kr -p 0.0.1.23 -s 0.0.0.245

    All three must be specified.
    """


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'l:p:s:h', ['language=', 'project=', 'solution=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    to_lang, pv, sv = None, None, None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-l', '--language'):
            to_lang = arg.lower()
        elif opt in ('-p', '--project'):
            pv = arg
        elif opt in ('-s', '--solution'):
            sv = arg
        else:
            usage()
            sys.exit(2)

    if to_lang is None or pv is None or sv is None:
        usage()
        sys.exit(2)

    first_path = "/Applications/League of Legends.app/Contents/LoL/RADS/projects/lol_air_client/releases/%s/deploy/bin/locale.properties" % pv
    second_path = "/Applications/League of Legends.app/Contents/LoL/RADS/solutions/lol_game_client_sln/releases/%s/deploy/DATA/cfg/defaults/locale.cfg" % sv
    third_path = "/Applications/League of Legends.app/Contents/LoL/RADS/solutions/lol_game_client_sln/releases/%s/configurationmanifest" % sv

    from_lang = ""
    with open(first_path, "r+") as f:
        content = f.read()
        from_lang = content.split("=")[1].lower()
        print "Changing client from %s to %s" % (from_lang, to_lang)
        f.seek(0)
        f.write(content.replace(from_lang, to_lang).replace(sus(from_lang), sus(to_lang)))
        f.truncate()

    with open(second_path, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(content.replace(from_lang, to_lang).replace(sus(from_lang), sus(to_lang)))
        f.truncate()

    with open(third_path, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(content.replace(from_lang, to_lang).replace(sus(from_lang), sus(to_lang)))
        f.truncate()

    print "All done, you can now click launch and enjoy the %s client" % to_lang


def sus(lc):
    sp = lc.split("_")
    return sp[0]+"_"+sp[1].upper()


if __name__ == '__main__':
    main(sys.argv)
