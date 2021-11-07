from orbit import load_asteroids, calc_position
from utils import build_timestamps, process_dataframe

if __name__ == '__main__':
    # Init df
    print(f"Initializing data...")
    asteroids_df = load_asteroids('asteroids_20210917.json')

    # User input
    selection = None
    while not selection:
        input_val = input("Select asteroid ID to query, default=104: ")
        try:
            if not input_val:
                selection = 104
            else:
                selection = int(input_val)
        except ValueError:
            print(f"{input_val} is not a valid number, please enter an asteroid ID.")
    print(f"You selected {selection}, continuing...")

    year_amount = None
    while not year_amount:
        input_val = input("Select amount of years to calculate for, default=5 "
                          "(*warning, the more years the longer the calculation takes!): ")
        try:
            if not input_val:
                year_amount = 5
            else:
                year_amount = int(input_val)
        except ValueError:
            print(f"{input_val} is not a valid number, please enter an asteroid ID.")
    print(f"You selected {year_amount} years, continuing...")

    # Filter out selected asteroid
    homebase = asteroids_df.loc[selection]
    asteroids_df = asteroids_df.drop(selection)

    # Get a range of adalia days for the period of a year
    print(f"Building timestamps...")
    timestamps, adalia_day_interval = build_timestamps(year_amount)

    # Calculate distance for each adalia day interval
    print(f"Starting calculations...")
    f = open(f"distance_from_{selection}.csv", 'w')
    f.write(f"id,avg_dist,max_dist,min_dist")
    home_orbital = homebase['orbital']
    home_base_positions = [calc_position(home_orbital, adalia_day) for adalia_day in adalia_day_interval]

    # Process
    process_dataframe(asteroids_df, selection, adalia_day_interval, home_base_positions)
    print(f"Processing finished!")
