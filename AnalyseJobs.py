import pandas as pd;

df = pd.read_csv('2018-02-02.csv');
df_com = pd.read_csv('Company.csv');
# print(df.head(3));

def cleanAgentCompany(df):
    _df = df;
    _removeComp = "Consult|recruit|Person|Search|Conn|Solution|Online|db |Tech|Info|Inno|Talent|Agent|Excel|Career|McKinley|Partner|Robert Walters|George Samuel|Wellesley Associates|HKT|Asian TAT Limited|Statsmaster|Software|Lazybug|eRun|Exactal Limited";
    _df.loc[(_df['Company'].str.contains(_removeComp, case=False)) & ~(_df['Type'] == 'Agent') & ~(_df['Type'] == 'Company'), 'Type'] = 'Agent';
    return  _df;

# df_com_v2 = df_com['Company'].str.contains('consult', case=False);
# print(df_com[df_com_v2].count());


def main():
    _SearchName ='watson';
    df_v2 = pd.merge(df, cleanAgentCompany(df_com), on='Company', how='left');
    # print(df_v2);
    # df_v2.to_csv('2018-02-01_v2.csv', index=False)
    # print(df_v2.head(3));
    # print(df_v2.dtypes);
    # print(df_v2[~(df_v2['Type'] == 'Agent')].head(5));
    print(df_v2[~(df_v2['Type'] == 'Agent') & (df_v2['Company'].str.contains(_SearchName, case=False))].head(5));

if __name__ == "__main__":
    main();

