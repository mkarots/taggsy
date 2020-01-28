
if __name__ == "__main__":
    import argparse
    import os 
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--files", type=str, nargs='+', required=True)
    args = argument_parser.parse_args() 
    paths = [os.path.join(os.path.abspath(os.getcwd()), item) for item in args.files]
    from taggy import Core
    core = Core()
    if len(paths) >= 2:
        [core.add_document(path=path) for path in paths]
    import pprint
    pprint.pprint(core.most_common())
    
