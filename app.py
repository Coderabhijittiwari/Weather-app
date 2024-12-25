import requests
import pandas as pd
import streamlit as st
from plotly import graph_objects as go

# Fetching data from the API
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from API")
        return None

# Creating a responsive graph
def create_graph(data, x_col, y_col, title):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode="lines+markers",
            line=dict(color="cyan"),
            marker=dict(size=6),
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title=title,
        template="plotly_white",
    )
    return fig

# Main function to render the dashboard
def main():
    # Streamlit layout
    st.set_page_config(layout="wide")
    st.title("Air Quality Monitoring Dashboard")

    # Fetch data
    api_url = "https://api.thingspeak.com/channels/1596152/feeds.json?results=50"
    raw_data = fetch_data(api_url)

    if not raw_data:
        return

    # Extract data into DataFrame
    feeds = raw_data["feeds"]
    df = pd.DataFrame(feeds)
    df["created_at"] = pd.to_datetime(df["created_at"])
    for col in ["field1", "field2", "field3", "field4", "field5", "field6"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Field mapping
    field_mapping = {
        "field1": "PM2.5",
        "field2": "PM10",
        "field3": "Ozone",
        "field4": "Humidity",
        "field5": "Temperature",
        "field6": "CO",
    }

    # Create responsive layout
    cols = st.columns(3)  # Three graphs per row
    graphs = []

    for idx, (field, title) in enumerate(field_mapping.items()):
        graph = create_graph(df, "created_at", field, title)
        graphs.append(graph)
        with cols[idx % 3]:
            st.plotly_chart(graph, use_container_width=True)

if __name__ == "__main__":
    main()
