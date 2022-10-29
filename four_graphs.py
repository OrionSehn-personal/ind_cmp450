#Uses plotly to draw a geographical cloropleth of the UK 


import plotly.graph_objects as go
import pandas as pd
import json
import plotly.express as px
import datetime




def plot_map(df, authorities, column, title):
    '''
    generate a map of the UK with a colour scale based on the values in the column

    :param df: dataframe containing the data to be plotted
    :param authorities: geojson containing the boundaries of the local authorities
    :param column: the column in the dataframe to be plotted
    :param title: the title of the plot
    :return: None

    '''

    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["gender"] == "Total"]
    df = df[df["time_period"] == 202122]

    df = df[df[column] != "c"]
    df = df[df[column] != "x"]
    df[column] = df[column].astype(float)

    fig = px.choropleth_mapbox(
        df,
        geojson=authorities, 
        locations='la_name',
        featureidkey="properties.LAD21NM",
        color_continuous_scale="Blues",
        mapbox_style="carto-positron",
        center={"lat": 55.09621, "lon": -4.0286298},
        zoom=4.8,
        range_color=(0,100),
        labels=None,
        opacity=0.5,
        title=title,
        color=column)

    fig.show()


def demonstrate_data_issues():
    '''
    demonstrate the issues with the data
    shows different entries for local authorities in the geojson and the availible data
    '''
    # Read data from a json
    authorities = json.load(open('Local_Authority_Districts_(December_2021)_GB_BFC.json'))

    # Iterative over JSON

    print("    Norfolk entries in geojson:")
    for i in range(len(authorities["features"])):
        # Extract local authority name
        la = authorities["features"][i]['properties']['LAD21NM']
        if "Norfolk" in la:
            print(la)
        # Assign the local authority name to a new 'id' property for later linking to dataframe
        authorities["features"][i]['id'] = la
        # While I'm at it, append local authority name to a list to make some dummy data to test, along with i for a value to test on map

    # Read data from a csv
    df = pd.read_csv(r'data\ks2_regional_and_local_authority_2016_to_2022_provisional.csv', dtype={'la_name': str})

    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["gender"] == "Total"]
    df = df[df["time_period"] == 202122]

    print("\n    Norfolk entries in dataset:")

    for i in range(len(df)):
        la = df.iloc[i]['la_name']
        if "Norfolk" in la:
            print(la)


def plot_maps(df, authorities, column, title):
    '''
    generate a map of the UK with a colour scale based on the values in the column

    :param df: dataframe containing the data to be plotted
    :param authorities: geojson containing the boundaries of the local authorities
    :param column: the column in the dataframe to be plotted
    :param title: the title of the plot
    :return: None

    '''

    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["gender"] == "Total"]
    df = df[df[column] != "c"]
    df = df[df[column] != "x"]
    df[column] = df[column].astype(float)

    # dates = [201516, 201617, 201718, 201819, 201920, 202021, 202122]

    
    dates = [202122]

    for date in dates:
        
        sdf = df[df["time_period"] == date]


        fig = px.choropleth_mapbox(
            sdf,
            geojson=authorities,
            locations='la_name',
            featureidkey="properties.CTYUA21NM",
            color_continuous_scale="Hot_r",
            mapbox_style="carto-positron",
            center={"lat": 53, "lon": -1.5},
            zoom=5.5,
            range_color=(55,90),
            labels=None,
            opacity=0.5,
            title=title +str(date),
            color=column)

        fig.show()


def plot_scatter(df):
    '''
    generate a scatter plot comparing the number of students who achieved expected standard in reading,
     to the number of students who achived expected standard in maths.
    '''

    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["gender"] == "Total"]
    df = df[df["time_period"] == 202122]

    df = df[df["t_read_met_expected_standard"] != "c"]
    df = df[df["t_read_met_expected_standard"] != "x"]
    df["t_read_met_expected_standard"] = df["t_read_met_expected_standard"].astype(float)

    df = df[df["t_mat_met_expected_standard"] != "c"]
    df = df[df["t_mat_met_expected_standard"] != "x"]
    df["t_mat_met_expected_standard"] = df["t_mat_met_expected_standard"].astype(float)

    
    fig = px.scatter(df, x="t_read_met_expected_standard", y="t_mat_met_expected_standard", hover_data=["la_name"], title="Reading Skills and Math Skills are Strongly Correlated (2021/2022)", labels={"t_read_met_expected_standard":"Number of pupils meeting the expected standard in reading", "t_mat_met_expected_standard": "Number of pupils meeting the expected standard in maths"})
    fig.show()


def plot_bar(df):
    '''
    plot a bar chart of the number of students who achieved expected standard in reading and maths by gender
    '''
    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["time_period"] == 202122]

    # print(px.data.tips())
    # df_boys = df[df["gender"] == "Boys"]
    # df_girls = df[df["gender"] == "Girls"]

    # focus_df = df["gender", "pt_read_met_expected_standard", "pt_mat_met_expected_standard"]
    # average
    
    df = df[df["t_read_met_expected_standard"] != "c"]
    df = df[df["t_read_met_expected_standard"] != "x"]
    df["t_read_met_expected_standard"] = df["t_read_met_expected_standard"].astype(float)

    df = df[df["t_mat_met_expected_standard"] != "c"]
    df = df[df["t_mat_met_expected_standard"] != "x"]
    df["t_mat_met_expected_standard"] = df["t_mat_met_expected_standard"].astype(float)

    df["Number of pupils meeting the expected standard in reading"] = df["t_read_met_expected_standard"].astype(float)
    df["Number of pupils meeting the expected standard in maths"] = df["t_mat_met_expected_standard"].astype(float)
    
    fig = px.histogram(df, x="gender", y=["Number of pupils meeting the expected standard in reading", "Number of pupils meeting the expected standard in maths"], barmode="group", title="There are more girls who meet expected standards in reading than boys, and vice verca for maths. (2021/2022)")
    fig.show()


def plot_line(df):
    '''
    plot a line chart of the number of students who achieved expected standard in maths over time
    '''
    df = df[df["geographic_level"] == "Local authority"]

    df = df[df["t_mat_met_expected_standard"] != "c"]
    df = df[df["t_mat_met_expected_standard"] != "x"]
    df["t_mat_met_expected_standard"] = df["t_mat_met_expected_standard"].astype(float)


    data = df.groupby("time_period", as_index = False)["t_mat_met_expected_standard"].sum()
    data = pd.DataFrame(data)
    formatted_years = []
    for year in data["time_period"]:
        formatted_years.append(datetime.datetime(int(str(year)[0:4]) +1, 1, 1))
    print(formatted_years)

    data["time_period"] = pd.Series(formatted_years)
    
    fig = px.line(data, x="time_period", y="t_mat_met_expected_standard", title="The number of students who achieved expected standard in maths had been increasing over time until 2020.", labels={"time_period":"Year", "t_mat_met_expected_standard": "Number of pupils meeting the expected standard in maths"})
    # fig = px.line(data, x=data.index, y=data.values, title="The number of students who achieved expected standard in maths has increased over time. (2016/2017 - 2021/2022)")

    fig.show()



def plot_line2(df):
    '''
    plot a line chart of the number of students who achieved expected standard in maths over time
    '''
    df = df[df["geographic_level"] == "Local authority"]

    df = df[df["t_mat_met_expected_standard"] != "c"]
    df = df[df["t_mat_met_expected_standard"] != "x"]

    df = df[df["t_mat_met_higher_standard"] != "c"]
    df = df[df["t_mat_met_higher_standard"] != "x"]

    df = df[df["t_mat_eligible_pupils"] != "c"]
    df = df[df["t_mat_eligible_pupils"] != "x"]

    df["t_mat_met_expected_standard"] = df["t_mat_met_expected_standard"].astype(float)
    df["t_mat_met_higher_standard"] = df["t_mat_met_higher_standard"].astype(float)
    df["t_mat_eligible_pupils"] = df["t_mat_eligible_pupils"].astype(float)

    data = df.groupby("time_period", as_index = False).sum()
    data = pd.DataFrame(data)

    data["pt_mat_met_expected_standard"] = 100 * data["t_mat_met_expected_standard"] / data["t_mat_eligible_pupils"]
    data["pt_mat_met_higher_standard"] = 100 * data["t_mat_met_higher_standard"] / data["t_mat_eligible_pupils"]

    formatted_years = []
    for year in data["time_period"]:
        formatted_years.append(datetime.datetime(int(str(year)[0:4]) +1, 1, 1))
    data["time_period"] = pd.Series(formatted_years)
    print(data)    
    fig = px.line(data, x="time_period", y=["pt_mat_met_expected_standard", "pt_mat_met_higher_standard"], title="Success of Students was on the rise until 2020", labels={"time_period":"Year", "t_mat_met_expected_standard": "Number of pupils meeting the expected standard in maths"})
    
    colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    fig.add_trace(go.Scatter(
        x=[data["time_period"][0], data["time_period"][4], data["time_period"][0], data["time_period"][4]],
        y=[data["pt_mat_met_higher_standard"][0], data["pt_mat_met_higher_standard"][4], data["pt_mat_met_expected_standard"][0], data["pt_mat_met_expected_standard"][4]],
        mode='markers',
        marker=dict(color=colors[0], size=8)
    ))

    
    fig.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=20,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    # autosize=False,
    # margin=dict(
    #     autoexpand=False,
    #     l=100,
    #     r=20,
    #     t=110,
    # ),
    # showlegend=False,
    plot_bgcolor='white'
)








    
    
    
    # fig.update_layout(margin = dict(t=10,l=10,b=10,r=10))
    # fig = px.line(data, x=data.index, y=data.values, title="The number of students who achieved expected standard in maths has increased over time. (2016/2017 - 2021/2022)")

    fig.show()


def horizontal_total_students(df):
    '''
    Plot a horizontal bar chart of the number of students who achieved expected standard in maths in each local authority
    '''
    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["time_period"] == 201516]
    df = df[df["pt_mat_met_expected_standard"] != "c"]
    df = df[df["pt_mat_met_expected_standard"] != "x"]
    df = df[df["gender"] == "Total"]
    df["pt_mat_met_expected_standard"] = df["pt_mat_met_expected_standard"].astype(float)
    # df = df.head()
    df = df.sort_values(by="pt_mat_met_expected_standard", ascending=True)
    print(df)
    print(list(df["pt_mat_met_expected_standard"]))
    # df.to_csv("test.csv")
    fig = px.bar(df, x="pt_mat_met_expected_standard", y="la_name", orientation='h', title="The number of students who achieved expected standard in maths in each local authority", width=1000, height=800, labels={"pt_mat_met_expected_standard":"Percentage of pupils meeting the expected standard in maths", "la_name": "Local Authority"})
    #make the graph less wide


    fig.show()





if __name__ == "__main__":


    authorities = json.load(open('Counties_and_Unitary_Authorities_(December_2021)_UK_BGC.geojson'))

    # Iterative over JSON
    for i in range(len(authorities["features"])):
        # Extract local authority name
        la = authorities["features"][i]['properties']['CTYUA21NM']
        # Assign the local authority name to a new 'id' property for later linking to dataframe
        authorities["features"][i]['id'] = la




    # Read data from a csv
    df = pd.read_csv(r'data\ks2_regional_and_local_authority_2016_to_2022_provisional.csv', dtype={'la_name': str})

    # plot_map(df, authorities, "pt_mat_met_expected_standard", "Percentage of pupils meeting the expected standard in maths (2021/2022)")
    # plot_map(df, authorities, "pt_mat_met_higher_standard", "Percentage of pupils reaching the higher standard in maths test  (2021/2022)")
    # plot_map(df, authorities, "pt_read_met_expected_standard", "Percentage of pupils meeting the expected standard in reading")
    # plot_map(df, authorities, "pt_read_met_higher_standard", "Percentage of pupils reaching the higher standard in reading test")

    plot_maps(df, authorities, "pt_read_met_expected_standard", "Percentage of pupils reaching the higher standard in maths test ")

    # horizontal_total_students(df)
    
    # plot_scatter(df)

    # plot_bar(df)

    # plot_line2(df)





