import csv
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('FIFA 2026 World Cup Stats')
st.write('Interactive dashboard with World Cup analytics and beautifully styled visuals.')

st.markdown(
    '''
    <style>
    .header-box {background: rgba(15, 28, 48, 0.95); border: 1px solid rgba(212,175,55,0.18); border-radius: 28px; padding: 36px; box-shadow: 0 30px 90px rgba(0,0,0,0.4); margin-bottom: 24px;}
    .hero-row {display: grid; grid-template-columns: 1fr; gap: 0; align-items: start; margin-bottom: 28px; max-width: 860px; margin-left: auto; margin-right: auto;}
    .hero-title {font-size: 3rem; line-height: 1.02; color: #f5e7b3; margin-bottom: 18px;}
    .hero-copy {font-size: 1.05rem; color: #d2c58b; max-width: 700px;}
    .hero-cta {display: inline-flex; align-items: center; gap: 10px; padding: 12px 24px; background: rgba(200,16,46,0.2); border: 1px solid rgba(200,16,46,0.35); border-radius: 999px; color: #f4d48d; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; margin-top: 24px;}
    .glass-card {background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(212,175,55,0.18); border-radius: 22px; backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); transition: transform 0.28s ease, box-shadow 0.28s ease; margin-bottom: 24px;}
    .glass-card:hover {transform: scale(1.04); box-shadow: 0 22px 64px rgba(200,16,46,0.26);}
    .country-grid {display:grid; grid-template-columns: repeat(4,minmax(220px,1fr)); gap: 18px; margin: 0 auto 28px; max-width: 1200px;}
    .country-card {padding: 20px; text-align:center; min-height: 240px;}
    .country-card img {border-radius: 16px; margin-bottom: 16px;}
    .country-card h4 {margin: 0 0 10px; color: #f4e1a2;}
    .country-card p {margin: 0; color: #d7c88e; line-height: 1.5; font-size: 0.95rem;}
    .player-grid {display:grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: 26px; margin-bottom: 44px;}
    .player-card {padding: 0; overflow:hidden; margin-bottom: 18px;}
    .player-card img {border-radius: 0; width: 100%; display:block; object-fit: cover;}
    .player-card-body {padding: 20px;}
    .player-card h4 {margin: 0 0 10px; color: #f4de9e;}
    .player-card p {margin: 0; color: #d4c78f;}
    .stat-carousel {display:flex; gap:16px; overflow-x:auto; padding-bottom:12px; margin-top: 16px;}
    .stat-card {min-width: 235px; padding: 22px; display:flex; flex-direction:column; justify-content:space-between;}
    .stat-card h4 {margin: 0 0 10px; font-size: 0.9rem; color: #d4af37; letter-spacing: 0.09em; text-transform: uppercase;}
    .stat-card strong {font-size: 2.6rem; color: #fff; line-height:1;}
    .stat-card span {color: #d8c77e;}
    .leaderboard-grid {display:grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 22px; margin-top:24px;}
    .leaderboard-card {padding: 22px;}
    .leaderboard-title {font-size: 1rem; margin-bottom: 18px; color: #f4e3ad; letter-spacing: 0.08em; text-transform: uppercase;}
    .leaderboard-table {width:100%; border-collapse: collapse; color:#eef1f5; font-size:0.95rem;}
    .leaderboard-table th, .leaderboard-table td {padding: 12px 10px; text-align:left; border-bottom: 1px solid rgba(255,255,255,0.08);}
    .leaderboard-table th {color:#d4af37; font-weight:700;}
    .leaderboard-table tbody tr:hover {background: rgba(255,255,255,0.05);}
    .team-pill {display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:999px; background: rgba(255,255,255,0.08); color:#fff; font-size:0.82rem;}
    .team-pill::before {content:'★'; color:#c8102e;}
    .team-flag {height: 18px; width: auto; border-radius: 3px; margin-right: 8px; vertical-align: middle;}
    .team-overview-row {display:grid; grid-template-columns: repeat(3,minmax(240px,1fr)); gap:18px; margin-bottom: 20px;}
    .section-header h2 {margin: 0 0 10px; font-size: 2rem; color: #f5e4a5;}
    .section-header p {margin: 0; color: #cfc09e;}
    .section-header p {margin: 0; color: #cfc09e;}
    </style>
    ''',
    unsafe_allow_html=True,
)

st.markdown(
    '''
    <div class="hero-row">
      <div class="header-box glass-card">
        <div class="hero-title">World Cup 2026 Analytics Hub</div>
        <div class="hero-copy">Track elite international performers, compare top nations, and explore premium football data visualizations in a modern dark mode layout.</div>
        <div class="hero-cta">Live FBref scouting</div>
      </div>
    </div>
    ''',
    unsafe_allow_html=True,
)


def build_headers(header_rows: list[list[str]]) -> list[str]:
    headers: list[str] = []
    max_len = max(len(row) for row in header_rows)
    for i in range(max_len):
        parts = [row[i].strip() if i < len(row) else '' for row in header_rows]
        primary = parts[0]
        secondary = parts[1]
        tertiary = parts[2] if len(parts) > 2 else ''
        if primary and secondary:
            headers.append(f'{primary}_{secondary}')
        elif primary:
            headers.append(primary)
        elif secondary:
            headers.append(secondary)
        else:
            headers.append(tertiary)
    return [header.strip('_') for header in headers]


def read_fbref_csv(path: str) -> pd.DataFrame:
    with open(path, encoding='utf-8-sig', newline='') as handle:
        reader = csv.reader(handle)
        header_rows = [next(reader) for _ in range(3)]
        headers = build_headers(header_rows)
        rows = list(reader)

    # FBref CSVs often include a fourth row of repeated column labels after the header rows.
    if rows and len(rows[0]) >= 4:
        first_row_lower = [cell.strip().lower() for cell in rows[0][:4]]
        if first_row_lower == ['league', 'season', 'team', 'player']:
            rows = rows[1:]

    df = pd.DataFrame(rows, columns=headers)

    def convert_if_numeric(series: pd.Series) -> pd.Series:
        values = series.astype(str).str.strip()
        nonempty = values[values != '']
        if nonempty.empty:
            return series
        if nonempty.str.match(r'^[+-]?(\d+)(\.\d+)?$').all():
            return pd.to_numeric(values, errors='coerce')
        return series

    return df.apply(convert_if_numeric)


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            '_'.join([str(item) for item in col if item and str(item) != '']).strip('_')
            for col in df.columns
        ]
    return df


def find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
    lowered = {str(col).lower(): col for col in df.columns}
    for candidate in candidates:
        candidate_low = candidate.lower()
        for col_low, col in lowered.items():
            if candidate_low in col_low:
                return col
    return None


def get_flag_url(nation: str) -> str | None:
    if not nation or not isinstance(nation, str):
        return None
    norm = nation.lower().strip()
    norm = norm.replace('–', ' ').replace('-', ' ').replace(' and ', ' ').replace('&', ' ').replace('  ', ' ')
    norm = norm.replace("’", "'").replace("'", '').replace('.', '')
    norm = norm.replace('é', 'e').replace('á', 'a').replace('ó', 'o').replace('í', 'i').replace('ú', 'u').replace('ç', 'c').replace('ã', 'a').replace('ô', 'o')
    mapping = {
        'algeria': 'dz','argentina': 'ar','australia': 'au','austria': 'at','belgium': 'be',
        'bosnia herzegovina': 'ba','bosnia herz': 'ba','brazil': 'br','cabo verde': 'cv','canada': 'ca',
        'colombia': 'co','costa rica': 'cr','croatia': 'hr','czech republic': 'cz','denmark': 'dk',
        'ecuador': 'ec','england': 'gb','france': 'fr','germany': 'de','ghana': 'gh','iran': 'ir',
        'italy': 'it','japan': 'jp','mexico': 'mx','morocco': 'ma','netherlands': 'nl','nigeria': 'ng',
        'norway': 'no','peru': 'pe','poland': 'pl','portugal': 'pt','qatar': 'qa','saudi arabia': 'sa',
        'senegal': 'sn','serbia': 'rs','spain': 'es','switzerland': 'ch','tunisia': 'tn','uruguay': 'uy',
        'paraguay': 'py','curacao': 'cw','cote divoire': 'ci','cotedivoire': 'ci','ir iran': 'ir',
        'usa': 'us','united states': 'us','united kingdom': 'gb','wales': 'gb','scotland': 'gb','ireland': 'ie',
        'north macedonia': 'mk'
    }
    if norm in mapping:
        return f'https://flagcdn.com/w80/{mapping[norm]}.png'
    if 'united states' in norm or 'usa' in norm:
        return 'https://flagcdn.com/w80/us.png'
    if 'korea' in norm:
        return 'https://flagcdn.com/w80/kr.png'
    if 'saudi' in norm:
        return 'https://flagcdn.com/w80/sa.png'
    if 'cabo' in norm or 'verde' in norm:
        return 'https://flagcdn.com/w80/cv.png'
    if 'bosnia' in norm:
        return 'https://flagcdn.com/w80/ba.png'
    if 'united' in norm and 'kingdom' in norm:
        return 'https://flagcdn.com/w80/gb.png'
    return None


def get_flag_html(nation: str) -> str:
    url = get_flag_url(nation)
    if url:
        return f'<img class="team-flag" src="{url}" alt="{nation} flag"/>'
    return ''


def safe_top(df: pd.DataFrame, column: str | None, n: int = 5, extra_cols: list[str] | None = None) -> pd.DataFrame:
    if column is None or column not in df.columns:
        return pd.DataFrame(
            [{'player': 'N/A', 'team': 'N/A', 'stat': 'Unavailable'}] * n
        )
    cols = ['player', 'team'] + (extra_cols or [])
    cols = [col for col in cols if col in df.columns] + [column]
    result = df.sort_values(column, ascending=False).head(n)[cols].reset_index(drop=True)
    return result.loc[:, ~result.columns.duplicated()]


def safe_bottom(df: pd.DataFrame, column: str | None, n: int = 5, extra_cols: list[str] | None = None) -> pd.DataFrame:
    if column is None or column not in df.columns:
        return pd.DataFrame(
            [{'team': 'N/A', 'stat': 'Unavailable'}] * n
        )
    cols = ['team'] + (extra_cols or [])
    cols = [col for col in cols if col in df.columns] + [column]
    result = df.sort_values(column, ascending=True).head(n)[cols].reset_index(drop=True)
    return result.loc[:, ~result.columns.duplicated()]

# Sidebar controls
st.sidebar.title('🏆 World Cup 2026 Analysis')
st.sidebar.header('Player analysis')

player_standard = read_fbref_csv('player_standard.csv')
player_misc = read_fbref_csv('player_misc.csv')
player_keeper = read_fbref_csv('player_keeper.csv')
team_standard = read_fbref_csv('team_standard.csv')
team_misc = read_fbref_csv('team_misc.csv')
team_keeper = read_fbref_csv('team_keeper.csv')


goal_col = find_column(player_standard, ['Performance_Gls', 'Performance_Goals', 'Gls', 'Goals'])
assist_col = find_column(player_standard, ['Performance_Ast', 'Assists', 'Ast'])
tackle_col = find_column(player_misc, ['Performance_TklW', 'TklW', 'Tackles'])
save_col = find_column(player_keeper, ['Performance_Saves', 'Saves'])
conceded_col = find_column(team_keeper, ['Performance_GA', 'GA', 'Goals Against', 'GoalsAllowed', 'GA_x', 'opp_Goals'])
conceded_source = team_keeper if conceded_col is not None else team_standard
minutes_mp_col = find_column(player_standard, ['Playing Time_MP', 'MP', 'Matches'])
minutes_90_col = find_column(player_standard, ['Playing Time_90s', '90s', 'Minutes'])

if goal_col is None or assist_col is None or tackle_col is None or save_col is None or minutes_mp_col is None or minutes_90_col is None:
    st.error('Unable to locate one or more required FBref statistic columns. Please verify the data load and column mapping.')
    st.stop()

nation_options = sorted(player_standard['nation'].dropna().unique())
selected_nation = st.sidebar.selectbox('Select nation', nation_options)
player_options = sorted(player_standard.loc[player_standard['nation'] == selected_nation, 'player'].dropna().unique())
selected_player = st.sidebar.selectbox('Select player', player_options)
flag_url = get_flag_url(selected_nation)
if flag_url:
    st.sidebar.image(flag_url, width=110, caption=selected_nation)

player_analysis = player_standard[player_standard['player'] == selected_player].copy()
player_analysis['Goals per Match'] = np.where(
    player_analysis[minutes_mp_col].fillna(0) > 0,
    player_analysis[goal_col].fillna(0) / player_analysis[minutes_mp_col],
    0,
)
player_analysis['Goals per 90'] = np.where(
    player_analysis[minutes_90_col].fillna(0) > 0,
    player_analysis[goal_col].fillna(0) / player_analysis[minutes_90_col],
    0,
)

player_standard['GoalsAssists'] = player_standard[goal_col].fillna(0) + player_standard[assist_col].fillna(0)

best_goal = safe_top(player_standard, goal_col, 1)
best_ga = safe_top(player_standard, 'GoalsAssists', 1)
best_tackle = safe_top(player_misc, tackle_col, 1)
best_save = safe_top(player_keeper, save_col, 1)

card_html = '<div class="player-grid">'
for title, df, stat_col, unit in [
    ('Most goals scored', best_goal, goal_col, ''),
    ('Most G/A', best_ga, 'GoalsAssists', ''),
    ('Most tackles', best_tackle, tackle_col, ''),
    ('Most saves', best_save, save_col, ''),
]:
    row = df.iloc[0] if not df.empty else None
    player = row['player'] if row is not None else 'N/A'
    stat = row[stat_col] if row is not None and stat_col in row else 'N/A'
    team = row['team'] if row is not None and 'team' in row else ''
    label = f'<div style="font-size:0.85rem; letter-spacing:0.12em; color:#d4af37; text-transform:uppercase; margin-bottom:12px;">{title}</div>'
    value = f'<div style="font-size:2.4rem; color:#fff; margin-bottom:10px;">{stat}</div>'
    details = f'<div style="color:#d7c88e;">{player} {f"· {team}" if team else ""}</div>'
    card_html += f'<div class="player-card glass-card"><div class="player-card-body">{label}{value}{details}</div></div>'
card_html += '</div>'
st.markdown(card_html, unsafe_allow_html=True)

st.markdown('<div class="section-header"><h2>Player leaderboards</h2><p>Top performers across goals, assists, tackles and saves.</p></div>', unsafe_allow_html=True)

def render_leaderboard_html(df: pd.DataFrame, title: str, headers: dict[str, str]) -> str:
    html = f'<div class="leaderboard-card glass-card"><div class="leaderboard-title">{title}</div>'
    html += '<div class="data-grid"><table class="leaderboard-table"><thead><tr>'
    for label in headers.values():
        html += f'<th>{label}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for key in headers.keys():
            value = row.get(key, '')
            if key == 'team' and pd.notna(value):
                flag = get_flag_html(value)
                html += f'<td><span class="team-pill">{flag}{value}</span></td>'
            else:
                html += f'<td>{value}</td>'
        html += '</tr>'
    html += '</tbody></table></div></div>'
    return html

player_goals = safe_top(player_standard, goal_col, 5, extra_cols=['Performance_Ast'])
player_tackles = safe_top(player_misc, tackle_col, 5)
player_assists = safe_top(player_standard, assist_col, 5)
player_saves = safe_top(player_keeper, save_col, 5)

st.markdown('<div class="leaderboard-grid">', unsafe_allow_html=True)
st.markdown(render_leaderboard_html(player_goals, 'Most goals scored', {'player': 'Player', 'team': 'Team', 'Performance_Ast': 'Assists', goal_col: 'Goals'}), unsafe_allow_html=True)
st.markdown(render_leaderboard_html(player_tackles, 'Most tackles done', {'player': 'Player', 'team': 'Team', tackle_col: 'Tackles Won'}), unsafe_allow_html=True)
st.markdown(render_leaderboard_html(player_assists, 'Most assists', {'player': 'Player', 'team': 'Team', assist_col: 'Assists'}), unsafe_allow_html=True)
st.markdown(render_leaderboard_html(player_saves, 'Most saves by GK', {'player': 'Player', 'team': 'Team', save_col: 'Saves'}), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header"><h2>Player analysis</h2><p>Inspect the selected player with premium stat cards and charts.</p></div>', unsafe_allow_html=True)
if not player_analysis.empty:
    summary_stats = [
        {'label': 'Total Goals', 'value': int(player_analysis[goal_col].iloc[0])},
        {'label': 'Total Assists', 'value': int(player_analysis[assist_col].iloc[0])},
        {'label': 'Matches Played', 'value': int(player_analysis[minutes_mp_col].iloc[0])},
        {'label': 'Goals per 90', 'value': round(float(player_analysis['Goals per 90'].iloc[0]), 2)},
    ]

    st.markdown(
        f'<div class="glass-card"><div class="leaderboard-title">{selected_player} - {selected_nation}</div><p style="color:#d3c68d; margin-top:10px;">Detailed campaign metrics and performance summaries with a modern dark UI.</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="stat-carousel">', unsafe_allow_html=True)
    for card in summary_stats:
        st.markdown(
            f'<div class="stat-card glass-card"><h4>{card["label"]}</h4><strong>{card["value"]}</strong><span>Current campaign</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    goals_vs_appearances = player_analysis.set_index('player')[[goal_col, minutes_mp_col]].rename(columns={goal_col: 'Goals', minutes_mp_col: 'Appearances'})
    goals_per_90 = player_analysis.set_index('player')[['Goals per 90']]

    fig_perf = px.bar(
        goals_vs_appearances.reset_index(),
        x='player',
        y=['Goals', 'Appearances'],
        title='Goals vs Appearances',
        color_discrete_sequence=['#d4af37', '#c8102e'],
    )
    fig_perf.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f5f1da',
        title_font_color='#d4af37',
        legend_title_text='',
        xaxis=dict(showgrid=False, linecolor='rgba(255,255,255,0.12)'),
        yaxis=dict(showgrid=False, linecolor='rgba(255,255,255,0.12)'),
    )

    fig_goals90 = px.bar(
        goals_per_90.reset_index(),
        x='player',
        y='Goals per 90',
        title='Goals per 90',
        color_discrete_sequence=['#c8102e'],
    )
    fig_goals90.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f5f1da',
        title_font_color='#d4af37',
        xaxis=dict(showgrid=False, linecolor='rgba(255,255,255,0.12)'),
        yaxis=dict(showgrid=False, linecolor='rgba(255,255,255,0.12)'),
    )

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_perf, use_container_width=True)
    with col2:
        st.plotly_chart(fig_goals90, use_container_width=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    nation_data = player_standard[player_standard['nation'] == selected_nation].copy()
    nation_misc = player_misc[['player', 'team', tackle_col]].copy()
    nation_data = nation_data.merge(nation_misc, on=['player', 'team'], how='left')
    nation_data = nation_data.sort_values(assist_col, ascending=False).head(10)
    if not nation_data.empty:
        fig = px.bar(
            nation_data,
            x='player',
            y=assist_col,
            title=f'Top 10 assist providers for {selected_nation}',
            labels={assist_col: 'Assists', 'player': 'Player'},
            color_discrete_sequence=['#d4af37'],
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f1da',
            title_font_color='#d4af37',
            xaxis=dict(showgrid=False, linecolor='rgba(255,255,255,0.12)'),
            yaxis=dict(showgrid=False, linecolor='rgba(255,255,255,0.12)'),
        )
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            top_assist_pie = nation_data.sort_values(assist_col, ascending=False).head(6)
            fig_assist_pie = px.pie(
                top_assist_pie,
                names='player',
                values=assist_col,
                title=f'Assist share among top {len(top_assist_pie)} of {selected_nation}',
                color_discrete_sequence=px.colors.sequential.Agsunset,
            )
            fig_assist_pie.update_traces(textposition='inside', textinfo='percent+label', rotation=90, domain=dict(x=[0.06,0.78]))
            fig_assist_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f1da',
                title_font_color='#d4af37',
                legend_title_text='',
                autosize=True,
                margin=dict(l=8, r=8, t=40, b=8),
                legend=dict(orientation='v', x=0.92, xanchor='left', y=0.5, font=dict(color='#f5f1da')),
            )
            st.plotly_chart(fig_assist_pie, use_container_width=True)

        col11, col12 = st.columns(2)

        shared_domain = dict(x=[0.05, 0.75])
        shared_legend = dict(orientation='v', x=0.85, xanchor='left', y=0.5, font=dict(color='#f5f1da'))
        shared_margin = dict(l=8, r=8, t=40, b=8)

        with col11:
            top_tackle_pie = nation_data.sort_values(tackle_col, ascending=False).head(6)
            fig_tackle_pie = px.pie(
                top_tackle_pie,
                names='player',
                values=tackle_col,
                title=f'Tackle share among top {len(top_tackle_pie)} of {selected_nation}',
                color_discrete_sequence=px.colors.sequential.Agsunset,
            )
            fig_tackle_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                rotation=90,
                domain=shared_domain
            )
            fig_tackle_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f1da',
                title_font_color='#d4af37',
                legend_title_text='',
                autosize=True,
                margin=shared_margin,
                legend=shared_legend,
            )
            st.plotly_chart(fig_tackle_pie, use_container_width=True)

        with col12:
            run_candidates = ['Performance_Runs', 'Runs', 'Carries', 'Carry', 'Progressive Carries', 'Dribbles', 'Dribble']
            run_col = find_column(player_misc, run_candidates) or find_column(player_standard, run_candidates)

            if run_col is not None:
                run_by_team = player_misc.groupby('team', as_index=False)[run_col].sum().sort_values(run_col, ascending=False).head(8)
                chart_label = 'Runs'
                chart_title = f'Total {chart_label} by team'
                value_col = run_col
            else:
                run_by_team = player_standard.groupby('team', as_index=False)[goal_col].sum().sort_values(goal_col, ascending=False).head(8)
                chart_label = 'Goals'
                chart_title = f'Total {chart_label} by team (runs unavailable)'
                value_col = goal_col

            fig_run_team = None
            if not run_by_team.empty:
                fig_run_team = px.pie(
                    run_by_team,
                    names='team',
                    values=value_col,
                    title=chart_title,
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                )
                fig_run_team.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    domain=shared_domain
                )
                fig_run_team.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#f5f1da',
                    title_font_color='#d4af37',
                    legend_title_text='',
                    autosize=True,
                    margin=shared_margin,
                    legend=shared_legend,
                )
                st.plotly_chart(fig_run_team, use_container_width=True)

        heatmap_cols = [goal_col, assist_col]
        if 'Performance_G+A' in nation_data.columns:
            heatmap_cols.append('Performance_G+A')
        if minutes_mp_col in nation_data.columns:
            heatmap_cols.append(minutes_mp_col)
        heatmap_cols = [col for col in heatmap_cols if col in nation_data.columns]

        heatmap_data = nation_data.sort_values(goal_col, ascending=False).head(8)[['player'] + heatmap_cols].fillna(0)
        if not heatmap_data.empty and heatmap_cols:
            heatmap_df = heatmap_data.set_index('player')
            fig_heat = px.imshow(
                heatmap_df,
                labels=dict(x='Stat', y='Player', color='Value'),
                x=heatmap_df.columns,
                y=heatmap_df.index,
                aspect='auto',
                color_continuous_scale=px.colors.sequential.Agsunset,
                title=f'Standard stat heatmap for top {len(heatmap_df)} players in {selected_nation}',
            )
            fig_heat.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#f5f1da',
                title_font_color='#d4af37',
            )
            fig_heat.update_traces(colorbar=dict(tickfont_color='#f5f1da'))
            if fig_run_team is not None:
                try:
                    fig_run_team.update_traces(rotation=180)
                except Exception:
                    pass
                st.plotly_chart(fig_run_team, use_container_width=True)
            else:
                st.markdown("<p style='color:#d7c88e;'>No team run/goal data available.</p>", unsafe_allow_html=True)
            st.plotly_chart(fig_heat, use_container_width=True)

        fig3d = px.scatter_3d(
            nation_data,
            x=goal_col,
            y=assist_col,
            z=tackle_col,
            color='player',
            size=minutes_mp_col,
            title=f'3D view: Goals, Assists and Tackles for {selected_nation}',
            labels={
                goal_col: 'Goals',
                assist_col: 'Assists',
                tackle_col: 'Tackles Won',
                minutes_mp_col: 'Matches',
            },
        )
        fig3d.update_traces(marker=dict(size=6, line=dict(width=1, color='#f5e1a3')))
        fig3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#f5f1da',
            title_font_color='#d4af37',
            margin=dict(l=24, r=24, t=60, b=24),
            scene=dict(
                aspectmode='cube',
                xaxis=dict(gridcolor='rgba(255,255,255,0.12)', backgroundcolor='rgba(0,0,0,0)', showbackground=False, zerolinecolor='rgba(255,255,255,0.08)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.12)', backgroundcolor='rgba(0,0,0,0)', showbackground=False, zerolinecolor='rgba(255,255,255,0.08)'),
                zaxis=dict(gridcolor='rgba(255,255,255,0.12)', backgroundcolor='rgba(0,0,0,0)', showbackground=False, zerolinecolor='rgba(255,255,255,0.08)'),
            ),
        )
        st.plotly_chart(fig3d, use_container_width=True, height=720)
    else:
        st.markdown('<p style="color:#d7c88e;">No assist data available for this nation.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="glass-card"><p style="color:#d7c88e;">No stats available for the selected player.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header"><h2>Team leaderboards</h2><p>Leading teams in goals, tackles, assists and saves.</p></div>', unsafe_allow_html=True)

team_goals = safe_top(team_standard, goal_col, 5, extra_cols=['team'])
team_goals = team_goals.loc[:, ~team_goals.columns.duplicated()]
team_tackles = safe_top(team_misc, tackle_col, 5, extra_cols=['team'])
team_tackles = team_tackles.loc[:, ~team_tackles.columns.duplicated()]
team_assists = safe_top(team_standard, assist_col, 5, extra_cols=['team'])
team_assists = team_assists.loc[:, ~team_assists.columns.duplicated()]
team_saves = safe_top(team_keeper, save_col, 5, extra_cols=['team'])
team_saves = team_saves.loc[:, ~team_saves.columns.duplicated()]
team_conceded = safe_bottom(conceded_source, conceded_col, 5, extra_cols=['team']) if conceded_col is not None else pd.DataFrame()
team_conceded = team_conceded.loc[:, ~team_conceded.columns.duplicated()]

if not team_goals.empty and not team_tackles.empty and not team_saves.empty:
    overview_html = '<div class="team-overview-row">'
    for title, df, stat_col in [
        ('Highest team goals', team_goals, goal_col),
        ('Highest team tackles', team_tackles, tackle_col),
        ('Highest team saves', team_saves, save_col),
    ]:
        row = df.iloc[0]
        team_name = row['team'] if 'team' in row else 'N/A'
        stat_value = row[stat_col] if stat_col in row else 'N/A'
        flag = get_flag_html(team_name)
        overview_html += (
            f'<div class="player-card glass-card"><div class="player-card-body">'
            f'<div style="font-size:0.85rem; letter-spacing:0.12em; color:#d4af37; margin-bottom:12px;">{title}</div>'
            f'<div style="font-size:2.4rem; color:#fff; margin-bottom:10px;">{stat_value}</div>'
            f'<div style="color:#d7c88e;">{flag}{team_name}</div>'
            '</div></div>'
        )
    overview_html += '</div>'
    st.markdown(overview_html, unsafe_allow_html=True)

st.markdown('<div class="leaderboard-grid">', unsafe_allow_html=True)
st.markdown(render_leaderboard_html(team_goals, 'Team goals scored', {'team': 'Team', goal_col: 'Goals'}), unsafe_allow_html=True)
st.markdown(render_leaderboard_html(team_tackles, 'Team tackles done', {'team': 'Team', tackle_col: 'Tackles Won'}), unsafe_allow_html=True)
st.markdown(render_leaderboard_html(team_assists, 'Team assists', {'team': 'Team', assist_col: 'Assists'}), unsafe_allow_html=True)
st.markdown(render_leaderboard_html(team_saves, 'Team saves by GK', {'team': 'Team', save_col: 'Saves'}), unsafe_allow_html=True)
if not team_conceded.empty:
    st.markdown(render_leaderboard_html(team_conceded, 'Top 5 teams with least conceded goals', {'team': 'Team', conceded_col: 'Goals Conceded'}), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
