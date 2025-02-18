from flask import request
from app.services.response import *
from app.services.models.part_model import *
from app.services.models.envelope_model import *
from datetime import datetime, timedelta
from app.config.config import Config
from requests.auth import HTTPBasicAuth
import pandas as pd
import math
import pytz
import urllib3
import requests
import numpy as np


def index():
    try:
        current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
        print(f"Task running at: {current_time}")

        config = Config()
        parts = get_parts()
        print(f"Processing total: {len(parts)} parts")

        for part in parts:
            try:
                if part[2] == None:
                    continue

                print(
                    f"Processing part: {part[3]}"
                )  # Assuming part[3] contains part name

                data = fetch(
                    config.PIWEB_API_USER,
                    config.PIWEB_API_PASS,
                    config.PIWEB_API_URL,
                    part[1],
                )

                print(f"Data: {data}")

                if not data.empty:
                    create_envelope(data, part[0])
                    print(f"Successfully processed part {part[3]}")
                else:
                    print(f"No data retrieved for part {part[3]}")

            except Exception as e:
                print(f"Error processing part {part[3]}: {e}")
                continue

        print(f"Task completed at: {datetime.now(pytz.timezone('Asia/Jakarta'))}")

    except Exception as e:
        print(f"Error executing task: {e}")


def fetch(username: str, password: str, host: str, web_id: str) -> pd.DataFrame:
    """
    Fetch data from PI Web API for the current hour

    Args:
        username (str): API username
        password (str): API password
        host (str): Base API URL
        web_id (str): Web ID for the data stream

    Returns:
        pd.DataFrame: DataFrame containing fetched data
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Setup session
    session = requests.Session()
    auth = HTTPBasicAuth(username, password)

    # Get current time and calculate time range for this hour
    current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
    start_time = current_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    # Format the timestamp
    timestamp = start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    try:
        # Make single API call for the hour
        url = f"{host}/streams/{web_id}/value?time={timestamp}"
        response = session.get(url, auth=auth, verify=False)
        response.raise_for_status()

        data = response.json()

        # Process the response
        signal_value = data["Value"]
        if isinstance(signal_value, dict):
            signal_value = signal_value.get("Value", 0)

        if isinstance(signal_value, (int, float)) and (
            math.isnan(signal_value) or math.isinf(signal_value)
        ):
            signal_value = 0

        # Create DataFrame with single record
        df = pd.DataFrame(
            [
                {
                    "datetime": pd.to_datetime(format_to_gmt(data["Timestamp"][:19])),
                    "signal": float(signal_value) if signal_value is not None else 0,
                }
            ]
        )

        print(f"Fetched data for {timestamp} - Web ID: {web_id}")
        return df

    except Exception as e:
        print(f"Error fetching data for {web_id} at {timestamp}: {e}")
        return pd.DataFrame()


def feature():
    # Mendapatkan timestamp untuk awal hari kemarin (00:00:00)
    yesterday_start = (datetime.now() - timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # Mendapatkan timestamp untuk akhir hari kemarin (23:59:59)
    yesterday_end = yesterday_start + timedelta(days=1) - timedelta(seconds=1)
    print(yesterday_start)
    print(yesterday_end)

    parts = get_parts()
    print(f"processing feature for {len(parts)}")

    for part in parts:
        print(f"processing feature for {part[3]}")

        data = get_envelope_values_by_date(
            part[0], start_date=yesterday_start, end_date=yesterday_end
        )
        df = pd.DataFrame(data, columns=["value", "datetime"])
        signal_values = df["value"].values
        min_indices, max_indices = find_signal_envelopes(signal_values)

        print(f"Found {len(max_indices)} maxima")
        save_envelopes_to_db(
            part[0], df, max_indices, features_id="9dcb7e40-ada7-43eb-baf4-2ed584233de7"
        )
        # predict_detail(part[0])

    print(
        f"Task feature high env completed at: {datetime.now(pytz.timezone('Asia/Jakarta'))}"
    )


def format_to_gmt(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    local_tz = pytz.timezone("Asia/Jakarta")
    local_date = local_tz.localize(date)

    updated_date = local_date + timedelta(hours=7)

    return updated_date.strftime("%Y-%m-%dT%H:%M:%SZ")


def find_signal_envelopes(signal, chunk_size=1, split_at_mean=False):
    """
    Find high and low envelopes of a signal.
    """
    diff_signal = np.diff(np.sign(np.diff(signal)))
    min_indices = np.nonzero(diff_signal > 0)[0] + 1
    max_indices = np.nonzero(diff_signal < 0)[0] + 1

    if split_at_mean:
        signal_mean = np.mean(signal)
        min_indices = min_indices[signal[min_indices] < signal_mean]
        max_indices = max_indices[signal[max_indices] > signal_mean]

    min_indices = min_indices[
        [
            i + np.argmin(signal[min_indices[i : i + chunk_size]])
            for i in range(0, len(min_indices), chunk_size)
        ]
    ]
    max_indices = max_indices[
        [
            i + np.argmax(signal[max_indices[i : i + chunk_size]])
            for i in range(0, len(max_indices), chunk_size)
        ]
    ]

    return min_indices, max_indices
