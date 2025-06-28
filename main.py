import argparse
from extract import load_neos, load_approaches
from database import NEODatabase
from filters import create_filters, limit
from helpers import parse_date
from write import write_to_csv, write_to_json


def inspect_neo(db, designation=None, name=None, verbose=False):
    """Inspect a specific Near-Earth Object (NEO).

    Retrieves and displays information about a NEO by its designation or name.
    If verbose is True, also displays its close approach data.

    Args:
        db (NEODatabase): The NEO database to search.
        designation (str, optional): The primary designation of the NEO.
        name (str, optional): The human-readable name of the NEO.
        verbose (bool): Whether to print close approach details.
    """
    neo = None
    if designation:
        neo = db.get_neo_by_designation(designation)
    elif name:
        neo = db.get_neo_by_name(name)

    if not neo:
        print("No matching NEO found.")
        return

    print(
        f"NEO {neo.designation} ({neo.name}) has a diameter of "
        f"{neo.diameter:.3f} km and is "
        f"{'potentially hazardous' if neo.hazardous else 'not potentially hazardous'}."
    )

    if verbose:
        for approach in neo.approaches:
            time = approach.time_str
            print(
                f"- On {time}, '{neo.designation} ({neo.name})' approaches Earth at a "
                f"distance of {approach.distance:.2f} au and a velocity of "
                f"{approach.velocity:.2f} km/s."
            )


def main():
    """Main command-line interface for the NEO inspection/query tool."""
    parser = argparse.ArgumentParser(
        description="Inspect or query Near-Earth Objects (NEOs)."
    )
    subparsers = parser.add_subparsers(dest='command')

    # Inspect subcommand
    inspect_parser = subparsers.add_parser(
        'inspect', help='Inspect a specific NEO.'
    )
    inspect_parser.add_argument('--pdes', help='Primary designation of the NEO.')
    inspect_parser.add_argument('--name', help='Name of the NEO.')
    inspect_parser.add_argument(
        '--verbose', action='store_true',
        help='Show detailed close approach info.'
    )

    # Query subcommand
    query_parser = subparsers.add_parser(
        'query', help='Query close approaches with filters.'
    )
    query_parser.add_argument('--start-date', type=str,
                              help='Filter for start date (YYYY-MM-DD).')
    query_parser.add_argument('--end-date', type=str,
                              help='Filter for end date (YYYY-MM-DD).')
    query_parser.add_argument('--date', type=str,
                              help='Exact date filter (YYYY-MM-DD).')
    query_parser.add_argument('--distance-min', type=float,
                              help='Minimum approach distance (au).')
    query_parser.add_argument('--distance-max', type=float,
                              help='Maximum approach distance (au).')
    query_parser.add_argument('--velocity-min', type=float,
                              help='Minimum approach velocity (km/s).')
    query_parser.add_argument('--velocity-max', type=float,
                              help='Maximum approach velocity (km/s).')
    query_parser.add_argument('--diameter-min', type=float,
                              help='Minimum NEO diameter (km).')
    query_parser.add_argument('--diameter-max', type=float,
                              help='Maximum NEO diameter (km).')
    query_parser.add_argument('--hazardous', action='store_true',
                              help='Filter for hazardous NEOs only.')
    query_parser.add_argument('--not-hazardous', action='store_true',
                              help='Filter for non-hazardous NEOs only.')
    query_parser.add_argument('--limit', type=int, default=10,
                              help='Limit number of results.')
    query_parser.add_argument('--outfile', required=True,
                              help='Path to save results (.csv or .json)')

    args = parser.parse_args()

    # Load data
    neos = load_neos('data/neos.csv')
    approaches = load_approaches('data/cad.json')
    db = NEODatabase(neos, approaches)

    if args.command == 'inspect':
        inspect_neo(
            db,
            designation=args.pdes,
            name=args.name,
            verbose=args.verbose
        )

    elif args.command == 'query':
        filters = create_filters(
            date=parse_date(args.date) if args.date else None,
            start_date=parse_date(args.start_date) if args.start_date else None,
            end_date=parse_date(args.end_date) if args.end_date else None,
            distance_min=args.distance_min,
            distance_max=args.distance_max,
            velocity_min=args.velocity_min,
            velocity_max=args.velocity_max,
            diameter_min=args.diameter_min,
            diameter_max=args.diameter_max,
            hazardous=True if args.hazardous
            else False if args.not_hazardous else None,
        )

        results = limit(db.query(filters), args.limit)

        if args.outfile.endswith('.csv'):
            write_to_csv(results, args.outfile)
        elif args.outfile.endswith('.json'):
            write_to_json(results, args.outfile)
        else:
            print("Unsupported output format. Use .csv or .json.")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
