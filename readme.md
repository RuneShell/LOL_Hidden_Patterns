# `League of Legends` hidden patterns
A project to **identify undiscovered patterns** in the world, for `Hidden Pattern(숨겨진 패턴)` course in Kyung Hee University.

<br/>

> [League of Legends](https://www.leagueoflegends.com/) is a 5v5 MOBA where teams face off to destroy the enemy's Nexus.

## Brief

### Data
I crawled 8,921 profiles from [OP.GG](https://op.gg/) using python `selenium`. <small><small>(2026-01-04, Korean server)

### Distribution
| Tier          | Data Count |
| ----          | ----  |
| Challenger    | 295[^1]   |
| Grandmaster   | 695[^1]   |
| Master        | 994[^1]   |
| Diamond       | 999       |
| Emerald       | 995       |
| Platinum      | 985       |
| Gold          | 992       |
| Silver        | 985       |
| Bronze        | 997       |
| Iron          | 984       |
| **Total**     | **8921**  | 

[^1]: Maximim *summoner* count is limited.

### data head
| ranking | name       | tag   | tier       | LP   | most1 | most2 | most3 | level | win | lose | games | win_rate |
| ------- | ---------- | ------ | ---------- | ---- | ---: | ---: | ---: | ----: | --: | ---: | ----: | -------- |
| 1       | moment     |  #0619| Challenger | 2041 | 비에고   | 암베사   | 제이스   | 90    | 405 | 252  | 657   | 62%       |
| 2       | DK Sharvel | #KR1  | Challenger | 2040 | 바이    | 키아나   | 판테온   | 965   | 729 | 584  | 1313  | 56%      |
| 3       | T1 Guardian| #KR3  | Challenger | 1967 | 암베사   | 크산테   | 럼블    | 496   | 898 | 763  | 1661  | 54%      |
| 4       | Phantasm   | #RANK1| Challenger | 1950 | 아크샨   | 퀸     | 흐웨이   | 74    | 304 | 170  | 474   | 64%      |

</small></small>



## Limitations
- 1 week long project


## Charts


#### 01. Relationship Heatmap between numerical columns

![img](https://github.com/RuneShell/LOL_Hidden_Patterns/tree/main/analysis/01._relationship_heapmap.png)

> 0 : no clear relationship </br>
> 1 : clear relationship

I found no clear hidden relationships here..
</br></br>

#### 02. Relationships between `[tier, level, total_games, win_rate]`

![img](https://github.com/RuneShell/LOL_Hidden_Patterns/tree/main/analysis/02._relationships_without_name.jpg)
</br></br>

#### 03. `name` Morphological Analysis
using `fastText`

[**Nickname Embedding Cluster by game Tier**](https://htmlpreview.github.io/?https://github.com/RuneShell/LOL_Hidden_Patterns/tree/main/analysis/03._name_morphological_analysis)
</br>
I found no clear relationship between `tier` ↔ `name (morphological)`. <br>
So we decided to analize relationship `tier` ↔ `name (semantic)`. 
</br></br>

#### 04. Preprocessing : `name` semantic classification
Our team classified the names into 9 semantic classes using [Genspark AI](https://www.genspark.ai/).

* `Neutral (중립적)`: Types where no specific emotion or personality is revealed, such as common nouns, personal names, or meaningless word combinations.
* `Aggressive (공격적)`: Types that express hostility, including profanity, slurs, threats to others, or harsh language.
* `Cute/Friendly (귀여운)`: Friendly expressions that include onomatopoeia/mimetic words, cute sentence endings, or refer to adorable subjects.
* `Sexual (선정적)`: Types intended to draw attention by including sexual slang or provocative expressions.
* `Insincere (성의없는)`: Types with low engagement and no meaningful structure, such as 'asdf', 'qwer', or random sequences of consonants.
* `Pessimistic (암울한)`: Types that reflect a negative self-image, revealing self-deprecating, cynical, or defeatist emotions.
* `Humorous (유머러스)`: Types that induce laughter by utilizing wordplay, parodies, or internet memes. 
* `Character (캐릭터)`: Types that directly adopt the names of in-game champions or animation characters.
* `Professional (프로팀)`: Types that express a sense of belonging by mimicking the nicknames or formats of famous pro gamers or teams (e.g., T1, GEN).

> *I know this classifacation is somewhat crude, but we had only 2 days limit for data analysis. I wished to classifty names into 32 classes with continuous score, not a discrete classes for machine learning.*

<small><small>

| ranking | name        | tag    | tier       | LP   | most1 | most2 | most3 | level | win | lose | win_rate | role   | type |
|---------|-------------|--------|------------|------|-------|-------|-------|-------|-----|------|----------|--------|------|
| 1       | moment      | #0619  | Challenger | 2041 | 비에고   | 암베사   | 제이스   | 90    | 405 | 252  | 62%      | 전사     | 중립적  |
| 2       | DK Sharvel  | #KR1   | Challenger | 2040 | 바이    | 키아나   | 판테온   | 965   | 729 | 584  | 5<<6%      | 전사     | 프로팀  |
| 5       | Effort      | #4444  | Challenger | 1936 | 노틸러스  | 브라움   | 알리스타  | 683   | 412 | 318  | 56%      | 탱커     | 중립적  |
| 6       | LNG BuLLDoG | #KR2   | Challenger | 1879 | 아지르   | 갈리오   | 유나라   | 765   | 703 | 559  | 56%      | 마법사    | 프로팀  |

</small></small>
</br>

#### 05. Analysis between `name type`, `role`
![img](https://github.com/RuneShell/LOL_Hidden_Patterns/tree/main/analysis/05-1._distribution_of_name_type_by_role.png)

- `Neutral(중립적)` nicknames, such as simple nouns, were the most common.

↓ (without `Neutral`)

![img](https://github.com/RuneShell/LOL_Hidden_Patterns/tree/main/analysis/05-2._distribution_of_name_type_by_role_(without_neutral).png)

 - `Cute(귀여운)` nickname rate for `Support(서포터)` is **1.79x higher** than the average of all other roles.

 - `Sexual(선정적)` nickname rate for `Assassin(암살자)` is **2.37x higher** than the average of all other roles. and is even **5.8x** compared to `Support(서포터)`.

  - `Insincere(성의없는)` nickname rate for `Support(서포터)` is **1.64x lower** than the average of all other roles.

</br>

#### 06. Analysis between `name type`, `tier`
![img](https://github.com/RuneShell/LOL_Hidden_Patterns/tree/main/analysis/06-1._distribution_of_name_type_by_tier.png)

- The higher the `Tier`, the higher the proportion of `Neutral(중립적)` nicknames. `Challenger` tier for `Neutral` nicknames is **1.64x higher** than `Iron` tier.

↓ (without `Neutral`)

![img](https://github.com/RuneShell/LOL_Hidden_Patterns/tree/main/analysis/06-2._distribution_of_name_type_by_tier_(without_neutral).png)

- The higher the `Tier`, the higher the proportion of `Professional(프로팀)` nicknames.
    - In `Challenger`, there are real progamers belong to professional teams.
    - But 


</br>

#### 07. Analysis between 