import pandas as pd
import numpy as np


def detect_network_anomaly(df, column_name, window_size=3, threshold_factor=2):
    """
    Detects anomalies in network data using a rolling average and standard deviation.

    Args:
        df: Pandas DataFrame containing the network data.
        column_name: Name of the column containing the network data (e.g., 'traffic', 'requests').
        window_size: Size of the rolling window for calculating average and standard deviation.
        threshold_factor: Factor by which standard deviation is multiplied to define the threshold.

    Returns:
        DataFrame with added columns: 'rolling_mean', 'rolling_std', 'upper_threshold', 'lower_threshold', 'anomaly'
        and boolean Series indicating anomalies.  Returns the original DataFrame if the column_name isn't found.
    """

    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in DataFrame.")
        return df

    df["rolling_mean"] = (
        df[column_name].rolling(window=window_size, center=True).mean()
    )  # Centered rolling average
    df["rolling_std"] = df[column_name].rolling(window=window_size, center=True).std()

    df["upper_threshold"] = df["rolling_mean"] + threshold_factor * df["rolling_std"]
    df["lower_threshold"] = df["rolling_mean"] - threshold_factor * df["rolling_std"]

    df["anomaly"] = (df[column_name] > df["upper_threshold"]) | (
        df[column_name] < df["lower_threshold"]
    )

    return df, df["anomaly"]


# Example usage:
data = {
    "timestamp": pd.to_datetime(
        [
            "2024-07-26 10:00:00",
            "2024-07-26 10:05:00",
            "2024-07-26 10:10:00",
            "2024-07-26 10:15:00",
            "2024-07-26 10:20:00",
            "2024-07-26 10:25:00",
            "2024-07-26 10:30:00",
            "2024-07-26 10:35:00",
            "2024-07-26 10:40:00",
            "2024-07-26 10:45:00",
            "2024-07-26 10:50:00",
        ]
    ),
    "traffic": [100, 105, 110, 102, 108, 115, 2200, 115, 2200, 115, 115],
}  # Example network traffic data

df = pd.DataFrame(data)

df, anomalies = detect_network_anomaly(
    df, "traffic", window_size=3, threshold_factor=2
)  # Adjust window_size and threshold_factor

print(df)
print("\nAnomalies:")
print(anomalies)

# To get only the anomalous data points:
anomalous_data = df[df["anomaly"]]
print("\nAnomalous Data Points:")
print(anomalous_data)


# Plotting (requires matplotlib)
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["traffic"], label="Traffic")
plt.plot(df["timestamp"], df["rolling_mean"], label="Rolling Mean")
plt.plot(
    df["timestamp"], df["upper_threshold"], label="Upper Threshold", linestyle="--"
)
plt.plot(
    df["timestamp"], df["lower_threshold"], label="Lower Threshold", linestyle="--"
)
plt.scatter(
    df[df["anomaly"]]["timestamp"],
    df[df["anomaly"]]["traffic"],
    color="red",
    label="Anomalies",
)  # Highlight anomalies
plt.xlabel("Timestamp")
plt.ylabel("Traffic")
plt.title("Network Traffic Anomaly Detection")
plt.legend()
plt.grid(True)
plt.show()
