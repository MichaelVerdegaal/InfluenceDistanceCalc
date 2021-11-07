import numpy as np
import pendulum

from orbit import euclidian, calc_position, get_adalia_day_at_time


def build_timestamps(years):
    current_timestamp = pendulum.now()
    timestamps = []
    adalia_day_interval = []

    for i in range(365 * years):
        current_timestamp = current_timestamp.add(days=1)
        timestamps.append(current_timestamp.to_datetime_string())
        adalia_day = get_adalia_day_at_time(current_timestamp.to_datetime_string())
        adalia_day_interval.append(adalia_day)
    return timestamps, adalia_day_interval


def process_dataframe(df, selection, adalia_day_interval, home_base_positions):
    f = open(f"distance_from_{selection}.csv", 'w')
    for i, row in df.iterrows():
        print(f"Calculating results for asteroid {row['i']}")
        row_orbital = row['orbital']
        distances = []
        for adalia_day in adalia_day_interval:
            x1 = home_base_positions[i]
            x2 = calc_position(row_orbital, adalia_day)
            distances.append(euclidian(x1, x2))
        f.write('\n')
        f.write(f"{row['i']}, {np.average(distances)}, {np.max(distances)}, {np.min(distances)}")
    f.close()
