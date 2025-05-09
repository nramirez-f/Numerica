import os
import xarray as xr
import plotly.graph_objects as go

class NcView:

    def __init__(self, ncf_path):
        """
        Load NetCDF file from given path
        """
        full_path = os.path.abspath(ncf_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File {full_path} not found.")
        
        try:
            self.data = xr.open_dataset(full_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load NetCDF file: {e}")
        
        print(f"Loaded: {full_path}")

    ## 1D ##
    def point(self, dimPos: int, iterPos: int, varName: str = 'u',dimName: str = 'x', iterName: str = 't'):
        """
        Plot the value of varName in dimPos of dimName at iterVal of iterName
        """
        x_data = self.data[dimName].isel({dimName: dimPos}).values
        y_data = self.data[varName].isel({dimName: dimPos, iterName: iterPos}).values

        fig = go.Figure(
            data=go.Scatter(
                x=x_data,
                y=y_data,
                mode='markers',
            )
        )

        fig.show()

    def scatter(self,  iterPos: int, varName: str, dimName: str, iterName: str, line_mode: str):
        """
        Creates a Scatter plot for the given varName at iterPos.
        """
        x_data = self.data[dimName].values
        y_data = self.data[varName].isel({iterName: iterPos}).values

        # Choose default line mode
        if line_mode not in ['lines', 'lines+markers', 'markers']:
            line_mode = 'markers'

        # Default marker dict
        default_marker_dict = dict( size=3,
                                    symbol='circle')

        scatter = go.Scatter(
            x=x_data,
            y=y_data,
            mode=line_mode,
            marker=default_marker_dict,
            name=varName,
        )

        return scatter

    def frame(self,  iterPos: int, varName: str = 'u', dimName: str = 'x', iterName: str = 't', line_mode: str = 'markers'):
        """
        Frame of varName at iterPos
        """
        fig = go.Figure()

        fig.add_trace(self.scatter(iterPos, varName, dimName, iterName, line_mode))

        fig.update_layout(showlegend=True)

        fig.show()

    def evolution(self, iterPosInit: int, varName: str = 'u', dimName: str = 'x', iterName: str = 't', line_mode: str = 'markers'):
        """
        Evolution plot from iterInit to the end of iterDomain.
        """
        iterDomain = self.data[iterName].values.tolist()[iterPosInit:]

        fig = go.Figure(data=[self.scatter(iterPosInit, varName, dimName, iterName, line_mode)])

        frames = [
            go.Frame(
                data=[self.scatter((iterPosInit + iterPosRel), varName, dimName, iterName, line_mode)],
                name=str(iterValue)
            )
            for iterPosRel, iterValue in enumerate(iterDomain)
        ]

        fig.update(frames=frames)

        eps_y = 0.1
        fig.update_layout(
            yaxis=dict(
                range=[self.data[varName].min().values - eps_y, self.data[varName].max().values + eps_y],
                title=dict(text=varName),
            ),
            xaxis=dict(
                range=[self.data[dimName].values[0], self.data[dimName].values[-1]],
                title=dict(text=dimName),
            )
        )

        # Legend
        fig.update_layout(
            showlegend=True
        )

        # Responsive
        fig.update_layout(
            autosize=True,
            margin=dict(l=40, r=40, t=40, b=40),
        )

        # Buttons
        fig.update_layout(
            updatemenus=[{
                "buttons": [
                    {
                        "label": "▶",
                        "method": "animate",
                        "args": [None, {
                            "frame": {"duration": 100, "redraw": False},
                            "mode": "immediate",
                            "fromcurrent": True,
                            "transition": {"duration": 0}
                        }],
                    },
                    {
                        "label": "❚❚",
                        "method": "animate",
                        "args": [[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }],
                    }
                ],
                "x": 0.05,
                "y": -0.07,
                "type": "buttons",
                "direction": "left",
            }]
        )

        # Slider
        fig.update_layout(
            sliders=[{
                "steps": [
                    {
                        "args": [[str(iterValue)], {
                            "mode": "immediate",
                            "fromcurrent": True,
                            "frame": {"duration": 0, "redraw": False},
                            "transition": {"duration": 0}
                        }],
                        "label": str(iterValue),
                        "method": "animate"
                    }
                    for iterValue in iterDomain
                ],
                "x": 0.06,
                "y": 0,
                "len": 0.92,
            }],
            annotations=[
                {
                    "text": iterName,
                    "showarrow": False,
                    "x": 1,
                    "y": -0.125,
                    "xref": "paper",
                    "yref": "paper",
                    "font": {"size": 14}
                }
            ]
        )


        fig.show()

