"""
Chart Generator - Creates interactive Plotly charts for the dashboard
Supports multiple chart types with professional styling
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.utils
import plotly
import pandas as pd
import numpy as np
import json

class ChartGenerator:
    """
    Professional chart generation class with Plotly
    """
    
    def __init__(self):
        self.color_schemes = {
            'blues': px.colors.sequential.Blues,
            'greens': px.colors.sequential.Greens,
            'oranges': px.colors.sequential.Oranges,
            'purples': px.colors.sequential.Purples,
            'default': px.colors.qualitative.Set3
        }
        
        self.chart_config = {
            'height': 400,
            'margin': dict(l=40, r=40, t=60, b=40),
            'font_family': 'Inter, sans-serif',
            'font_size': 12,
            'title_font_size': 16,
            'showlegend': True,
            'hovermode': 'x unified'
        }
    
    def create_chart(self, data, dataset_name, chart_type):
        """Create chart based on dataset and chart type"""
        if chart_type == 'line':
            return self._create_line_chart(data, dataset_name)
        elif chart_type == 'bar':
            return self._create_bar_chart(data, dataset_name)
        elif chart_type == 'pie':
            return self._create_pie_chart(data, dataset_name)
        elif chart_type == 'scatter':
            return self._create_scatter_chart(data, dataset_name)
        elif chart_type == 'heatmap':
            return self._create_heatmap(data, dataset_name)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
    
    def _apply_theme(self, fig, title=""):
        """Apply consistent theming to all charts"""
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': self.chart_config['title_font_size'], 'family': self.chart_config['font_family']}
            },
            font={'family': self.chart_config['font_family'], 'size': self.chart_config['font_size']},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=self.chart_config['height'],
            margin=self.chart_config['margin'],
            hovermode=self.chart_config['hovermode'],
            showlegend=self.chart_config['showlegend']
        )
        
        # Update axes styling
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(148, 163, 184, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(148, 163, 184, 0.3)'
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(148, 163, 184, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(148, 163, 184, 0.3)'
        )
        
        return fig
    
    def _create_line_chart(self, data, dataset_name):
        """Create line chart for trend analysis"""
        if dataset_name == 'sales':
            # Monthly revenue trend
            monthly_data = data.groupby([data['date'].dt.to_period('M'), 'region'])['revenue'].sum().reset_index()
            monthly_data['date'] = monthly_data['date'].dt.to_timestamp()
            
            fig = px.line(
                monthly_data,
                x='date',
                y='revenue',
                color='region',
                title='Revenue Trend Over Time by Region',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
        elif dataset_name == 'climate':
            # Temperature trend by location
            monthly_data = data.groupby([data['date'].dt.to_period('M'), 'location'])['temperature'].mean().reset_index()
            monthly_data['date'] = monthly_data['date'].dt.to_timestamp()
            
            fig = px.line(
                monthly_data,
                x='date',
                y='temperature',
                color='location',
                title='Average Temperature Trend by Location',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
        elif dataset_name == 'population':
            # Population growth by continent
            fig = px.line(
                data,
                x='year',
                y='population',
                color='continent',
                title='Population Growth by Continent',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
        elif dataset_name == 'finance':
            # Stock price trends
            fig = px.line(
                data,
                x='date',
                y='price',
                color='symbol',
                title='Stock Price Trends',
                color_discrete_sequence=px.colors.qualitative.Dark2
            )
            
        else:
            # Generic line chart
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            date_cols = data.select_dtypes(include=['datetime64']).columns
            
            if len(date_cols) > 0 and len(numeric_cols) > 0:
                fig = px.line(data, x=date_cols[0], y=numeric_cols[0], title='Trend Over Time')
            else:
                fig = go.Figure()
                fig.add_annotation(text="No suitable data for line chart", x=0.5, y=0.5)
        
        self._apply_theme(fig, fig.layout.title.text)
        return json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    
    def _create_bar_chart(self, data, dataset_name):
        """Create bar chart for category comparison"""
        if dataset_name == 'sales':
            # Top products by revenue
            product_revenue = data.groupby('product')['revenue'].sum().sort_values(ascending=False).head(10)
            
            fig = px.bar(
                x=product_revenue.index,
                y=product_revenue.values,
                title='Top Products by Revenue',
                color=product_revenue.values,
                color_continuous_scale='Blues'
            )
            fig.update_xaxes(title='Product')
            fig.update_yaxes(title='Revenue ($)')
            
        elif dataset_name == 'climate':
            # Average temperature by location
            temp_by_location = data.groupby('location')['temperature'].mean().sort_values(ascending=False)
            
            fig = px.bar(
                x=temp_by_location.index,
                y=temp_by_location.values,
                title='Average Temperature by Location',
                color=temp_by_location.values,
                color_continuous_scale='RdYlBu_r'
            )
            fig.update_xaxes(title='Location')
            fig.update_yaxes(title='Temperature (°C)')
            
        elif dataset_name == 'population':
            # Top countries by population (latest year)
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year]
            top_countries = latest_data.nlargest(15, 'population')
            
            fig = px.bar(
                top_countries,
                x='country',
                y='population',
                title=f'Top Countries by Population ({latest_year})',
                color='population',
                color_continuous_scale='Viridis'
            )
            fig.update_xaxes(title='Country', tickangle=45)
            fig.update_yaxes(title='Population')
            
        elif dataset_name == 'finance':
            # Average volume by sector
            sector_volume = data.groupby('sector')['volume'].mean().sort_values(ascending=False)
            
            fig = px.bar(
                x=sector_volume.index,
                y=sector_volume.values,
                title='Average Trading Volume by Sector',
                color=sector_volume.values,
                color_continuous_scale='Purples'
            )
            fig.update_xaxes(title='Sector')
            fig.update_yaxes(title='Volume')
            
        else:
            # Generic bar chart
            categorical_cols = data.select_dtypes(include=['object']).columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                grouped_data = data.groupby(categorical_cols[0])[numeric_cols[0]].sum().sort_values(ascending=False).head(10)
                fig = px.bar(x=grouped_data.index, y=grouped_data.values, title='Category Comparison')
            else:
                fig = go.Figure()
                fig.add_annotation(text="No suitable data for bar chart", x=0.5, y=0.5)
        
        self._apply_theme(fig, fig.layout.title.text)
        return json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    
    def _create_pie_chart(self, data, dataset_name):
        """Create pie chart for distribution analysis"""
        if dataset_name == 'sales':
            # Revenue distribution by region
            region_revenue = data.groupby('region')['revenue'].sum()
            
            fig = px.pie(
                values=region_revenue.values,
                names=region_revenue.index,
                title='Revenue Distribution by Region',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
        elif dataset_name == 'climate':
            # Distribution by climate zone
            zone_counts = data['climate_zone'].value_counts()
            
            fig = px.pie(
                values=zone_counts.values,
                names=zone_counts.index,
                title='Data Distribution by Climate Zone',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
        elif dataset_name == 'population':
            # Population distribution by continent (latest year)
            latest_year = data['year'].max()
            latest_data = data[data['year'] == latest_year]
            continent_pop = latest_data.groupby('continent')['population'].sum()
            
            fig = px.pie(
                values=continent_pop.values,
                names=continent_pop.index,
                title=f'Population Distribution by Continent ({latest_year})',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
        elif dataset_name == 'finance':
            # Market cap distribution by sector
            sector_cap = data.groupby('sector')['market_cap'].sum()
            
            fig = px.pie(
                values=sector_cap.values,
                names=sector_cap.index,
                title='Market Cap Distribution by Sector',
                color_discrete_sequence=px.colors.qualitative.Dark2
            )
            
        else:
            # Generic pie chart
            categorical_cols = data.select_dtypes(include=['object']).columns
            
            if len(categorical_cols) > 0:
                value_counts = data[categorical_cols[0]].value_counts().head(8)
                fig = px.pie(values=value_counts.values, names=value_counts.index, title='Distribution')
            else:
                fig = go.Figure()
                fig.add_annotation(text="No suitable data for pie chart", x=0.5, y=0.5)
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        self._apply_theme(fig, fig.layout.title.text)
        return json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    
    def _create_scatter_chart(self, data, dataset_name):
        """Create scatter plot for correlation analysis"""
        if dataset_name == 'sales':
            # Revenue vs Units Sold by Product
            fig = px.scatter(
                data,
                x='units_sold',
                y='revenue',
                color='product',
                size='profit_margin',
                title='Revenue vs Units Sold by Product',
                hover_data=['sales_rep'],
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
        elif dataset_name == 'climate':
            # Temperature vs Humidity by Climate Zone
            fig = px.scatter(
                data,
                x='temperature',
                y='humidity',
                color='climate_zone',
                size='rainfall',
                title='Temperature vs Humidity by Climate Zone',
                hover_data=['location'],
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
        elif dataset_name == 'population':
            # GDP per Capita vs Life Expectancy
            fig = px.scatter(
                data,
                x='gdp_per_capita',
                y='life_expectancy',
                color='continent',
                size='population',
                title='GDP per Capita vs Life Expectancy',
                hover_data=['country'],
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
        elif dataset_name == 'finance':
            # Price vs Volume by Sector
            fig = px.scatter(
                data,
                x='volume',
                y='price',
                color='sector',
                size='market_cap',
                title='Stock Price vs Trading Volume by Sector',
                hover_data=['symbol'],
                color_discrete_sequence=px.colors.qualitative.Dark2
            )
            
        else:
            # Generic scatter plot
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) >= 2:
                fig = px.scatter(data, x=numeric_cols[0], y=numeric_cols[1], title='Correlation Analysis')
            else:
                fig = go.Figure()
                fig.add_annotation(text="No suitable data for scatter plot", x=0.5, y=0.5)
        
        self._apply_theme(fig, fig.layout.title.text)
        return json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
    
    def _create_heatmap(self, data, dataset_name):
        """Create heatmap for multi-dimensional analysis"""
        if dataset_name == 'sales':
            # Revenue heatmap: Product vs Region
            heatmap_data = data.groupby(['product', 'region'])['revenue'].sum().unstack(fill_value=0)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Blues',
                hoverongaps=False
            ))
            fig.update_layout(title='Revenue Heatmap: Product vs Region')
            
        elif dataset_name == 'climate':
            # Temperature heatmap: Month vs Location
            data['month'] = data['date'].dt.month
            heatmap_data = data.groupby(['month', 'location'])['temperature'].mean().unstack(fill_value=0)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='RdYlBu_r',
                hoverongaps=False
            ))
            fig.update_layout(title='Temperature Heatmap: Month vs Location')
            
        elif dataset_name == 'population':
            # Population growth heatmap: Decade vs Continent
            data['decade'] = (data['year'] // 10) * 10
            heatmap_data = data.groupby(['decade', 'continent'])['growth_rate'].mean().unstack(fill_value=0)
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Viridis',
                hoverongaps=False
            ))
            fig.update_layout(title='Population Growth Rate Heatmap: Decade vs Continent')
            
        elif dataset_name == 'finance':
            # Correlation heatmap of numeric columns
            numeric_cols = ['price', 'volume', 'market_cap', 'daily_return']
            correlation_matrix = data[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='RdBu',
                zmid=0,
                hoverongaps=False
            ))
            fig.update_layout(title='Financial Metrics Correlation Heatmap')
            
        else:
            # Generic correlation heatmap
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) >= 2:
                correlation_matrix = data[numeric_cols].corr()
                fig = go.Figure(data=go.Heatmap(
                    z=correlation_matrix.values,
                    x=correlation_matrix.columns,
                    y=correlation_matrix.index,
                    colorscale='RdBu',
                    zmid=0
                ))
                fig.update_layout(title='Correlation Heatmap')
            else:
                fig = go.Figure()
                fig.add_annotation(text="No suitable data for heatmap", x=0.5, y=0.5)
        
        self._apply_theme(fig, fig.layout.title.text)
        return json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig))
