# 📊 DataViz Pro Dashboard

A professional data visualization platform with dynamic filtering, interactive charts, and real-time Git integration.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## ✨ **Features**

- **🔄 Git Integration**: Real-time commit tracking with auto-refresh
- **📊 Dynamic Filters**: Auto-adapt to any dataset structure
- **📈 Interactive Charts**: Real-time visualizations with Plotly.js
- **📁 File Upload**: Support for CSV, Excel, JSON files
- **💾 Data Export**: Download filtered data and charts
- **📱 Responsive Design**: Modern UI with Tailwind CSS

## 🚀 **Quick Start**

```bash
# Clone and install
git clone https://github.com/sumaiyahibrahim/Data-Visualization-Dashboard.git
cd Data-Visualization-Dashboard
pip install -r requirements.txt

# Run locally
python app.py
# Open: http://localhost:5000
```

## 🛠️ **Tech Stack**

- **Backend**: Flask + Python
- **Frontend**: Tailwind CSS + JavaScript
- **Charts**: Plotly.js
- **Data**: Pandas + NumPy
- **Deployment**: Gunicorn

## 📁 **Structure**

```
├── app.py                 # Main Flask app
├── data_manager.py        # Data processing
├── chart_generator.py     # Chart generation
├── requirements.txt       # Dependencies
├── static/               # CSS, JS, assets
├── templates/            # HTML templates
└── data/                # Sample datasets
```

## 🌐 **Deployment**

### **Render.com (Recommended)**
1. Push to GitHub
2. Connect repository on Render
3. Set environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secure-key`
4. Deploy automatically!

### **Other Platforms**
- **Railway**: Auto-detection supported
- **Vercel**: One-click deployment
- **Heroku**: Production ready

## 🔧 **Environment Variables**

```
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
```

## 📊 **Sample Data**

Includes datasets for:
- Sales analytics
- World happiness index
- Stock market data
- Weather records

## 🎯 **Key Highlights**

- **Real-time Git tracking**: Shows actual commit timestamps
- **Professional UI**: Portfolio-ready design
- **Production optimized**: Fast, scalable, secure
- **Auto-deployment**: Updates on GitHub push

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built for professional data visualization and portfolio showcasing** 🎯
