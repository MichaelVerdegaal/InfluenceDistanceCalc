import numpy as np
import pendulum

from orbit import load_asteroids, get_adalia_day_at_time, euclidian, calc_position

if __name__ == '__main__':
    # Init df
    print(f"Initializing data...")
    asteroids_df = load_asteroids('asteroids_20210917.json')
    selection = int(input("Select asteroid ID to query against: "))
    print(f"You selected {selection}, continuing...")
    homebase = asteroids_df.loc[selection]
    asteroids_df = asteroids_df.drop(selection)

    # Get a range of adalia days for the period of a year
    print(f"Building timestamps...")
    current_timestamp = pendulum.now()
    timestamps = []
    adalia_day_interval = []

    for i in range(365 * 5):
        current_timestamp = current_timestamp.add(days=1)
        timestamps.append(current_timestamp.to_datetime_string())
        adalia_day = get_adalia_day_at_time(current_timestamp.to_datetime_string())
        adalia_day_interval.append(adalia_day)

    # Calculate distance for each adalia day interval
    print(f"Starting calculations...")
    f = open(f"distance_from_{selection}.csv", 'w')
    f.write(f"id,avg_dist,max_dist,min_dist")
    home_orbital = homebase['orbital']
    home_base_positions = [calc_position(home_orbital, adalia_day) for adalia_day in adalia_day_interval]

    # Process
    for i, row in asteroids_df.iterrows():
        print(f"Calculating results for asteroid {row['i']}")
        row_orbital = row['orbital']
        distances = []
        for i, adalia_day in enumerate(adalia_day_interval):
            x1 = home_base_positions[i]
            x2 = calc_position(row_orbital, adalia_day)
            distances.append(euclidian(x1, x2))
        f.write('\n')
        f.write(f"{row['i']}, {np.average(distances)}, {np.max(distances)}, {np.min(distances)}")
    print(f"Processing finished!")
