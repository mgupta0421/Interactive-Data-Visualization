import parser


def worldMap(region=None):
    data = parser.get_stringency_index_data_per_date()
    data_slider = []
    removedates = []
    datelist = data['dates']
    for i, date in enumerate(datelist):
        if all(value is None for value in data['index_values'][i]):
            removedates.append(date)
        else:
            data_each_day = dict(
                visible=False,
                type='choropleth',
                locations=data['countries'],
                z=data['index_values'][i],
                text=[date.strftime('%d. %B %Y')] * len(data['countries']),
                colorbar={'title': 'Stringency Index'},
                zmin=0,
                zmax=100
             )
            data_slider.append(data_each_day)
    date_list = [element for element in datelist if element not in removedates]
    steps = []
    data_slider[len(data_slider)-1]['visible'] = True
    for i in range(len(data_slider)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data_slider)], label=f'{date_list[i].strftime("%d. %B %Y")}')
        step['args'][1][i] = True
        steps.append(step)
    sliders = [dict(active=len(data_slider)-1, steps=steps)]
    layout = dict(title='Government Response Stringency Index', geo=dict(projection_type='equirectangular', scope=region),
                  sliders=sliders, width=1400, height=630, clickmode = 'event')
    fig = dict(data=data_slider, layout=layout)
    return fig
