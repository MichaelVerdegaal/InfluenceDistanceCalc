import numpy as np
import pandas as pd
import pendulum

from orbit import euclidian, calc_position, get_adalia_day_at_time


def build_timestamps(years: int):
    """
    Generates a range of timestamps
    :param years: amount of years to calculate for
    :return: list of timestamps, list of adalia days
    """
    current_timestamp = pendulum.now()
    timestamps = []
    adalia_day_interval = []

    for i in range(365 * years):
        current_timestamp = current_timestamp.add(days=1)
        timestamps.append(current_timestamp.to_datetime_string())
        adalia_day = get_adalia_day_at_time(current_timestamp.to_datetime_string())
        adalia_day_interval.append(adalia_day)
    return timestamps, adalia_day_interval


def process_dataframe(df: pd.DataFrame, selection: int, adalia_day_interval: list, home_base_positions: list):
    """
    Calculates relative distance for each combination
    :param df: dataframe with asteroids
    :param selection: selected asteroid
    :param adalia_day_interval: range of adalia days to calculate at
    :param home_base_positions: calculated positions of the selection, this is done only once to save speed
    """

    def helper(row):
        print(f"Calculating results for asteroid {row['i']}")
        row_orbital = row['orbital']
        distances = []
        for j, adalia_day in enumerate(adalia_day_interval):
            x1 = home_base_positions[j]
            x2 = calc_position(row_orbital, adalia_day)
            distances.append(euclidian(x1, x2))
        f.write(f"\n{row['i']}, {np.mean(distances)}, {np.max(distances)}, {np.min(distances)}")

    f = open(f"distance_from_{selection}.csv", 'w')
    [helper(row) for i, row in df.iterrows()]
    f.close()
