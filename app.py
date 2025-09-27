"""
DataViz Pro Dashboard - Professional Flask Application
A scalable, modern data visualization platform with Tailwind CSS
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import plotly
import json
from datetime import datetime, timedelta
import io
import os
from data_manager import DataManager
from chart_generator import ChartGenerator

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'dataviz-pro-2024-secure-key'
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}

# Initialize data manager and chart generator
data_manager = DataManager()
chart_generator = ChartGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def dashboard():
    """Main dashboard route"""
    # Get available datasets
    datasets = data_manager.get_available_datasets()
    
    # Get initial data for default dataset
    default_dataset = 'sales'
    initial_data = data_manager.get_dataset_summary(default_dataset)
    
    return render_template('dashboard.html', 
                         datasets=datasets,
                         initial_data=initial_data,
                         current_dataset=default_dataset)

@app.route('/api/datasets')
def get_datasets():
    """API endpoint to get available datasets"""
    datasets = data_manager.get_available_datasets()
    return jsonify(datasets)

@app.route('/api/dataset/<dataset_name>')
def get_dataset_info(dataset_name):
    """Get dataset information and summary"""
    try:
        data_info = data_manager.get_dataset_summary(dataset_name)
        return jsonify(data_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/filters/<dataset_name>')
def get_filter_options(dataset_name):
    """Get available filter options for a specific dataset"""
    try:
        filter_options = data_manager.get_filter_options(dataset_name)
        return jsonify(filter_options)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/data/<dataset_name>')
def get_dataset_data(dataset_name):
    """Get filtered dataset data"""
    try:
        # Get filter parameters
        filters = {
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'regions': request.args.getlist('regions'),
            'categories': request.args.getlist('categories'),
            'limit': int(request.args.get('limit', 1000))
        }
        
        # Get filtered data
        data = data_manager.get_filtered_data(dataset_name, filters)
        
        return jsonify({
            'data': data.to_dict('records'),
            'total_rows': len(data),
            'columns': list(data.columns)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/charts/<dataset_name>/<chart_type>')
def get_chart_data(dataset_name, chart_type):
    """Generate chart data for specific dataset and chart type"""
    try:
        # Get filter parameters
        filters = {
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'regions': request.args.getlist('regions'),
            'categories': request.args.getlist('categories')
        }
        
        # Get filtered data
        data = data_manager.get_filtered_data(dataset_name, filters)
        
        # Generate chart
        chart_json = chart_generator.create_chart(data, dataset_name, chart_type)
        
        return jsonify(chart_json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/summary/<dataset_name>')
def get_dataset_summary(dataset_name):
    """Get summary statistics for dataset"""
    try:
        # Get filter parameters
        filters = {
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'regions': request.args.getlist('regions'),
            'categories': request.args.getlist('categories')
        }
        
        # Get filtered data
        data = data_manager.get_filtered_data(dataset_name, filters)
        
        # Calculate summary statistics
        summary = data_manager.calculate_summary_stats(data, dataset_name)
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/export/<dataset_name>')
def export_data(dataset_name):
    """Export filtered data as CSV"""
    try:
        # Get filter parameters
        filters = {
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'regions': request.args.getlist('regions'),
            'categories': request.args.getlist('categories')
        }
        
        # Get filtered data
        data = data_manager.get_filtered_data(dataset_name, filters)
        
        # Create CSV in memory
        output = io.StringIO()
        data.to_csv(output, index=False)
        output.seek(0)
        
        # Create file-like object for download
        mem = io.BytesIO()
        mem.write(output.getvalue().encode())
        mem.seek(0)
        
        filename = f"{dataset_name}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return send_file(
            mem,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    """Upload custom dataset"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        dataset_name = request.form.get('dataset_name', '').strip()
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not dataset_name:
            return jsonify({'error': 'Dataset name is required'}), 400
        
        if file and allowed_file(file.filename):
            # Create upload directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Secure filename and save
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the uploaded file
            result = data_manager.process_uploaded_file(file_path, dataset_name)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return jsonify(result)
        else:
            return jsonify({'error': 'Invalid file type. Please upload CSV, Excel, or JSON files.'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/datasets/<dataset_name>/delete', methods=['DELETE'])
def delete_dataset(dataset_name):
    """Delete a custom dataset"""
    try:
        result = data_manager.delete_custom_dataset(dataset_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Initialize sample data if not exists
    data_manager.initialize_sample_data()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
