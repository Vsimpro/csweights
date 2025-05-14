def read_file( filename : str ):

    lines : str = []

    with open( filename, "r" ) as file:
        for line in file.readlines():
            lines.append( line.strip("\n") )

    return lines


def defang_item_url( url : str ) -> str:
    return url.split("/730/")[ 1 ].replace("%20", "_").replace("%3A", ":")