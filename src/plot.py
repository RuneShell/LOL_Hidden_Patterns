import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 티어 순서 및 색상 정의 (리그 오브 레전드 공식 테마 색상 참고)
tier_order = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Emerald', 'Diamond', 'Master', 'Grandmaster', 'Challenger']
tier_colors = {
    'Iron': '#51484a', 'Bronze': '#8c513a', 'Silver': '#80989d', 'Gold': '#cd8837',
    'Platinum': '#4e9996', 'Emerald': '#278853', 'Diamond': '#576bce',
    'Master': '#9d48e0', 'Grandmaster': '#c7262c', 'Challenger': '#4eb5ff'
}

# 2. 데이터 전처리
def preprocess_data(df):
    # 'win'과 'lose'를 더해 '플레이한 판 수' 생성 [1, 2]
    df['win'] = df['win'].astype(float)
    df['lose'] = df['lose'].astype(float)
    df['total_games'] = df['win'] + df['lose']
    
    # 'win_rate' 문자열에서 '%' 제거 후 실수형 변환 [1, 3]
    if df['win_rate'].dtype == object:
        df['win_rate'] = df['win_rate'].str.replace('%', '').astype(float)
        
    # 티어 순서 고정을 위한 Categorical 설정
    df['tier'] = pd.Categorical(df['tier'], categories=tier_order, ordered=True)

    #
    df['level'] = df['level'].astype(float)
    #print(df.head())
    return df

# 3. 6개의 scatter plot 그리기 (Seaborn 활용)
def draw_lol_seaborn_plots(df):
    df = preprocess_data(df)
    
    # 스타일 설정
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(3, 2, figsize=(13, 20))
    fig.suptitle('League of Legends Tier Data Analysis', fontsize=22, fontweight='bold')

    # 플롯 정보 리스트 [x축, y축, 제목]
    plot_configs = [
        ['tier', 'level', 'Tier vs Level'],
        ['tier', 'total_games', 'Tier vs Total Games'],
        ['level', 'total_games', 'Level vs Total Games'],
        ['tier', 'win_rate', 'Tier vs Win Rate (%)'],
        ['level', 'win_rate', 'Level vs Win Rate (%)'],
        ['total_games', 'win_rate', 'Total Games vs Win Rate (%)']
    ]

    for i, config in enumerate(plot_configs):
        row, col = divmod(i, 2)
        ax = axes[row, col]
        
        # Seaborn scatterplot 실행
        sns.scatterplot(
            data=df, x=config[0], y=config[1], 
            hue='tier', palette=tier_colors, 
            ax=ax, s=20, alpha=0.6, legend=(i == 0) # 첫 번째 그래프에만 범례 표시
        )
        
        ax.set_title(config[2], fontsize=15, fontweight='bold')
        ax.set_xlabel(config[0].replace('_', ' ').capitalize())
        ax.set_ylabel(config[1].replace('_', ' ').capitalize())

        # 티어 축(x축) 라벨 정렬
        if config[0] == 'tier':
            ax.set_xticklabels(tier_order, rotation=45)

    # 전체 레이아웃 조정 및 범례 위치 설정
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    fig.legend(title='Tiers', bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.show()
    plt.savefig('output.jpg', dpi=450)



excel_data = pd.read_excel('output.xlsx', sheet_name=None)
concat_df = pd.concat(excel_data.values(), ignore_index=True)
#print(concat_df[concat_df['tier'] == 'Emerald'])
draw_lol_seaborn_plots(concat_df)