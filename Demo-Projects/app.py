# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Configure file watcher to avoid infinite loops - simplified for compatibility
if os.getenv('DASH_DEBUG', 'true').lower() == 'true':
    # Only watch specific directories and files
    app.config.suppress_callback_exceptions = True
    app.config.external_stylesheets = []
    app.config.external_scripts = []

if __name__ == "__main__":
    app.run(
        debug=True,
        dev_tools_hot_reload=True,
        dev_tools_hot_reload_interval=1000,
        dev_tools_hot_reload_watch_interval=1000,
        dev_tools_hot_reload_max_retry=5,
        dev_tools_silence_routes_logging=True,
        dev_tools_ui=True,
        dev_tools_props_check=True,
        dev_tools_serve_dev_bundles=True,
        dev_tools_prune_errors=True
    ) 