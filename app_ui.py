# Importing Libraries
from nicegui import ui, app as nicegui_app
from fastapi import FastAPI
import plotly.express as px
import pandas as pd

# Create a Sample DataFrame
df = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'Revenue': [200, 220, 250, 230, 280],
    'Compliance': [80, 85, 90, 88, 95],
    'Risk': [60, 58, 70, 65, 75]
})

# Create a FastAPI app
# app = FastAPI()

@nicegui_app.get('/api/revenue')
def get_revenue():
    return df.to_dict(orient='records')


@ui.page('/')
def main_page():
    # Define a global variable for the drawer
    global left_drawer

    ui.add_head_html('<link rel="stylesheet" href="/static/theme.css">')

    # Left Drawer (Navigation)
    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4') as left_drawer:
        ui.label('Navigation').classes('text-lg font-bold p-2')
        ui.separator()
        ui.link('Dashboard', target='/dashboard')
        ui.link('Settings', target='/settings')
        ui.link('Profile', target='/profile')
        ui.link('Help', target='/help')

    # Header with top menu
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label('RegTech365 Dashboard').classes('text-2xl text-white p-4')
        
        with ui.row():
            ui.button(icon='menu', on_click=left_drawer.toggle).props('flat color=white')
            with ui.menu():
                ui.menu_item('Home', on_click=lambda: ui.navigate('/'))
                ui.menu_item('About', on_click=lambda: ui.navigate('/about'))
                ui.menu_item('Contact', on_click=lambda: ui.navigate('/contact'))

    # Main content area
    with ui.column().classes('p-4'):
        ui.label('Welcome to the main content area!').classes('text-lg')

        # Quick navigation buttons (these navigate to routes — create pages for them)
        with ui.row().classes('items-center gap-4'):
            ui.button('Dashboard', on_click=lambda: ui.navigate('/dashboard'))
            ui.button('Settings', on_click=lambda: ui.navigate('/settings'))
            ui.button('Profile', on_click=lambda: ui.navigate('/profile'))
            ui.button('Help', on_click=lambda: ui.navigate('/help'))

        # Dropdown / select example
        ui.select(['Report A', 'Report B', 'Report C'], label='Choose report',
              on_change=lambda e: ui.notify(f'Selected: {e.value}'))

        # Tabs for a sample platform
        with ui.tabs() as platform_tabs:
            with ui.tab('Overview'):
                ui.label('Platform A — Overview').classes('text-lg')
                ui.markdown('Summary content and KPIs go here.')
            with ui.tab('Reports'):
                ui.label('Platform A — Reports')
                ui.button('Open Report A', on_click=lambda: ui.navigate('/reports/a'))
            with ui.tab('Settings'):
                ui.label('Platform A — Settings')
        line_fig = px.line(df, x='Month', y='Revenue', title='Monthly Revenue')
        ui.plotly(line_fig)

        # Pie chart showing Compliance distribution
        fig_pie = px.pie(df, names='Month', values='Compliance', title='Compliance Distribution by Month')
        ui.plotly(fig_pie)

        # Bar chart comparing Risk and Compliance
        fig_bar = px.bar(df, x='Month', y=['Risk', 'Compliance'], barmode='group', title='Risk vs Compliance by Month')
        ui.plotly(fig_bar)

@nicegui_app.get("/api/test")
def test_api():
    return {"status": "FastAPI is integrated successfully!"}

@ui.page('/dashboard')
def dashboard_page():
    ui.label('Dashboard Overview').classes('text-2xl font-bold')
    ui.markdown('This page shows system analytics and charts.')
    
    # Example: reuse one of your charts here
    fig = px.bar(df, x='Month', y='Compliance', title='Monthly Compliance')
    ui.plotly(fig)


@ui.page('/settings')
def settings_page():
    ui.label('Settings Page').classes('text-2xl font-bold')
    ui.markdown('Adjust preferences and configuration here.')

@ui.page('/profile')
def profile_page():
    ui.label('Profile Page').classes('text-2xl font-bold')
    ui.markdown('User information and activity summary.')

@ui.page('/help')
def help_page():
    ui.label('Help & Support').classes('text-2xl font-bold')
    ui.markdown('Contact admin or view FAQs.')

@ui.page('/reports')
def report_a_page():
    ui.label('Report A').classes('text-2xl font-bold')
    ui.markdown('Detailed report analysis goes here.')

# Run the app
if __name__ in {"__main__", "__mp_main__"}:

    ui.run()