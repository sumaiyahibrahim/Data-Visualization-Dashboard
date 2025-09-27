"""
Data Manager - Handles all data operations for the dashboard
Supports multiple datasets: Sales, Climate, Population, Finance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class DataManager:
    """
    Professional data management class for multi-domain datasets
    """
    
    def __init__(self):
        self.datasets = {}
        self.custom_datasets = {}
        self.dataset_configs = {
            'sales': {
                'name': 'Sales Analytics',
                'description': 'Global sales performance data across regions and products',
                'date_column': 'date',
                'value_columns': ['revenue', 'units_sold'],
                'category_columns': ['region', 'product', 'sales_rep'],
                'color_scheme': 'blues'
            },
            'climate': {
                'name': 'Climate Data',
                'description': 'Global climate measurements and weather patterns',
                'date_column': 'date',
                'value_columns': ['temperature', 'rainfall', 'humidity'],
                'category_columns': ['location', 'climate_zone'],
                'color_scheme': 'greens'
            },
            'population': {
                'name': 'Population Demographics',
                'description': 'Global population statistics and demographic trends',
                'date_column': 'year',
                'value_columns': ['population', 'growth_rate', 'urban_percentage'],
                'category_columns': ['country', 'continent', 'income_level'],
                'color_scheme': 'oranges'
            },
            'finance': {
                'name': 'Financial Markets',
                'description': 'Stock market data and financial indicators',
                'date_column': 'date',
                'value_columns': ['price', 'volume', 'market_cap'],
                'category_columns': ['symbol', 'sector', 'exchange'],
                'color_scheme': 'purples'
            }
        }
    
    def initialize_sample_data(self):
        """Initialize sample datasets if they don't exist"""
        data_dir = 'data'
        os.makedirs(data_dir, exist_ok=True)
        
        for dataset_name in self.dataset_configs.keys():
            file_path = os.path.join(data_dir, f'{dataset_name}.csv')
            if not os.path.exists(file_path):
                print(f"Generating sample data for {dataset_name}...")
                data = self._generate_sample_data(dataset_name)
                data.to_csv(file_path, index=False)
                print(f"Created {file_path} with {len(data)} records")
    
    def _generate_sample_data(self, dataset_name):
        """Generate realistic sample data for each dataset"""
        np.random.seed(42)  # For reproducible data
        
        if dataset_name == 'sales':
            return self._generate_sales_data()
        elif dataset_name == 'climate':
            return self._generate_climate_data()
        elif dataset_name == 'population':
            return self._generate_population_data()
        elif dataset_name == 'finance':
            return self._generate_finance_data()
        else:
            raise ValueError(f"Unknown dataset: {dataset_name}")
    
    def _generate_sales_data(self):
        """Generate realistic sales data"""
        regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
        products = ['Laptops', 'Smartphones', 'Tablets', 'Headphones', 'Smart Watches', 'Cameras', 'Gaming Consoles', 'Smart TVs']
        sales_reps = ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown', 'Frank Miller', 'Grace Lee', 'Henry Taylor']
        
        data = []
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        for _ in range(2000):
            date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
            region = np.random.choice(regions)
            product = np.random.choice(products)
            sales_rep = np.random.choice(sales_reps)
            
            # Seasonal effects
            month = date.month
            seasonal_multiplier = 1.0
            if month in [11, 12]:  # Holiday season
                seasonal_multiplier = 1.5
            elif month in [6, 7]:  # Summer
                seasonal_multiplier = 1.2
            
            base_price = {
                'Laptops': 800, 'Smartphones': 600, 'Tablets': 300, 'Headphones': 150,
                'Smart Watches': 250, 'Cameras': 500, 'Gaming Consoles': 400, 'Smart TVs': 700
            }[product]
            
            units_sold = int(np.random.poisson(20) * seasonal_multiplier)
            unit_price = base_price * np.random.uniform(0.8, 1.2)
            revenue = units_sold * unit_price
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'region': region,
                'product': product,
                'sales_rep': sales_rep,
                'units_sold': units_sold,
                'unit_price': round(unit_price, 2),
                'revenue': round(revenue, 2),
                'profit_margin': round(np.random.uniform(0.15, 0.35), 3),
                'customer_satisfaction': round(np.random.uniform(3.5, 5.0), 1)
            })
        
        return pd.DataFrame(data)
    
    def _generate_climate_data(self):
        """Generate realistic climate data"""
        locations = ['New York', 'London', 'Tokyo', 'Sydney', 'Mumbai', 'Cairo', 'São Paulo', 'Moscow', 'Lagos', 'Bangkok']
        climate_zones = ['Temperate', 'Tropical', 'Arid', 'Continental', 'Mediterranean']
        
        data = []
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        for location in locations:
            # Assign climate zone based on location
            zone_mapping = {
                'New York': 'Temperate', 'London': 'Temperate', 'Tokyo': 'Temperate',
                'Sydney': 'Mediterranean', 'Mumbai': 'Tropical', 'Cairo': 'Arid',
                'São Paulo': 'Tropical', 'Moscow': 'Continental', 'Lagos': 'Tropical',
                'Bangkok': 'Tropical'
            }
            climate_zone = zone_mapping[location]
            
            # Generate daily data
            current_date = start_date
            while current_date <= end_date:
                # Base temperature by location and season
                base_temps = {
                    'New York': 15, 'London': 12, 'Tokyo': 18, 'Sydney': 20,
                    'Mumbai': 28, 'Cairo': 25, 'São Paulo': 22, 'Moscow': 5,
                    'Lagos': 30, 'Bangkok': 32
                }
                
                base_temp = base_temps[location]
                seasonal_variation = 10 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)
                temperature = base_temp + seasonal_variation + np.random.normal(0, 3)
                
                # Rainfall based on climate zone
                if climate_zone == 'Tropical':
                    rainfall = np.random.exponential(5)
                elif climate_zone == 'Arid':
                    rainfall = np.random.exponential(0.5)
                else:
                    rainfall = np.random.exponential(2)
                
                humidity = np.random.uniform(30, 90)
                wind_speed = np.random.exponential(10)
                
                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'location': location,
                    'climate_zone': climate_zone,
                    'temperature': round(temperature, 1),
                    'rainfall': round(rainfall, 1),
                    'humidity': round(humidity, 1),
                    'wind_speed': round(wind_speed, 1),
                    'air_quality_index': np.random.randint(20, 200)
                })
                
                current_date += timedelta(days=7)  # Weekly data to keep size manageable
        
        return pd.DataFrame(data)
    
    def _generate_population_data(self):
        """Generate realistic population data"""
        countries = ['United States', 'China', 'India', 'Brazil', 'Russia', 'Japan', 'Germany', 'United Kingdom', 'France', 'Italy', 'Canada', 'Australia', 'Mexico', 'South Korea', 'Spain', 'Argentina', 'South Africa', 'Egypt', 'Nigeria', 'Kenya']
        continents = ['North America', 'Asia', 'Asia', 'South America', 'Europe', 'Asia', 'Europe', 'Europe', 'Europe', 'Europe', 'North America', 'Oceania', 'North America', 'Asia', 'Europe', 'South America', 'Africa', 'Africa', 'Africa', 'Africa']
        income_levels = ['High Income', 'Upper Middle Income', 'Lower Middle Income', 'Low Income']
        
        data = []
        
        for i, country in enumerate(countries):
            continent = continents[i]
            
            # Assign income level based on country
            income_mapping = {
                'United States': 'High Income', 'China': 'Upper Middle Income', 'India': 'Lower Middle Income',
                'Brazil': 'Upper Middle Income', 'Russia': 'Upper Middle Income', 'Japan': 'High Income',
                'Germany': 'High Income', 'United Kingdom': 'High Income', 'France': 'High Income',
                'Italy': 'High Income', 'Canada': 'High Income', 'Australia': 'High Income',
                'Mexico': 'Upper Middle Income', 'South Korea': 'High Income', 'Spain': 'High Income',
                'Argentina': 'Upper Middle Income', 'South Africa': 'Upper Middle Income',
                'Egypt': 'Lower Middle Income', 'Nigeria': 'Lower Middle Income', 'Kenya': 'Lower Middle Income'
            }
            income_level = income_mapping.get(country, 'Lower Middle Income')
            
            # Generate yearly data from 2000 to 2024
            base_population = np.random.randint(10_000_000, 1_400_000_000)
            
            for year in range(2000, 2025):
                # Simulate population growth
                growth_rate = np.random.uniform(-0.5, 3.0) if income_level in ['Low Income', 'Lower Middle Income'] else np.random.uniform(-0.2, 1.5)
                population = int(base_population * (1 + growth_rate/100) ** (year - 2000))
                
                urban_percentage = np.random.uniform(30, 95)
                life_expectancy = np.random.uniform(60, 85)
                literacy_rate = np.random.uniform(50, 99)
                gdp_per_capita = np.random.uniform(500, 80000)
                
                data.append({
                    'year': year,
                    'country': country,
                    'continent': continent,
                    'income_level': income_level,
                    'population': population,
                    'growth_rate': round(growth_rate, 2),
                    'urban_percentage': round(urban_percentage, 1),
                    'life_expectancy': round(life_expectancy, 1),
                    'literacy_rate': round(literacy_rate, 1),
                    'gdp_per_capita': round(gdp_per_capita, 0)
                })
        
        return pd.DataFrame(data)
    
    def _generate_finance_data(self):
        """Generate realistic financial market data"""
        symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'ORCL', 'CRM', 'ADBE', 'PYPL', 'INTC', 'CSCO']
        sectors = ['Technology', 'Technology', 'Technology', 'Consumer Discretionary', 'Consumer Discretionary', 'Technology', 'Technology', 'Communication Services', 'Technology', 'Technology', 'Technology', 'Technology', 'Financial Services', 'Technology', 'Technology']
        exchanges = ['NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NYSE', 'NYSE', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ']
        
        data = []
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        for i, symbol in enumerate(symbols):
            sector = sectors[i]
            exchange = exchanges[i]
            
            # Base price for each stock
            base_prices = {
                'AAPL': 150, 'GOOGL': 2500, 'MSFT': 300, 'AMZN': 3200, 'TSLA': 800,
                'META': 300, 'NVDA': 400, 'NFLX': 500, 'AMD': 100, 'ORCL': 80,
                'CRM': 200, 'ADBE': 500, 'PYPL': 250, 'INTC': 50, 'CSCO': 45
            }
            
            current_price = base_prices[symbol]
            current_date = start_date
            
            while current_date <= end_date:
                # Skip weekends
                if current_date.weekday() >= 5:
                    current_date += timedelta(days=1)
                    continue
                
                # Simulate realistic price movements
                daily_return = np.random.normal(0.001, 0.025)  # Average 0.1% daily return with 2.5% volatility
                price_change = current_price * daily_return
                
                open_price = current_price
                close_price = current_price + price_change
                high_price = max(open_price, close_price) * np.random.uniform(1.0, 1.03)
                low_price = min(open_price, close_price) * np.random.uniform(0.97, 1.0)
                
                volume = int(np.random.lognormal(15, 1))  # Log-normal distribution for volume
                market_cap = close_price * np.random.randint(1_000_000, 10_000_000)  # Shares outstanding
                
                data.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'symbol': symbol,
                    'sector': sector,
                    'exchange': exchange,
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(close_price, 2),
                    'volume': volume,
                    'market_cap': round(market_cap, 0),
                    'price': round(close_price, 2),
                    'daily_return': round(daily_return * 100, 2)
                })
                
                current_price = close_price
                current_date += timedelta(days=1)
        
        return pd.DataFrame(data)
    
    def get_available_datasets(self):
        """Get list of available datasets with metadata"""
        all_datasets = {name: config for name, config in self.dataset_configs.items()}
        all_datasets.update(self.custom_datasets)
        return all_datasets
    
    def load_dataset(self, dataset_name):
        """Load dataset from CSV file"""
        if dataset_name not in self.datasets:
            file_path = f'data/{dataset_name}.csv'
            if os.path.exists(file_path):
                self.datasets[dataset_name] = pd.read_csv(file_path)
                # Convert date columns
                config = self.dataset_configs[dataset_name]
                date_col = config['date_column']
                if date_col in self.datasets[dataset_name].columns:
                    self.datasets[dataset_name][date_col] = pd.to_datetime(self.datasets[dataset_name][date_col])
            else:
                raise FileNotFoundError(f"Dataset file not found: {file_path}")
        
        return self.datasets[dataset_name]
    
    def get_dataset_summary(self, dataset_name):
        """Get summary information about a dataset"""
        df = self.load_dataset(dataset_name)
        config = self.dataset_configs[dataset_name]
        
        summary = {
            'name': config['name'],
            'description': config['description'],
            'total_rows': len(df),
            'columns': list(df.columns),
            'date_range': {
                'start': df[config['date_column']].min().strftime('%Y-%m-%d'),
                'end': df[config['date_column']].max().strftime('%Y-%m-%d')
            },
            'value_columns': config['value_columns'],
            'category_columns': config['category_columns']
        }
        
        return summary
    
    def get_filtered_data(self, dataset_name, filters):
        """Apply filters to dataset and return filtered data"""
        df = self.load_dataset(dataset_name).copy()
        config = self.dataset_configs[dataset_name]
        
        # Apply date filters
        if filters.get('start_date') and filters.get('end_date'):
            start_date = pd.to_datetime(filters['start_date'])
            end_date = pd.to_datetime(filters['end_date'])
            df = df[(df[config['date_column']] >= start_date) & (df[config['date_column']] <= end_date)]
        
        # Apply category filters
        if filters.get('regions') and 'region' in df.columns:
            df = df[df['region'].isin(filters['regions'])]
        
        if filters.get('categories'):
            # Find the appropriate category column
            for col in config['category_columns']:
                if col in df.columns and filters.get('categories'):
                    df = df[df[col].isin(filters['categories'])]
                    break
        
        # Apply limit
        if filters.get('limit'):
            df = df.head(filters['limit'])
        
        return df
    
    def get_filter_options(self, dataset_name):
        """Get available filter options for a dataset with enhanced dynamic detection"""
        try:
            df = self.load_dataset(dataset_name)
            if df is None or df.empty:
                return {'error': 'Dataset not found or empty'}
            
            config = self.dataset_configs.get(dataset_name, {})
            category_columns = config.get('category_columns', [])
            value_columns = config.get('value_columns', [])
            date_column = config.get('date_column', 'date')
            
            # Auto-detect columns if not configured (for custom datasets)
            if not category_columns and not value_columns:
                category_columns = []
                value_columns = []
                
                for col in df.columns:
                    # Skip date columns
                    if col.lower() in ['date', 'time', 'timestamp'] or 'date' in col.lower():
                        continue
                    
                    # Check if column is categorical (string or low cardinality)
                    if df[col].dtype == 'object' or df[col].nunique() <= 20:
                        category_columns.append(col)
                    # Check if column is numeric with reasonable range for filtering
                    elif pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() > 10:
                        value_columns.append(col)
            
            filter_options = {}
            
            # Generate filter options for categorical columns
            for col in category_columns:
                if col in df.columns:
                    unique_values = df[col].dropna().unique()
                    if len(unique_values) <= 50:  # Only show if not too many options
                        filter_options[col] = {
                            'type': 'select',
                            'label': col.replace('_', ' ').title(),
                            'options': sorted([str(val) for val in unique_values]),
                            'icon': self._get_column_icon(col)
                        }
            
            # Generate range filters for numeric columns
            for col in value_columns:
                if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                    col_data = df[col].dropna()
                    if len(col_data) > 0:
                        filter_options[col] = {
                            'type': 'range',
                            'label': col.replace('_', ' ').title(),
                            'min': float(col_data.min()),
                            'max': float(col_data.max()),
                            'step': self._calculate_step(col_data),
                            'icon': self._get_column_icon(col)
                        }
            
            # Handle date range
            date_col = None
            for col in df.columns:
                if col.lower() in ['date', 'time', 'timestamp'] or 'date' in col.lower():
                    date_col = col
                    break
            
            if date_col and date_col in df.columns:
                try:
                    # Convert to datetime if not already
                    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
                        df[date_col] = pd.to_datetime(df[date_col])
                    
                    filter_options['date_range'] = {
                        'min': df[date_col].min().strftime('%Y-%m-%d'),
                        'max': df[date_col].max().strftime('%Y-%m-%d')
                    }
                except:
                    pass  # Skip date range if conversion fails
            
            return filter_options
            
        except Exception as e:
            return {'error': str(e)}
    
    def _get_column_icon(self, column_name):
        """Get appropriate icon for column based on name"""
        column_lower = column_name.lower()
        
        icon_mapping = {
            'region': 'fas fa-globe',
            'location': 'fas fa-map-marker-alt',
            'country': 'fas fa-flag',
            'continent': 'fas fa-globe-americas',
            'product': 'fas fa-box',
            'category': 'fas fa-tags',
            'sales_rep': 'fas fa-user-tie',
            'rep': 'fas fa-user',
            'employee': 'fas fa-user',
            'customer': 'fas fa-user-friends',
            'revenue': 'fas fa-dollar-sign',
            'price': 'fas fa-dollar-sign',
            'cost': 'fas fa-dollar-sign',
            'profit': 'fas fa-chart-line',
            'units': 'fas fa-cubes',
            'quantity': 'fas fa-cubes',
            'temperature': 'fas fa-thermometer-half',
            'climate': 'fas fa-cloud',
            'weather': 'fas fa-cloud-sun',
            'population': 'fas fa-users',
            'demographic': 'fas fa-users',
            'sector': 'fas fa-industry',
            'industry': 'fas fa-industry',
            'symbol': 'fas fa-chart-line',
            'stock': 'fas fa-chart-line',
            'exchange': 'fas fa-building',
            'status': 'fas fa-info-circle',
            'type': 'fas fa-tag',
            'level': 'fas fa-layer-group'
        }
        
        # Check for exact and partial matches
        for key, icon in icon_mapping.items():
            if key in column_lower:
                return icon
        
        # Default icons based on common patterns
        if any(word in column_lower for word in ['name', 'title', 'label']):
            return 'fas fa-tag'
        elif any(word in column_lower for word in ['amount', 'value', 'total', 'sum']):
            return 'fas fa-calculator'
        elif any(word in column_lower for word in ['rate', 'percent', 'ratio']):
            return 'fas fa-percentage'
        else:
            return 'fas fa-filter'
    
    def _calculate_step(self, data):
        """Calculate appropriate step size for numeric range inputs"""
        data_range = data.max() - data.min()
        if data_range == 0:
            return 1
        
        # Calculate step based on range
        if data_range < 1:
            return 0.01
        elif data_range < 10:
            return 0.1
        elif data_range < 100:
            return 1
        elif data_range < 1000:
            return 10
        else:
            return 100
    
    def calculate_summary_stats(self, df, dataset_name):
        """Calculate summary statistics for filtered data"""
        config = self.dataset_configs[dataset_name]
        
        stats = {
            'total_records': len(df),
            'date_range': {
                'start': df[config['date_column']].min().strftime('%Y-%m-%d'),
                'end': df[config['date_column']].max().strftime('%Y-%m-%d')
            }
        }
        
        # Calculate statistics for value columns
        for col in config['value_columns']:
            if col in df.columns:
                stats[f'{col}_total'] = float(df[col].sum())
                stats[f'{col}_avg'] = float(df[col].mean())
                stats[f'{col}_max'] = float(df[col].max())
                stats[f'{col}_min'] = float(df[col].min())
        
        # Count unique categories
        for col in config['category_columns']:
            if col in df.columns:
                stats[f'unique_{col}'] = int(df[col].nunique())
        
        return stats
    
    def process_uploaded_file(self, file_path, dataset_name):
        """Process uploaded file and create custom dataset"""
        try:
            # Read the file based on extension
            file_ext = file_path.split('.')[-1].lower()
            
            if file_ext == 'csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            elif file_ext == 'json':
                df = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            # Validate dataset
            if df.empty:
                raise ValueError("Dataset is empty")
            
            if len(df) < 2:
                raise ValueError("Dataset must have at least 2 rows")
            
            # Auto-detect column types
            date_columns = []
            numeric_columns = []
            category_columns = []
            
            for col in df.columns:
                # Try to detect date columns
                if any(keyword in col.lower() for keyword in ['date', 'time', 'year', 'month']):
                    try:
                        pd.to_datetime(df[col].dropna().head(100))
                        date_columns.append(col)
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                        continue
                    except:
                        pass
                
                # Check if numeric
                if df[col].dtype in ['int64', 'float64'] or pd.api.types.is_numeric_dtype(df[col]):
                    numeric_columns.append(col)
                else:
                    category_columns.append(col)
            
            # Create dataset configuration
            config = {
                'name': dataset_name.title(),
                'description': f'Custom uploaded dataset: {dataset_name}',
                'date_column': date_columns[0] if date_columns else None,
                'value_columns': numeric_columns[:5],  # Limit to first 5 numeric columns
                'category_columns': category_columns[:5],  # Limit to first 5 category columns
                'color_scheme': 'viridis',
                'is_custom': True,
                'upload_date': datetime.now().isoformat(),
                'total_rows': len(df),
                'total_columns': len(df.columns)
            }
            
            # Save dataset
            safe_name = dataset_name.lower().replace(' ', '_').replace('-', '_')
            file_path = f'data/{safe_name}.csv'
            df.to_csv(file_path, index=False)
            
            # Store in custom datasets
            self.custom_datasets[safe_name] = config
            self.dataset_configs[safe_name] = config
            
            # Save custom datasets registry
            self._save_custom_datasets_registry()
            
            return {
                'success': True,
                'dataset_name': safe_name,
                'message': f'Dataset "{dataset_name}" uploaded successfully',
                'config': config
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_custom_dataset(self, dataset_name):
        """Delete a custom dataset"""
        try:
            if dataset_name not in self.custom_datasets:
                return {'success': False, 'error': 'Dataset not found or not a custom dataset'}
            
            # Remove from memory
            if dataset_name in self.datasets:
                del self.datasets[dataset_name]
            
            if dataset_name in self.custom_datasets:
                del self.custom_datasets[dataset_name]
            
            if dataset_name in self.dataset_configs:
                del self.dataset_configs[dataset_name]
            
            # Remove file
            file_path = f'data/{dataset_name}.csv'
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Update registry
            self._save_custom_datasets_registry()
            
            return {
                'success': True,
                'message': f'Dataset "{dataset_name}" deleted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _save_custom_datasets_registry(self):
        """Save custom datasets registry to file"""
        try:
            registry_path = 'data/custom_datasets.json'
            with open(registry_path, 'w') as f:
                json.dump(self.custom_datasets, f, indent=2)
        except Exception as e:
            print(f"Error saving custom datasets registry: {e}")
    
    def _load_custom_datasets_registry(self):
        """Load custom datasets registry from file"""
        try:
            registry_path = 'data/custom_datasets.json'
            if os.path.exists(registry_path):
                with open(registry_path, 'r') as f:
                    self.custom_datasets = json.load(f)
                    # Merge with dataset_configs
                    self.dataset_configs.update(self.custom_datasets)
        except Exception as e:
            print(f"Error loading custom datasets registry: {e}")
    
    def initialize_sample_data(self):
        """Initialize sample datasets if they don't exist"""
        data_dir = 'data'
        os.makedirs(data_dir, exist_ok=True)
        
        # Load custom datasets registry
        self._load_custom_datasets_registry()
        
        for dataset_name in ['sales', 'climate', 'population', 'finance']:
            file_path = os.path.join(data_dir, f'{dataset_name}.csv')
            if not os.path.exists(file_path):
                print(f"Generating sample data for {dataset_name}...")
                data = self._generate_sample_data(dataset_name)
                data.to_csv(file_path, index=False)
                print(f"Created {file_path} with {len(data)} records")
