import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import parser


def plotFun(selectionList=None, country_code=None):
    country_name = ''
    data = parser.get_policy_data(country_code)
    name=parser.get_countries()
    for code,countryname in name.items():
        if code==country_code:
            country_name=countryname
    dates = [d.isoformat() for d in data['dates']]
    start = dates[0]
    end = dates[-1]

    lineplot = go.Scatter(x=dates, y=data['new deaths'], mode='lines', yaxis='y2',
                          line=dict(color='green', width=3), name='New Deaths')
    lineplot1 = go.Scatter(x=dates, y=data['new cases'], mode='lines', yaxis='y2',
                           line=dict(color='cyan', width=3), name='New Cases')
    lineplot2 = go.Scatter(x=dates, y=data['total deaths'], mode='lines', yaxis='y2',
                           line=dict(color='red', width=3), name='Total Deaths')
    lineplot3 = go.Scatter(x=dates, y=data['total cases'], mode='lines', yaxis='y2',
                           line=dict(color='blue', width=3), name='Total Cases')

    multi = go.Figure()

    multi.add_trace(go.Scatter(
        x=dates,
        y=data['new deaths'],
        name='New Deaths',  # Style name/legend entry with html tags
        connectgaps=True  # override default to connect the gaps
    ))
    multi.add_trace(go.Scatter(
        x=dates,
        y=data['new cases'],
        name='New Cases',
    ))
    layout = go.Layout(title=dict(text='Strictness Level on Lockdown Policies for '+ country_name,x=0.5,y=0.9),
                       xaxis=dict(title='Date', tickformat = '%B-%d',rangeselector=dict(buttons=list([dict(count=1,
                                                                                      label="Month", step="month",
                                                                                      stepmode="backward"),
                                                                                 dict(step="all", label="All")])),
                                  rangeslider=dict(visible=True, thickness=0.09, autorange=True, bordercolor='blue'),
                                  type="date"))
    policy = data['policy_names']
    policyvalues=pd.DataFrame(data['policy_values'])
    policyvalues=policyvalues.transpose()
    policyvalues.columns=policy
    if selectionList:
        policyvalues = policyvalues[[col for col in policyvalues.columns if col in selectionList]]
        policyvalues = policyvalues.fillna(method='ffill')
        policyvalues = policyvalues.fillna(method='bfill')
        policyvalues = policyvalues.transpose()
        heatmap = go.Heatmap(z=policyvalues, x=dates, y=policyvalues.index, xgap=0, ygap=1,
                             hovertemplate='Date: %{x}<br>Policy: %{y}<br>Strictness: %{z}', hoverongaps=True,
                             colorscale=px.colors.sequential.Oryel, yaxis='y1',
                             colorbar=dict(nticks=5, dtick=1, tick0=0, x=-0.2,
                                           title=dict(text='|--------------Strictness Level-------------->', side="right",
                                                      font=dict(size=14))), name="strictness")
        fig = go.Figure(data=[heatmap, lineplot, lineplot1, lineplot2, lineplot3], layout=layout)
        fig.update_layout(yaxis1=dict(title='Policy Restrictions', side='right'))
        fig.update_layout(yaxis2=dict(title='Count', overlaying='y', side='left'))

    else:
        fig = go.Figure(data=[lineplot, lineplot1, lineplot2, lineplot3], layout=layout)
        fig.update_layout(yaxis2=dict(title='Count', overlaying='y', side='left'))


    fig.update_layout(xaxis=dict(range=[start, end]), width=1500, height=600, margin=dict(pad=5))
    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )
    # format x-axis ticks
    fig.update_layout(xaxis_tickformat='%d %B (%a)<br>%Y')
    fig.update_xaxes(
        showgrid=True,
        ticks="outside",
        tickson="boundaries",
        ticklen=5
    )
    # format y-axis ticks
    fig.update_yaxes(
        showgrid=True,
        ticks="outside",
        tickson="boundaries",
        ticklen=5
    )
    return fig


if __name__ == '__main__':
    plotFun()
