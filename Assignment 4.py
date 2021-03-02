import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# read csv into dataframe df
df = pd.read_csv('DataWeierstrass.csv', sep=';')

# converting professor and lecture String value into Int values.
df['professor'] = df['professor'].str.replace('([a-z]+)', '')
df['professor'] = df['professor'].str.lstrip('0')
df['professor'] = df['professor'] .astype('int')
df['lecture'] = df['lecture'].str.replace('([a-z]+)', '')
df['lecture'] = df['lecture'].str.lstrip('0')
df['lecture'] = df['lecture'] .astype('int')

# a) Scatterplot Matrix for Best Professor
sm = px.scatter_matrix(df,dimensions=['professor','lecture', 'participants','professional expertise', 'motivation','clear presentation','overall impression'],
                       color="professor")
sm.update_layout(title="Scatter Plot Matrix for Best professor",width=1150,height=1150)
sm.update_traces(diagonal_visible=False)
sm.show()

# b) Parallel coordinates for Best Professor
import plotly.graph_objects as go

pc = go.Figure(data=go.Parcoords(line = dict(color = df['professor'],colorscale = 'balance',showscale = True,),
        dimensions = list([
            dict(label = "Professor", values = df['professor']),
            dict(label = 'Lecture', values = df['lecture']),
            dict(label = 'Participants', values = df['participants']),
            dict(range = [6,1],label = 'Professional Expertise', values = df['professional expertise']),
            dict(range = [6,1],label = 'Motivation', values = df['motivation']),
            dict(range = [6,1],label = 'Clear Presentation', values = df['clear presentation']),
            dict(range = [6,1],label = 'Overall Impression', values = df['overall impression'])])))
pc.update_layout(title="Parallel Coordinates for Best Professor")
pc.show()
