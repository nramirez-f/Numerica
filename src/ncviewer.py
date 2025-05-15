import os
import xarray as xr
import plotly.graph_objects as go

def _scatter(ncfile_path,  iterPos: int, varName: str, dimName: str, iterName: str, line_mode: str = 'markers', line_color:str = 'black', line_width: int = 1, scatterName: str = ""):
        """
        Creates a Scatter plot for the given varName at iterPos.
        """
        full_path = os.path.abspath(ncfile_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File {full_path} not found.")
        
        try:
            ncf = xr.open_dataset(full_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load NetCDF file: {e}")

        x_data = ncf[dimName].values
        y_data = ncf[varName].isel({iterName: iterPos}).values

        # Choose default line mode
        if line_mode not in ['lines', 'lines+markers', 'markers']:
            line_mode = 'markers'

        # Default marker dict
        default_marker_dict = dict(size=3,
                                    symbol='circle')

        scatter = go.Scatter(
            x=x_data,
            y=y_data,
            mode=line_mode,
            line=dict(color=line_color, width=line_width),
            marker=default_marker_dict,
            name=f"{varName} ({ncfile_path})" if scatterName == "" else scatterName,
        )

        return scatter


class NcView:

    def __init__(self, ncfile_path):
        """
        Load NetCDF file from given path
        """
        full_path = os.path.abspath(ncfile_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File {full_path} not found.")
        
        try:
            self.data = xr.open_dataset(full_path)
            self.path = full_path
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

    def scatter(self,  iterPos: int, varName: str, dimName: str, iterName: str, line_mode: str, line_color: str = 'black', line_width: int = 1, scatterName: str = ""):
        """
        Creates a Scatter plot for the given varName at iterPos.
        """
        x_data = self.data[dimName].values
        y_data = self.data[varName].isel({iterName: iterPos}).values

        # Choose default line mode
        if line_mode not in ['lines', 'lines+markers', 'markers']:
            line_mode = 'markers'

        # Default marker dict
        default_marker_dict = dict(size=3,
                                    symbol='circle')

        scatter = go.Scatter(
            x=x_data,
            y=y_data,
            mode=line_mode,
            line=dict(color=line_color, width=line_width),
            marker=default_marker_dict,
            name=varName if scatterName == "" else scatterName,
        )

        return scatter

    def frame(self,  iterPos: int, dimMin: float, dimMax: float, varName: str = 'u', dimName: str = 'x', iterName: str = 't', line_mode: str = 'markers', line_color: str = 'black', line_width: int = 1 ,details: bool = True, show: bool = True):
        """
        Frame of varName at iterPos
        """
        fig = go.Figure()

        fig.add_trace(self.scatter(iterPos, varName, dimName, iterName, line_mode, line_color, line_width))


        iter_value = self.data[iterName].values.tolist()[iterPos]

        time_annotation = dict(
            text=f"{iterName} = {iter_value}",
            x=0.5,
            y=-0.1,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=20),
            align="center",
        )

        figure_annotations = [time_annotation]
        menu_buttons = []

        if details:
            details_annotation = dict(
                text=(
                    f"<b>Author:</b> {self.data.attrs.get('author')}<br>"
                    f"<b>Institution:</b> {self.data.attrs.get('institution')}<br>"
                    f"<b>Source:</b> <a href={self.data.attrs.get('source')}>{self.data.attrs.get('source')}</a><br>"
                    f"<b>References:</b> {self.data.attrs.get('references')}<br>"
                    f"<b>Description:</b> {self.data.attrs.get('description')}<br>"
                ),
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16),
                align="left",
                bgcolor="white",
                bordercolor="black",
                borderwidth=1,
                visible=False,
                name="info-popup"
            )
            figure_annotations.append(details_annotation)

            detail_button = dict(   type="buttons",
                                    showactive=True,
                                    direction="right",
                                    buttons=[
                                        dict(
                                            label="Details",
                                            method="relayout",
                                            args=[{"annotations[1].visible": False}],
                                            args2=[{"annotations[1].visible": True}]
                                        )
                                    ],
                                    x=-0.02,
                                    y=1
                                ) 
            menu_buttons.append(detail_button)

        fig.update_layout(
            title=dict(text=self.data.attrs.get("title"), font_size=24, x=0.5),
            showlegend=True,
            annotations=figure_annotations,
            updatemenus=menu_buttons,
            xaxis=dict(range=[dimMin, dimMax]),
        )

        if show:
            fig.show()

        return fig
    
    def frameComparison(self,  iterPos: int, dimMin: float, dimMax: float, framesList: list, varName: str = 'u', dimName: str = 'x', iterName: str = 't', line_mode: str = 'markers', line_color: str = 'black', line_width: int = 1 ,details: bool = True):
        """
        Frames comparison beetwen ncfile an the frames includes in the framesList by this object:

        framesList: [
            {   "ncfile_path": 'advection1D-exact.nc',
                "iterPos": 100,
                 "varName": "u",
                "dimName": "x",
                "iterName": "t",
                "varNameInPlot" : "exact",
                "line_mode": "lines", 
                "line_color": "black"},
                ...
        ]
        """
        fig = self.frame(iterPos, dimMin, dimMax, varName, dimName, iterName, line_mode, line_color, line_width, details = False, show = False)

        for frame in framesList:
            fig.add_trace(_scatter(frame["ncfile_path"], frame["iterPos"], frame["varName"], frame["dimName"], frame["iterName"], frame["line_mode"], frame["line_color"], line_width, frame["varNameInPlot"]))


        fig.show()

        return fig

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
            autosize=True,
            showlegend=True,
            margin=dict(l=40, r=40, t=40, b=40),
            title=dict(text=self.data.attrs.get("title"), font_size=24, x=0.5),
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

    def close(self, remove: bool = False):
        self.data.close()
        if remove:
            os.remove(self.path)


