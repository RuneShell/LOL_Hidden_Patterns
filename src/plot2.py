import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import platform

# --- (이전 설정 부분 동일) ---
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
else:
    plt.rc('font', family='AppleGothic')

plt.rcParams['axes.unicode_minus'] = False

tier_order = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Emerald', 'Diamond', 'Master', 'Grandmaster', 'Challenger']
tier_colors = {
    'Iron': '#51484a', 'Bronze': '#8c513a', 'Silver': '#80989d', 'Gold': '#cd8837',
    'Platinum': '#4e9996', 'Emerald': '#278853', 'Diamond': '#576bce',
    'Master': '#9d48e0', 'Grandmaster': '#c7262c', 'Challenger': '#4eb5ff'
}

def preprocess_data(df):
    df.columns = [str(col).strip() for col in df.columns]
    df['win'] = df['win'].astype(float)
    df['lose'] = df['lose'].astype(float)
    df['total_games'] = df['win'] + df['lose']
    
    if df['win_rate'].dtype == object:
        df['win_rate'] = df['win_rate'].str.replace('%', '').astype(float)
        
    df['tier'] = pd.Categorical(df['tier'], categories=tier_order, ordered=True)
    df['level'] = df['level'].astype(float)
    return df

def draw_lol_seaborn_plots(df):
    df = preprocess_data(df)
    sns.set_theme(style="whitegrid", font='Malgun Gothic', rc={"axes.unicode_minus": False})
    
    fig, axes = plt.subplots(3, 2, figsize=(13, 20))
    fig.suptitle('League of Legends 티어 데이터 분석 (검은 점: 평균값)', fontsize=22, fontweight='bold')

    plot_configs = [
        ['type', 'level', '유형별 레벨 분포'],
        ['tier', 'total_games', '티어별 총 판 수'],
        ['level', 'total_games', '레벨 vs 총 판 수'],
        ['tier', 'win_rate', '티어별 승률 (%)'],
        ['level', 'win_rate', '레벨 vs 승률 (%)'],
        ['total_games', 'win_rate', '총 판 수 vs 승률 (%)']
    ]

    for i, config in enumerate(plot_configs):
        row, col = divmod(i, 2)
        ax = axes[row, col]
        x_col, y_col, title = config
        
        if x_col in df.columns:
            # 1. 전체 데이터 산점도
            sns.scatterplot(
                data=df, x=x_col, y=y_col, 
                hue='tier', palette=tier_colors, 
                ax=ax, s=40, alpha=0.5, legend=(i == 1)
            )
            
            # 2. 평균값 계산 및 표시 (추가된 부분)
            # x축 컬럼으로 그룹화하여 y축 컬럼의 평균 계산
            means = df.groupby(x_col, observed=True)[y_col].mean().reset_index()
            
            sns.scatterplot(
                data=means, x=x_col, y=y_col,
                color='black', s=100, marker='X', # 검은색 'X' 모양으로 강조
                ax=ax, label='Mean' if i == 1 else None, # 범례 하나에만 표시
                zorder=10 # 다른 점들보다 위에 그리도록 설정
            )
            
        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.set_xlabel(x_col.replace('_', ' ').capitalize())
        ax.set_ylabel(y_col.replace('_', ' ').capitalize())

        if x_col == 'tier':
            ax.set_xticks(range(len(tier_order)))
            ax.set_xticklabels(tier_order, rotation=45)

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    
    handles, labels = axes[0, 1].get_legend_handles_labels()
    fig.legend(handles, labels, title='Tiers & Mean', bbox_to_anchor=(1.02, 0.5), loc='center left')
    
    plt.savefig('output_with_means.jpg', dpi=450, bbox_inches='tight')
    print("그래프가 output_with_means.jpg로 저장되었습니다.")

# --- 데이터 불러오기 및 실행 ---
try:
    df_challenger = pd.read_excel('제목 없는 스프레드시트.xlsx', sheet_name='Challenger')
    draw_lol_seaborn_plots(df_challenger)
except Exception as e:
    print(f"오류 발생: {e}")