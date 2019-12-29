import seaborn as sns
import pandas  as pd
import numpy   as np
import glob
# file path for all of the donations on external hard drive. All pulled from FEC.GOV 
file_path_2005_2008 = [
            '/Volumes/Polotics_capstone_drive/capstone/Data/2005-2006/Donations',
            '/Volumes/Polotics_capstone_drive/capstone/Data/2007-2008/Donations'
            ]
file_path_2009_2012 = [
            '/Volumes/Polotics_capstone_drive/capstone/Data/2009-2010/Donations',
            '/Volumes/Polotics_capstone_drive/capstone/Data/2011-2012/Donations/indiv12/by_date'
            ]

file_path_2013_2016 = [
            '/Volumes/Polotics_capstone_drive/capstone/Data/2013-2014/Donations/indiv14/by_date',
            '/Volumes/Polotics_capstone_drive/capstone/Data/2015-2016/Donatoins/indiv16/by_date'    
            ]

file_path_2016_pt2 = [
            '/Volumes/Polotics_capstone_drive/capstone/Data/2015-2016/Donatoins/by_date_2'
            ]

file_path_2017_2020 = [
            '/Volumes/Polotics_capstone_drive/capstone/Data/2017-2018/Donations/indiv18/by_date',
            ]

file_path_2017_2020_pt2 =[
            '/Volumes/Polotics_capstone_drive/capstone/Data/2017-2018/Donations/2017-18_pt2',
            '/Volumes/Polotics_capstone_drive/capstone/Data/2019-2020/Donations/indiv20/by_date'
            ]
# File path for the campaings expenditures on external hard drive. All files pulled from FEC.Gov

File_path_exp_2005_2008=['/Volumes/Polotics_capstone_drive/capstone/Data/2005-2006/Exp',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2007-2008/Exp']

File_path_exp_2009_2012=['/Volumes/Polotics_capstone_drive/capstone/Data/2009-2010/Exp',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2011-2012/Exp']

File_path_exp_2013_2016=['/Volumes/Polotics_capstone_drive/capstone/Data/2013-2014/Exp',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2015-2016/Exp']

File_path_exp_2017_2020=['/Volumes/Polotics_capstone_drive/capstone/Data/2017-2018/Exp',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2019-2020/Exp']
# File path for the super pac contrubutions on external hard drive. All files pulled from FEC.Gov

File_path_pac_2005_2008=['/Volumes/Polotics_capstone_drive/capstone/Data/2005-2006/PAC',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2007-2008/PAC']

File_path_pac_2009_2012=['/Volumes/Polotics_capstone_drive/capstone/Data/2009-2010/PAC',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2011-2012/PAC']

File_path_pac_2013_2016=['/Volumes/Polotics_capstone_drive/capstone/Data/2013-2014/PAC',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2015-2016/PAC']

File_path_pac_2017_2020=['/Volumes/Polotics_capstone_drive/capstone/Data/2017-2018/PAC',
                         '/Volumes/Polotics_capstone_drive/capstone/Data/2019-2020/PAC']
# function for reading in the data useing glob package
def gather_files(file_path):
    full_lines = []
    for path in file_path:
        files = [f for f in glob.glob(path + "**/*.txt", recursive=True)]
        for file in files:
            print(f'I am working on {file}')
            with open(file, encoding = 'utf8', errors = 'ignore') as f:
                for line in f:
                    line_list = [i.strip() for i in line.split('|')]
                    full_lines.append(line_list)
    print("Now converting to Data Frame")
    df = pd.DataFrame(full_lines)
    print("All done your datafram is ready")
    return(df)
# this function for reading in the file path of the data
# use nameing convention df_startYear_endYear for data frames names
file_path_2017_2020_pt2 = gather_files(file_path_2017_2020_pt2)


def Names_of_col_for_donations(df):
    # names of columns given from the FEC
    
    df.rename(columns={0: 'CMTE_ID', 1:'AMNDT_IND', 2:'RPT_TP', 3:'TRANSACTION_PGI',
                       4:'IMAGE_NUM', 5:'TRANSACTION_TP', 6:'ENTITY_TP', 7:'NAME',8:'CITY',
                       9:'STATE', 10:'ZIP_CODE', 11:'EMPLOYER', 12:'OCCUPATION',
                       13:'TRANSACTION_DT', 14:'TRANSACTION_AMT', 15:'OTHER_ID',
                       16:'TRAN_ID', 17:'FILE_NUM', 18:'MEMO_CD', 19:'MEMO_TEXT',
                       20:'SUB_ID'},
                       inplace=True)
    print('Column names changed')
    # Droppign of un needed columns 
    df.drop(['IMAGE_NUM',
             'TRANSACTION_PGI',
             'MEMO_TEXT',
             'TRANSACTION_TP',
             'TRAN_ID',
             'OTHER_ID',
            'MEMO_TEXT',
            'MEMO_CD'], axis = 1,inplace = True) 
    print("un needed columns were droped :) ")
    
    # converting to the correct data type
    df['TRANSACTION_AMT'] = df['TRANSACTION_AMT'].astype(str).astype(int)
    df['SUB_ID'] = df['SUB_ID'].astype(str).astype(int)
    df['TRANSACTION_DT'] = df['TRANSACTION_DT'].astype(str)
    print('Data types changed')
    
    # Date time operation and cleaning sets any missing values to be 0 then drops them
    df['TRANSACTION_DT'].replace(to_replace ="", 
                             value ='0',inplace = True)
    df = df[df.TRANSACTION_DT != '0']
    df.fillna(0)
    print('Dropped 0s')
    
    # sets the values to be a date time object 
    df['TRANSACTION_DT'] = pd.to_datetime(df['TRANSACTION_DT'], format='%m%d%Y',errors = 'coerce')
    df.set_index('TRANSACTION_DT',inplace = True)
    df = df.loc['CHANGE FOR THE CORRECT DATE RANGE']
    print('Date time object')
    
    # sorts the values to be in order 
    df.sort_index(inplace = True)
    # forces any dates that were entered won to be dropped 
    print('data is organized ')
    # drops unneeded columns  
    return(df)
def Names_of_col_for_expenses(df):

    # names of columns given from the FEC
    
    df.rename(columns={0:'CMTE_ID', 1:'AMNDT_IND', 2:'RPT_YR', 3:'RPT_TP', 4:'IMAGE_NUM',
                       5:'LINE_NUM', 6:'FORM_TP_CD', 7:'SCHED_TP_CD', 8:'NAME', 9:'CITY',
                       10:'STATE', 11:'ZIP_CODE', 12:'TRANSACTION_DT',13:'TRANSACTION_AMT',
                       14:'TRANSACTION_PGI', 15:'PURPOSE', 16:'CATEGORY', 17:'CATEGORY_DESC',
                       18:'MEMO_CD', 19:'MEMO_TEXT', 20:'ENTITY_TP', 21:'SUB_ID',
                       22:'FILE_NUM', 23:'TRAN_ID', 24:'BACK_REF_TRAN_ID'}, inplace=True)
    print('Column names changed')
    # drops unneeded columns 
    df.drop(['IMAGE_NUM',
             'TRANSACTION_PGI',
             'MEMO_TEXT',
             'TRAN_ID',
            'SCHED_TP_CD',
            'LINE_NUM',
            'MEMO_CD',
            'MEMO_TEXT'
            ], axis = 1,inplace = True) 
    print("un needed columns were droped :) ")

    # makes the necessary values to be the correct data type
    
    df['TRANSACTION_AMT'].replace(to_replace =[""], 
                             value ='0',inplace = True)
    df = df[df.TRANSACTION_AMT != '0']
    df['TRANSACTION_AMT'] = df['TRANSACTION_AMT'].astype(str).astype(float)
    df['SUB_ID'] = df['SUB_ID'].astype(str).astype(int)
    df['TRANSACTION_DT'] = df['TRANSACTION_DT'].astype(str)
    df.fillna(0)
    print('Data types changed')
    
    # Date time operation and cleaning sets any missing values to be 0 then drops them
    
    df['TRANSACTION_DT'].replace(to_replace ="", 
                             value ='0',inplace = True)
    df = df[df.TRANSACTION_DT != '0']
    print('Dropped 0s')
    
    # sets the values to be a date time object 
    
    df['TRANSACTION_DT'] = pd.to_datetime(df['TRANSACTION_DT'], format='%m/%d/%Y',errors = 'coerce')
    df.set_index('TRANSACTION_DT',inplace = True)
    df = df.loc['CHANGE FOR THE CORRECT DATE RANGE']
    print('Date time object')
    
    # sorts the values to be in order 
    
    df.sort_index(inplace = True)
    
    # forces any dates that were entered wrong to be dropped 
    
    print('data is organized ')
    
    return(df)
# Makes csv of donations with the first steps of cleaning our data 
Names_of_col_for_donations('list of files').to_csv('Path to save cleaned csv')

# Makes csv of Expenses with the first steps of cleaning our data 
Names_of_col_for_expenses('list of files').to_csv('file_Path_For_exp')


df_2005_2008_donations = pd.read_csv('../../Data/don/2005_2008.csv')
# list of the Democratic candidates in the primary 2008 with the CMTE_ID
Obama = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431445'])]
Clinton = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431569'])]
Edwards = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431205'])]
Richardson = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431577'])]
Biden = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00334037'])]
Dodd = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431379'])]
Gravel = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00423202'])]
Kucinich = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00430975'])]
# list of the Republican candidates in the primary 2008
McCain = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00430470'])]
Huckabee = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431809'])]
Romney = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431171'])]
Paul = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00432914'])]
Thompson = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00438507'])]
Keyes = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00452532'])]
Hunter = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00431411'])]
Giuliani = df_2005_2008_donations.loc[df_2005_2008_donations['CMTE_ID'].isin(['C00430512'])]
# writer the candidates the the proper csvs
# Democrat candidates for 2008
Obama.to_csv('../../Data/don/2005_2008_ind_cand/Obama_2008.csv')
Clinton.to_csv('../../Data/don/2005_2008_ind_cand/Clinton_2008.csv')
Edwards.to_csv('../../Data/don/2005_2008_ind_cand/Edwards_2008.csv')
Richardson.to_csv('../../Data/don/2005_2008_ind_cand/Richardson_2008.csv')
Biden.to_csv('../../Data/don/2005_2008_ind_cand/Biden_2008.csv')
Dodd.to_csv('../../Data/don/2005_2008_ind_cand/Dodd_2008.csv')
Gravel.to_csv('../../Data/don/2005_2008_ind_cand/Gravel_2008.csv')
Kucinich.to_csv('../../Data/don/2005_2008_ind_cand/Kucinich_2008.csv')
# Republican candidates for 2008
McCain.to_csv('../../Data/don/2005_2008_ind_cand/McCain_2008.csv')
Huckabee.to_csv('../../Data/don/2005_2008_ind_cand/Huckabee_2008.csv')
Romney.to_csv('../../Data/don/2005_2008_ind_cand/Romney_2008.csv')
Paul.to_csv('../../Data/don/2005_2008_ind_cand/Paul_2008.csv')
Thompson.to_csv('../../Data/don/2005_2008_ind_cand/Thompson_2008.csv')
Keyes.to_csv('../../Data/don/2005_2008_ind_cand/Keyes_2008.csv')
Hunter.to_csv('../../Data/don/2005_2008_ind_cand/Hunter_2008.csv') 
Giuliani.to_csv('../../Data/don/2005_2008_ind_cand/Giuliani_2008.csv')
# read in the correct data frame for the 2012 elections
df_2009_2012_donations = pd.read_csv('../../Data/don/2009_2012.csv')
# Republican candidates for 2012
Romney = df_2009_2012_donations.loc[df_2009_2012_donations['CMTE_ID'].isin(['C00431171'])]
Santorum = df_2009_2012_donations.loc[df_2009_2012_donations['CMTE_ID'].isin(['C00496034'])] 
Paul = df_2009_2012_donations.loc[df_2009_2012_donations['CMTE_ID'].isin(['C00495820'])]
Gingrich = df_2009_2012_donations.loc[df_2009_2012_donations['CMTE_ID'].isin(['C00496497'])] 
# write the candidates to the proper csvs 
Romney.to_csv('../../Data/don/2009_2012_ind_cand/Romney_2012.csv')
Santorum.to_csv('../../Data/don/2009_2012_ind_cand/Santorum_2012.csv')
Paul.to_csv('../../Data/don/2009_2012_ind_cand/Paul_2012.csv') 
Gingrich.to_csv('../../Data/don/2009_2012_ind_cand/Gingrich_2012.csv')
#part 1 of the donations 2013-2016
df_2013_2016_donations = pd.read_csv('../../Data/don/2013_2016.csv')

#part 2 of the donations 2016
df_2013_2016_donations_pt2 = pd.read_csv('../../Data/don/2013_2016_pt2.csv')
# Republican candidates for 2016

Trump = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00580100'])]
Cruz = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00574624'])]
Kasich = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00581876'])]
Rubio = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00458844'])]
Carson = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00573519'])]
Bush = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00579458'])]
Paul = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00575449'])]
Christie = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00580399'])]
Huckabee = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00577981'])]
Fiorina = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00577312'])]
Gilmore = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00582668'])]
Santorum = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00578492'])]
Perry = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00500587'])]
Walker = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00580480'])]
Jindal = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00580159'])]
Graham = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00578757'])]
Pataki = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00578245'])]
# Democrat candidates for 2016
Clinton_2016 = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00575795'])]
Sanders_2016 = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00577130'])]
OMalley = df_2013_2016_donations.loc[df_2013_2016_donations['CMTE_ID'].isin(['C00578658'])]
# write the candidates to csvs
#republican nominees
Trump.to_csv('../../Data/don/2013_2016_ind_cand/Trump_2016.csv')
Cruz.to_csv('../../Data/don/2013_2016_ind_cand/Cruz_2016.csv')
Kasich.to_csv('../../Data/don/2013_2016_ind_cand/Kasich_2016.csv') 
Rubio.to_csv('../../Data/don/2013_2016_ind_cand/Rubio_2016.csv')
Carson.to_csv('../../Data/don/2013_2016_ind_cand/Carson_2016.csv')
Bush.to_csv('../../Data/don/2013_2016_ind_cand/Bush_2016.csv')
Paul.to_csv('../../Data/don/2013_2016_ind_cand/Paul_2016.csv') 
Christie.to_csv('../../Data/don/2013_2016_ind_cand/Christie_2016.csv')
Huckabee.to_csv('../../Data/don/2013_2016_ind_cand/Huckabee_2016.csv')
Fiorina.to_csv('../../Data/don/2013_2016_ind_cand/Fiorina_2016.csv')
Gilmore.to_csv('../../Data/don/2013_2016_ind_cand/Gilmore_2016.csv') 
Santorum.to_csv('../../Data/don/2013_2016_ind_cand/Santorum_2016.csv')
Perry.to_csv('../../Data/don/2013_2016_ind_cand/Perry_2016.csv')
Walker.to_csv('../../Data/don/2013_2016_ind_cand/Walker_2016.csv')
Jindal.to_csv('../../Data/don/2013_2016_ind_cand/Jindal_2016.csv') 
Graham.to_csv('../../Data/don/2013_2016_ind_cand/Grahm_2016.csv')
Pataki.to_csv('../../Data/don/2013_2016_ind_cand/Pataki_2016.csv')
# democratic nominees 
Clinton_2016.to_csv('../../Data/don/2013_2016_ind_cand/Clinton_2016.csv')
Sanders_2016.to_csv('../../Data/don/2013_2016_ind_cand/Sanders_2016.csv') 
OMalley.to_csv('../../Data/don/2013_2016_ind_cand/Omalley_2016.csv')
# Republican candidates for 2016_pt2
Trump2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00580100'])]
Cruz2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00574624'])]
Kasich2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00581876'])]
Rubio2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00458844'])]
Carson2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00573519'])]
Bush2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00579458'])]
Paul2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00575449'])]
Christie2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00580399'])]
Huckabee2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00577981'])]
Fiorina2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00577312'])]
Gilmore2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00582668'])]
Santorum2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00578492'])]
Perry2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00500587'])]
Walker2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00580480'])]
Jindal2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00580159'])]
Graham2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00578757'])]
Pataki2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00578245'])]
# Democratic candidates for 2016_pt2
# Democrat candidates for 2016
Clinton_20162 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00575795'])]
Sanders_20162 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00577130'])]
OMalley2 = df_2013_2016_donations_pt2.loc[df_2013_2016_donations_pt2['CMTE_ID'].isin(['C00578658'])]
# write the candidate to new csvs making sure to rename the csvs to pt2
Trump2.to_csv('../../Data/don/2013_2016_ind_cand/Trump_2016_pt2.csv')
Cruz2.to_csv('../../Data/don/2013_2016_ind_cand/Cruz_2016_pt2.csv')
Kasich2.to_csv('../../Data/don/2013_2016_ind_cand/Kasich_2016_pt2.csv') 
Rubio2.to_csv('../../Data/don/2013_2016_ind_cand/Rubio_2016_pt2.csv')
Carson2.to_csv('../../Data/don/2013_2016_ind_cand/Carson_2016_pt2.csv')
Bush2.to_csv('../../Data/don/2013_2016_ind_cand/Bush_2016_pt2.csv')
Paul2.to_csv('../../Data/don/2013_2016_ind_cand/Paul_2016_pt2.csv') 
Christie2.to_csv('../../Data/don/2013_2016_ind_cand/Christie_2016_pt2.csv')
Huckabee2.to_csv('../../Data/don/2013_2016_ind_cand/Huckabee_2016_pt2.csv')
Fiorina2.to_csv('../../Data/don/2013_2016_ind_cand/Fiorina_2016_pt2.csv')
Gilmore2.to_csv('../../Data/don/2013_2016_ind_cand/Gilmore_2016_pt2.csv') 
Santorum2.to_csv('../../Data/don/2013_2016_ind_cand/Santorum_2016_pt2.csv')
Perry2.to_csv('../../Data/don/2013_2016_ind_cand/Perry_2016_pt2.csv')
Walker2.to_csv('../../Data/don/2013_2016_ind_cand/Walker_2016_pt2.csv')
Jindal2.to_csv('../../Data/don/2013_2016_ind_cand/Jindal_2016_pt2.csv') 
Graham2.to_csv('../../Data/don/2013_2016_ind_cand/Grahm_2016_pt2.csv')
Pataki2.to_csv('../../Data/don/2013_2016_ind_cand/Pataki_2016_pt2.csv')
# democratic nominees 
Clinton_20162.to_csv('../../Data/don/2013_2016_ind_cand/Clinton_2016_pt2.csv')
Sanders_20162.to_csv('../../Data/don/2013_2016_ind_cand/Sanders_2016_pt2.csv') 
OMalley2.to_csv('../../Data/don/2013_2016_ind_cand/Omalley_2016_pt2.csv')
# read in the needed data
df_2017_2020_donations = pd.read_csv('../../Data/don/2017_2020.csv')
df_2017_2020_donations_2 = pd.read_csv('../../Data/don/2017_2020_pt2.csv')
# part one of the 2020 candidates
Biden = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00703975'])]
Booker = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00695510'])]
Buttigieg = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00697441'])]
Castro = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00693044'])]
Delaney = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00508416'])]
Gabbard = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00693713'])]
Klobuchar = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00696419'])]
Sanders = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00696948'])]
Steyer = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00711614'])]
Warren = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00693234'])]
Williamson = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00696054'])]
Yang = df_2017_2020_donations.loc[df_2017_2020_donations['CMTE_ID'].isin(['C00659938'])]
# part two of the 2020 candidates
Biden_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00703975'])]
Booker_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00695510'])]
Buttigieg_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00697441'])]
Castro_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00693044'])]
Delaney_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00508416'])]
Gabbard_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00693713'])]
Klobuchar_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00696419'])]
Sanders_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00696948'])]
Steyer_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00711614'])]
Warren_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00693234'])]
Williamson_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00696054'])]
Yang_2 = df_2017_2020_donations_2.loc[df_2017_2020_donations_2['CMTE_ID'].isin(['C00659938'])]
# write part 1 to the correct csv
Biden.to_csv('../../Data/don/2017_2020_ind_cand/Biden.csv')
Booker.to_csv('../../Data/don/2017_2020_ind_cand/Booker.csv')
Buttigieg.to_csv('../../Data/don/2017_2020_ind_cand/Buttigieg.csv')
Castro.to_csv('../../Data/don/2017_2020_ind_cand/Castro.csv') 
Delaney.to_csv('../../Data/don/2017_2020_ind_cand/Delaney.csv')
Gabbard.to_csv('../../Data/don/2017_2020_ind_cand/Gabbard.csv')
Klobuchar.to_csv('../../Data/don/2017_2020_ind_cand/Klobuchar.csv')
Sanders.to_csv('../../Data/don/2017_2020_ind_cand/Sanders.csv')
Steyer.to_csv('../../Data/don/2017_2020_ind_cand/Steyer.csv')
Warren.to_csv('../../Data/don/2017_2020_ind_cand/Warren.csv')
Williamson.to_csv('../../Data/don/2017_2020_ind_cand/Williamson.csv')
Yang.to_csv('../../Data/don/2017_2020_ind_cand/Yang.csv')
# write part 2 to the correct csv making sure not to over write part 1
Biden_2.to_csv('../../Data/don/2017_2020_ind_cand/Biden2.csv')
Booker_2.to_csv('../../Data/don/2017_2020_ind_cand/Booker2.csv')
Buttigieg_2.to_csv('../../Data/don/2017_2020_ind_cand/Buttigieg2.csv')
Castro_2.to_csv('../../Data/don/2017_2020_ind_cand/Castro2.csv') 
Delaney_2.to_csv('../../Data/don/2017_2020_ind_cand/Delaney2.csv')
Gabbard_2.to_csv('../../Data/don/2017_2020_ind_cand/Gabbard2.csv')
Klobuchar_2.to_csv('../../Data/don/2017_2020_ind_cand/Klobuchar2.csv')
Sanders_2.to_csv('../../Data/don/2017_2020_ind_cand/Sanders2.csv')
Steyer_2.to_csv('../../Data/don/2017_2020_ind_cand/Steyer2.csv')
Warren_2.to_csv('../../Data/don/2017_2020_ind_cand/Warren2.csv')
Williamson_2.to_csv('../../Data/don/2017_2020_ind_cand/Williamson2.csv')
Yang_2.to_csv('../../Data/don/2017_2020_ind_cand/Yang2.csv')
df_2008_exp = pd.read_csv('../../Data/exp/2005_2008_exp.csv') 
df_2008_exp.drop(columns=['AMNDT_IND','RPT_TP','LINE_NUM','FORM_TP_CD','NAME','CITY',
                          'CATEGORY','CATEGORY_DESC','MEMO_CD','ENTITY_TP','25'],inplace = True)
# list of the Democratic candidates in the primary 2008
Obama = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431445'])]
Clinton = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431569'])]
Edwards = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431205'])]
Richardson = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431577'])]
Biden = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00334037'])]
Dodd = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431379'])]
Gravel = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00423202'])]
Kucinich = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00430975'])]
# list of the Republican candidates in the primary 2008
McCain = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00430470'])]
Huckabee = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431809'])]
Romney = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431171'])]
Paul = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00432914'])]
Thompson = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00438507'])]
Keyes = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00452532'])]
Hunter = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00431411'])]
Giuliani = df_2008_exp.loc[df_2008_exp['CMTE_ID'].isin(['C00430512'])]
Obama.to_csv('../../Data/exp/2008_ind_cand_exp/obama_exp.csv')
Clinton.to_csv('../../Data/exp/2008_ind_cand_exp/Clinton_exp.csv')
Edwards.to_csv('../../Data/exp/2008_ind_cand_exp/Edwards_exp.csv')
Richardson.to_csv('../../Data/exp/2008_ind_cand_exp/Richardson_exp.csv')
Biden.to_csv('../../Data/exp/2008_ind_cand_exp/Biden_exp.csv')
Dodd.to_csv('../../Data/exp/2008_ind_cand_exp/Dodd_exp.csv')
Gravel.to_csv('../../Data/exp/2008_ind_cand_exp/Gravel_exp.csv')
Kucinich.to_csv('../../Data/exp/2008_ind_cand_exp/Kucinish_exp.csv')
McCain.to_csv('../../Data/exp/2008_ind_cand_exp/MaCain_exp.csv')
Huckabee.to_csv('../../Data/exp/2008_ind_cand_exp/Huckabee_exp.csv')
Romney.to_csv('../../Data/exp/2008_ind_cand_exp/Romney_exp.csv')
Paul.to_csv('../../Data/exp/2008_ind_cand_exp/Paul_exp.csv')
Thompson.to_csv('../../Data/exp/2008_ind_cand_exp/Thompson_exp.csv')
Keyes.to_csv('../../Data/exp/2008_ind_cand_exp/Keyes_exp.csv')
Hunter.to_csv('../../Data/exp/2008_ind_cand_exp/Hunter_exp.csv')
Giuliani.to_csv('../../Data/exp/2008_ind_cand_exp/Giuliani_exp.csv')
df_2012_exp = pd.read_csv('../../Data/exp/2009_2012_exp.csv') 
df_2012_exp.drop(columns=['AMNDT_IND','RPT_TP','LINE_NUM','FORM_TP_CD','NAME','CITY',
                          'CATEGORY','CATEGORY_DESC','MEMO_CD','ENTITY_TP','25'],inplace = True)
Romney_exp = df_2012_exp.loc[df_2012_exp['CMTE_ID'].isin(['C00431171'])]
Santorum_exp =df_2012_exp.loc[df_2012_exp['CMTE_ID'].isin(['C00496034'])] 
Paul_exp = df_2012_exp.loc[df_2012_exp['CMTE_ID'].isin(['C00495820'])]
Gingrich_exp = df_2012_exp.loc[df_2012_exp['CMTE_ID'].isin(['C00496497'])]
Romney_exp.to_csv('../../Data/exp/2012_ind_cand_exp/Romney_exp.csv')
Santorum_exp.to_csv('../../Data/exp/2012_ind_cand_exp/Santorum_exp.csv')
Paul_exp.to_csv('../../Data/exp/2012_ind_cand_exp/Paul_exp.csv')
Gingrich_exp.to_csv('../../Data/exp/2012_ind_cand_exp/Gingrich_exp.csv')
df_2016_exp = pd.read_csv('../../Data/exp/2013_2016_exp.csv') 
df_2016_exp.drop(columns=['AMNDT_IND','RPT_TP','FORM_TP_CD','NAME','CITY',
                          'CATEGORY','CATEGORY_DESC','MEMO_CD','ENTITY_TP','25'],inplace = True)
Trump_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00580100'])]
Cruz_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00574624'])]
Kasich_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00581876'])]
Rubio_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00458844'])]
Carson_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00573519'])]
Bush_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00579458'])]
Paul_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00575449'])]
Christie_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00580399'])]
Huckabee_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00577981'])]
Fiorina_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00577312'])]
Gilmore_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00582668'])]
Santorum_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00578492'])]
Perry_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00500587'])]
Walker_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00580480'])]
Jindal_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00580159'])]
Graham_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00578757'])]
Pataki_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00578245'])]
# Democratic candidates for 2016_pt2
# Democrat candidates for 2016
Clinton_2016_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00575795'])]
Sanders_2016_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00577130'])]
OMalley_exp = df_2016_exp.loc[df_2016_exp['CMTE_ID'].isin(['C00578658'])]
Trump_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Trump_exp.csv')
Cruz_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Cruz_exp.csv')
Kasich_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Kasich_exp.csv')
Rubio_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Rubio_exp.csv')
Carson_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Carson_exp.csv')
Bush_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Bush_exp.csv')
Paul_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Paul_exp.csv')
Christie_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Christie_exp.csv')
Huckabee_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Huckabee_exp.csv')
Fiorina_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Fiorina_exp.csv')
Gilmore_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Gilmore_exp.csv')
Santorum_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Santorum_exp.csv')
Perry_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Perry_exp.csv')
Walker_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Walker_exp.csv')
Jindal_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Jindal_exp.csv')
Graham_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Graham_exp.csv')
Pataki_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Pataki_exp.csv')
Clinton_2016_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Clinton_exp.csv')
Sanders_2016_exp.to_csv('../../Data/exp/2016_ind_cand_exp/Sanders_exp.csv')
OMalley_exp.to_csv('../../Data/exp/2016_ind_cand_exp/OMalley_exp.csv')
df_2020_exp = pd.read_csv('../../Data/exp/2017_2020_exp.csv')
Biden_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00703975'])]
Booker_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00695510'])]
Buttigieg_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00697441'])]
Castro_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00693044'])]
Delaney_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00508416'])]
Gabbard_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00693713'])]
Klobuchar_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00696419'])]
Sanders_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00696948'])]
Steyer_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00711614'])]
Warren_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00693234'])]
Williamson_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00696054'])]
Yang_exp =df_2020_exp.loc[df_2020_exp['CMTE_ID'].isin(['C00659938'])]
Biden_exp.to_csv('../../Data/exp/2020_exp/Biden_exp.csv')
Booker_exp.to_csv('../../Data/exp/2020_exp/Booker_exp.csv')
Buttigieg_exp.to_csv('../../Data/exp/2020_exp/Buttigieg_exp.csv')
Castro_exp.to_csv('../../Data/exp/2020_exp/Castro_exp.csv') 
Delaney_exp.to_csv('../../Data/exp/2020_exp/Delaney_exp.csv')
Gabbard_exp.to_csv('../../Data/exp/2020_exp/Gabbard_exp.csv')
Klobuchar_exp.to_csv('../../Data/exp/2020_exp/Klobuchar_exp.csv')
Sanders_exp.to_csv('../../Data/exp/2020_exp/Sanders_exp.csv')
Steyer_exp.to_csv('../../Data/exp/2020_exp/Steyer_exp.csv')
Warren_exp.to_csv('../../Data/exp/2020_exp/Warren_exp.csv')
Williamson_exp.to_csv('../../Data/exp/2020_exp/Williamson_exp.csv')
Yang_exp.to_csv('../../Data/exp/2020_exp/Yang_exp.csv')
# read in just the csv for the candidates
Trump_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Trump_2016_pt2.csv')
Cruz_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Cruz_2016_pt2.csv')
Kasich_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Kasich_2016_pt2.csv') 
Rubio_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Rubio_2016_pt2.csv')
Carson_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Carson_2016_pt2.csv')
Bush_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Bush_2016_pt2.csv')
Paul_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Paul_2016_pt2.csv') 
Christie_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Christie_2016_pt2.csv')
Huckabee_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Huckabee_2016_pt2.csv')
Fiorina_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Fiorina_2016_pt2.csv')
Gilmore_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Gilmore_2016_pt2.csv') 
Santorum_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Santorum_2016_pt2.csv')
Perry_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Perry_2016_pt2.csv')
Walker_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Walker_2016_pt2.csv')
Jindal_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Jindal_2016_pt2.csv') 
Grahm_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Grahm_2016_pt2.csv')
Pataki_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Pataki_2016_pt2.csv')
# democratic nominees 
Clinton_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Clinton_2016_pt2.csv')
Sanders_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Sanders_2016_pt2.csv') 
Omalley_pt2= pd.read_csv('../../Data/don/2013_2016_ind_cand/Omalley_2016_pt2.csv')
# read in just the path for the candidates 
Trump_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Trump_2016.csv')
Cruz_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Cruz_2016.csv')
Kasich_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Kasich_2016.csv') 
Rubio_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Rubio_2016.csv')
Carson_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Carson_2016.csv')
Bush_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Bush_2016.csv')
Paul_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Paul_2016.csv') 
Christie_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Christie_2016.csv')
Huckabee_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Huckabee_2016.csv')
Fiorina_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Fiorina_2016.csv')
Gilmore_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Gilmore_2016.csv') 
Santorum_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Santorum_2016.csv')
Perry_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Perry_2016.csv')
Walker_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Walker_2016.csv')
Jindal_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Jindal_2016.csv') 
Grahm_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Grahm_2016.csv')
Pataki_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Pataki_2016.csv')
# democratic nominees 
Clinton_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Clinton_2016.csv')
Sanders_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Sanders_2016.csv') 
Omalley_pt1= pd.read_csv('../../Data/don/2013_2016_ind_cand/Omalley_2016.csv')
# concat the two data frames together into one data frame 
Trump = pd.concat([Trump_pt1,Trump_pt2])
Cruz = pd.concat([Cruz_pt1,Cruz_pt2])
Kasich = pd.concat([Kasich_pt1,Kasich_pt2])
Rubio = pd.concat([Rubio_pt1,Rubio_pt2])
Carson = pd.concat([Carson_pt1,Carson_pt2])
Bush = pd.concat([Bush_pt1,Bush_pt2])
Paul = pd.concat([Paul_pt1,Paul_pt2])
Christie = pd.concat([Christie_pt1,Christie_pt2])
Huckabee = pd.concat([Huckabee_pt1,Huckabee_pt2])
Fiorina = pd.concat([Fiorina_pt1,Fiorina_pt2])
Gilmore = pd.concat([Gilmore_pt1,Gilmore_pt2])
Santorum = pd.concat([Santorum_pt1,Santorum_pt2])
Perry = pd.concat([Perry_pt1,Perry_pt2]) 
Walker = pd.concat([Walker_pt1,Walker_pt2]) 
Jindal = pd.concat([Jindal_pt1,Jindal_pt2]) 
Grahm = pd.concat([Grahm_pt1,Grahm_pt2])  
Pataki = pd.concat([Pataki_pt1,Pataki_pt2])
Clinton = pd.concat([Clinton_pt1,Clinton_pt2])
Sanders = pd.concat([Sanders_pt1,Sanders_pt2])
Omalley = pd.concat([Omalley_pt1,Omalley_pt2])
Biden = pd.read_csv('../../Data/don/2017_2020_ind_cand/Biden.csv')
Booker = pd.read_csv('../../Data/don/2017_2020_ind_cand/Booker.csv')
Buttigieg = pd.read_csv('../../Data/don/2017_2020_ind_cand/Buttigieg.csv')
Castro = pd.read_csv('../../Data/don/2017_2020_ind_cand/Castro.csv') 
Delaney = pd.read_csv('../../Data/don/2017_2020_ind_cand/Delaney.csv')
Gabbard = pd.read_csv('../../Data/don/2017_2020_ind_cand/Gabbard.csv')
Klobuchar = pd.read_csv('../../Data/don/2017_2020_ind_cand/Klobuchar.csv')
Sanders = pd.read_csv('../../Data/don/2017_2020_ind_cand/Sanders.csv')
Steyer = pd.read_csv('../../Data/don/2017_2020_ind_cand/Steyer.csv')
Warren = pd.read_csv('../../Data/don/2017_2020_ind_cand/Warren.csv')
Williamson = pd.read_csv('../../Data/don/2017_2020_ind_cand/Williamson.csv')
Yang = pd.read_csv('../../Data/don/2017_2020_ind_cand/Yang.csv')
Biden2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Biden2.csv')
Booker2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Booker2.csv')
Buttigieg2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Buttigieg2.csv')
Castro2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Castro2.csv') 
Delaney2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Delaney2.csv')
Gabbard2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Gabbard2.csv')
Klobuchar2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Klobuchar2.csv')
Sanders2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Sanders2.csv')
Steyer2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Steyer2.csv')
Warren2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Warren2.csv')
Williamson2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Williamson2.csv')
Yang2 = pd.read_csv('../../Data/don/2017_2020_ind_cand/Yang2.csv')
Biden = pd.concat([Biden,Biden2])
Booker = pd.concat([Booker,Booker2])
Buttigieg = pd.concat([Buttigieg,Buttigieg2])
Castro = pd.concat([Castro,Castro2])
Delaney = pd.concat([Delaney,Delaney2])
Gabbard = pd.concat([Gabbard,Gabbard2])
Klobuchar = pd.concat([Klobuchar,Klobuchar2])
Sanders = pd.concat([Sanders,Sanders2])
Steyer = pd.concat([Steyer,Steyer2])
Warren = pd.concat([Warren,Warren2])
Williamson = pd.concat([Williamson,Williamson2])
Yang = pd.concat([Yang,Yang2])
Biden.to_csv('../../Data/don/2017_2020_ind_cand_final/Biden.csv')
Booker.to_csv('../../Data/don/2017_2020_ind_cand_final/Booker.csv')
Buttigieg.to_csv('../../Data/don/2017_2020_ind_cand_final/Buttigieg.csv')
Castro.to_csv('../../Data/don/2017_2020_ind_cand_final/Castro.csv')
Delaney.to_csv('../../Data/don/2017_2020_ind_cand_final/Delaney.csv')
Gabbard.to_csv('../../Data/don/2017_2020_ind_cand_final/Gabbard.csv')
Klobuchar.to_csv('../../Data/don/2017_2020_ind_cand_final/Klobuchar.csv')
Sanders.to_csv('../../Data/don/2017_2020_ind_cand_final/Sanders.csv')
Steyer.to_csv('../../Data/don/2017_2020_ind_cand_final/Steyer.csv')
Warren.to_csv('../../Data/don/2017_2020_ind_cand_final/Warren.csv')
Williamson.to_csv('../../Data/don/2017_2020_ind_cand_final/Williamson.csv')
Yang.to_csv('../../Data/don/2017_2020_ind_cand_final/Yang.csv')
# put the 2016 candidates in a final csv 
Trump.to_csv('../../Data/don/2013_2016_ind_cand_final/Trump_2016_don_clean.csv')
Cruz.to_csv('../../Data/don/2013_2016_ind_cand_final/Cruz_2016_don_clean.csv')
Kasich.to_csv('../../Data/don/2013_2016_ind_cand_final/Kasich_2016_don_clean.csv')
Rubio.to_csv('../../Data/don/2013_2016_ind_cand_final/Rubio_2016_don_clean.csv')
Carson.to_csv('../../Data/don/2013_2016_ind_cand_final/Carson_2016_don_clean.csv')
Bush.to_csv('../../Data/don/2013_2016_ind_cand_final/Bush_2016_don_clean.csv')
Paul.to_csv('../../Data/don/2013_2016_ind_cand_final/Paul_2016_don_clean.csv')
Christie.to_csv('../../Data/don/2013_2016_ind_cand_final/Christie_2016_don_clean.csv')
Huckabee.to_csv('../../Data/don/2013_2016_ind_cand_final/Huckabee_2016_don_clean.csv')
Fiorina.to_csv('../../Data/don/2013_2016_ind_cand_final/Fiorina_2016_don_clean.csv')
Gilmore.to_csv('../../Data/don/2013_2016_ind_cand_final/Gilmore_2016_don_clean.csv')
Santorum.to_csv('../../Data/don/2013_2016_ind_cand_final/Santorm_2016_don_clean.csv')
Perry.to_csv('../../Data/don/2013_2016_ind_cand_final/Perry_2016_don_clean.csv')
Walker.to_csv('../../Data/don/2013_2016_ind_cand_final/Walker_2016_don_clean.csv')
Jindal.to_csv('../../Data/don/2013_2016_ind_cand_final/Jindal_2016_don_clean.csv')
Grahm.to_csv('../../Data/don/2013_2016_ind_cand_final/Grahm_2016_don_clean.csv')
Pataki.to_csv('../../Data/don/2013_2016_ind_cand_final/Pataki_2016_don_clean.csv')
Clinton.to_csv('../../Data/don/2013_2016_ind_cand_final/Clinton_2016_don_clean.csv')
Sanders.to_csv('../../Data/don/2013_2016_ind_cand_final/Sanders_2016_don_clean.csv')
Omalley.to_csv('../../Data/don/2013_2016_ind_cand_final/Omalley_2016_don_clean.csv')
Obama = pd.read_csv('../../Data/don/2005_2008_ind_cand/Obama_2008.csv')
Clinton_08 = pd.read_csv('../../Data/don/2005_2008_ind_cand/Clinton_2008.csv')
Edwards = pd.read_csv('../../Data/don/2005_2008_ind_cand/Edwards_2008.csv')
Richardson = pd.read_csv('../../Data/don/2005_2008_ind_cand/Richardson_2008.csv')
Biden = pd.read_csv('../../Data/don/2005_2008_ind_cand/Biden_2008.csv')
Dodd = pd.read_csv('../../Data/don/2005_2008_ind_cand/Dodd_2008.csv')
Gravel = pd.read_csv('../../Data/don/2005_2008_ind_cand/Gravel_2008.csv')
Kucinich = pd.read_csv('../../Data/don/2005_2008_ind_cand/Kucinich_2008.csv')
McCain = pd.read_csv('../../Data/don/2005_2008_ind_cand/McCain_2008.csv')
Huckabee = pd.read_csv('../../Data/don/2005_2008_ind_cand/Huckabee_2008.csv')
Romney = pd.read_csv('../../Data/don/2005_2008_ind_cand/Romney_2008.csv')
Paul = pd.read_csv('../../Data/don/2005_2008_ind_cand/Paul_2008.csv')
Thompson = pd.read_csv('../../Data/don/2005_2008_ind_cand/Thompson_2008.csv')
Keyes = pd.read_csv('../../Data/don/2005_2008_ind_cand/Keyes_2008.csv')
Hunter = pd.read_csv('../../Data/don/2005_2008_ind_cand/Hunter_2008.csv') 
Giuliani = pd.read_csv('../../Data/don/2005_2008_ind_cand/Giuliani_2008.csv')

Obama_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/obama_exp.csv')
Clinton_08_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Clinton_exp.csv')
Edwards_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Edwards_exp.csv')
Richardson_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Richardson_exp.csv')
Biden_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Biden_exp.csv')
Dodd_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Dodd_exp.csv')
Gravel_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Gravel_exp.csv')
Kucinich_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Kucinish_exp.csv')
McCain_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/MaCain_exp.csv')
Huckabee_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Huckabee_exp.csv')
Romney_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Romney_exp.csv')
Paul_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Paul_exp.csv')
Thompson_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Thompson_exp.csv')
Keyes_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Keyes_exp.csv')
Hunter_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Hunter_exp.csv') 
Giuliani_exp = pd.read_csv('../../Data/exp/2008_ind_cand_exp/Giuliani_exp.csv')
df_2008_GOP = pd.DataFrame(columns = ['Candidate'])
df_2008_DCCC = pd.DataFrame(columns = ['Candidate'])
df_2008_GOP['Candidate'] = ['McCain','Huckabee','Romney','Paul',
                                     'Thompson','Keyes','Hunter','Giuliani']
df_2008_DCCC['Candidate'] = ['Obama','Clinton','Edwards','Richardson',
                                     'Biden','Dodd','Gravel','Kucinich']
def eng_fet_2008(df1,df2,df3):
    for i in df1.index:
        data_frame = df2[i]
        data_frame.set_index('TRANSACTION_DT',inplace = True)
        q1 = data_frame.loc['2007-01-01':'2007-03-31']
        q2 = data_frame.loc['2007-04-01':'2007-06-30']
        q3 = data_frame.loc['2007-07-01':'2007-09-30']
        q4 = data_frame.loc['2007-10-01':'2007-12-31']
        q1_16 = data_frame.loc['2008-01-01':'2008-03-31']
        q2_16 = data_frame.loc['2008-04-01':'2008-06-30']
        q3_16 = data_frame.loc['2008-07-01':'2008-09-30']
        df1.loc[i,'Q1_Don1'] = q1['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don1'] = q2['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don1'] = q3['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_Don1'] = q4['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_Don2'] = q1_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don2'] = q2_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don2'] = q3_16['TRANSACTION_AMT'].sum()
    for i in  df1.index:
        data_frame_exp = df3[i]
        data_frame_exp.set_index('TRANSACTION_DT',inplace = True)
        data_frame_exp.drop(['Unnamed: 0'], axis = 1,inplace = True)
        q1_exp = data_frame_exp.loc['2007-01-01':'2007-03-31']
        q2_exp = data_frame_exp.loc['2007-04-01':'2007-06-30']
        q3_exp = data_frame_exp.loc['2007-07-01':'2007-09-30']
        q4_exp = data_frame_exp.loc['2007-10-01':'2007-12-31']
        q1_16_exp = data_frame_exp.loc['2008-01-01':'2008-03-31']
        q2_16_exp = data_frame_exp.loc['2008-04-01':'2008-06-30']
        q3_16_exp = data_frame_exp.loc['2008-07-01':'2008-09-30']
        df1.loc[i,'Q1_exp1'] = q1_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp1'] = q2_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp1'] = q3_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_exp1'] = q4_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_exp2'] = q1_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp2'] = q2_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp2'] = q3_16_exp['TRANSACTION_AMT'].sum()
        
    
    return(df1)
df_2008_GOP = eng_fet_2008(df_2008_GOP,[McCain,Huckabee,Romney,Paul,
                                     Thompson,Keyes,Hunter,Giuliani],
                                       [McCain_exp,Huckabee_exp,Romney_exp,Paul_exp,
                                     Thompson_exp,Keyes_exp,Hunter_exp,Giuliani_exp])
df_2008_DCCC = eng_fet_2008(df_2008_DCCC,[Obama,Clinton_08,Edwards,Richardson,
                                     Biden,Dodd,Gravel,Kucinich],
                                        [Obama_exp,Clinton_08_exp,Edwards_exp,Richardson_exp,
                                     Biden_exp,Dodd_exp,Gravel_exp,Kucinich_exp])
days_in_race_GOP_2008 = [554,401,359,458,139,214,446,359]
days_in_race_DCCC_2008 = [564,504,406, 354,361,357,863,408]
df_2008_GOP['Dropped_out'] = 1
df_2008_DCCC['Dropped_out'] = 1
df_2008_GOP.loc[0,'Dropped_out']=0
df_2008_GOP.loc[2,'Dropped_out']=0
df_2008_DCCC.loc[0,'Dropped_out']=0
df_2008_DCCC.loc[6,'Dropped_out']=0
df_2008_GOP['Days_in_race'] = 0
df_2008_DCCC['Days_in_race'] = 0
for i in df_2008_GOP.index:
    df_2008_GOP.loc[i,'Days_in_race'] = days_in_race_GOP_2008[i]
for i in df_2008_DCCC.index:
    df_2008_DCCC.loc[i,'Days_in_race'] = days_in_race_DCCC_2008[i]

df_2008_DCCC.to_csv('../../Data/Model/2008_modeling_DCCC.csv')
df_2008_GOP.to_csv('../../Data/Model/2008_modeling_GOP.csv')
df_2012_features_GOP = pd.DataFrame(columns = ['Candidate'])
df_2012_features_GOP['Candidate'] = ['Romney','Santorum', 'Paul','Gingrich']
# read in the data frames that we created earlier for 2012
Romney = pd.read_csv('../../Data/don/2009_2012_ind_cand/Romney_2012.csv')
Santorum = pd.read_csv('../../Data/don/2009_2012_ind_cand/Santorum_2012.csv')
Paul = pd.read_csv('../../Data/don/2009_2012_ind_cand/Paul_2012.csv') 
Gingrich = pd.read_csv('../../Data/don/2009_2012_ind_cand/Gingrich_2012.csv')

Romney_exp = pd.read_csv('../../Data/exp/2012_ind_cand_exp/Romney_exp.csv')
Santorum_exp = pd.read_csv('../../Data/exp/2012_ind_cand_exp/Santorum_exp.csv')
Paul_exp = pd.read_csv('../../Data/exp/2012_ind_cand_exp/Paul_exp.csv') 
Gingrich_exp = pd.read_csv('../../Data/exp/2012_ind_cand_exp/Gingrich_exp.csv')
def eng_fet_2012(df1,df2,df3):
    for i in df1.index:
        data_frame = df2[i]
        data_frame.set_index('TRANSACTION_DT',inplace = True)
        data_frame.drop(['Unnamed: 0'], axis = 1,inplace = True) 
        q1 = data_frame.loc['2011-01-01':'2011-03-31']
        q2 = data_frame.loc['2011-04-01':'2011-06-30']
        q3 = data_frame.loc['2011-07-01':'2011-09-30']
        q4 = data_frame.loc['2011-10-01':'2011-12-31']
        q1_16 = data_frame.loc['2012-01-01':'2012-03-31']
        q2_16 = data_frame.loc['2012-04-01':'2012-06-30']
        q3_16 = data_frame.loc['2012-07-01':'2012-09-30']
        df1.loc[i,'Q1_Don1'] = q1['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don1'] = q2['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don1'] = q3['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_Don1'] = q4['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_Don2'] = q1_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don2'] = q2_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don2'] = q3_16['TRANSACTION_AMT'].sum()
    for i in  df1.index:
        data_frame_exp = df3[i]
        data_frame_exp.set_index('TRANSACTION_DT',inplace = True)
        data_frame_exp.drop(['Unnamed: 0'], axis = 1,inplace = True)
        q1_exp = data_frame_exp.loc['2011-01-01':'2011-03-31']
        q2_exp = data_frame_exp.loc['2011-04-01':'2011-06-30']
        q3_exp = data_frame_exp.loc['2011-07-01':'2011-09-30']
        q4_exp = data_frame_exp.loc['2011-10-01':'2011-12-31']
        q1_16_exp = data_frame_exp.loc['2012-01-01':'2012-03-31']
        q2_16_exp = data_frame_exp.loc['2012-04-01':'2012-06-30']
        q3_16_exp = data_frame_exp.loc['2012-07-01':'2012-09-30']
        df1.loc[i,'Q1_exp1'] = q1_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp1'] = q2_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp1'] = q3_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_exp1'] = q4_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_exp2'] = q1_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp2'] = q2_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp2'] = q3_16_exp['TRANSACTION_AMT'].sum()
        
    
    return(df1)
df_2012_GOP = eng_fet_2012(df_2012_features_GOP,[Romney, Santorum, Paul, Gingrich],
                          [Romney_exp, Santorum_exp, Paul_exp, Gingrich_exp])
days_in_race_GOP_2012 = [453,319,407,402]
df_2012_GOP['Dropped_out'] = 1
df_2012_GOP.loc[0,'Dropped_out']=0
df_2012_GOP.loc[2,'Dropped_out']=0
df_2012_GOP['Days_in_race'] = 0
for i in df_2012_GOP.index:
    df_2012_GOP.loc[i,'Days_in_race'] = days_in_race_GOP_2012[i]
df_2012_GOP.to_csv('../../Data/Model/2012_modeling_GOP.csv')
df_2016_features_GOP = pd.DataFrame(columns = ['Candidate'])
df_2016_features_DCCC = pd.DataFrame(columns = ['Candidate']) 
df_2016_features_GOP['Candidate'] = ['Trump', 'Cruz','Kasich','Rubio','Carson','Bush','Paul',
                                     'Christie', 'Huckabee','Fiorina','Gilmore','Santorum',
                                     'Perry','Walker', 'Jindal', 'Grahm','Pataki']
df_2016_features_DCCC['Candidate'] = ['Clinton','Sanders','Omalley']   
# read in the data frames so they can be used in the function
Trump =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Trump_2016_don_clean.csv')
Cruz =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Cruz_2016_don_clean.csv')
Kasich =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Kasich_2016_don_clean.csv')
Rubio =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Rubio_2016_don_clean.csv')
Carson =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Carson_2016_don_clean.csv')
Bush =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Bush_2016_don_clean.csv')
Paul =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Paul_2016_don_clean.csv')
Christie =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Christie_2016_don_clean.csv')
Huckabee =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Huckabee_2016_don_clean.csv')
Fiorina =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Fiorina_2016_don_clean.csv')
Gilmore =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Gilmore_2016_don_clean.csv')
Santorum =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Santorm_2016_don_clean.csv')
Perry =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Perry_2016_don_clean.csv')
Walker =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Walker_2016_don_clean.csv')
Jindal =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Jindal_2016_don_clean.csv')
Grahm =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Grahm_2016_don_clean.csv')
Pataki =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Pataki_2016_don_clean.csv')
Clinton =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Clinton_2016_don_clean.csv')
Sanders =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Sanders_2016_don_clean.csv')
Omalley =pd.read_csv('../../Data/don/2013_2016_ind_cand_final/Omalley_2016_don_clean.csv')

Trump_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Trump_exp.csv')
Cruz_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Cruz_exp.csv')
Kasich_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Kasich_exp.csv')
Rubio_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Rubio_exp.csv')
Carson_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Carson_exp.csv')
Bush_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Bush_exp.csv')
Paul_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Paul_exp.csv')
Christie_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Christie_exp.csv')
Huckabee_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Huckabee_exp.csv')
Fiorina_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Fiorina_exp.csv')
Gilmore_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Gilmore_exp.csv')
Santorum_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Santorum_exp.csv')
Perry_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Perry_exp.csv')
Walker_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Walker_exp.csv')
Jindal_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Jindal_exp.csv')
Grahm_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Graham_exp.csv')
Pataki_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Pataki_exp.csv')
Clinton_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Clinton_exp.csv')
Sanders_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/Sanders_exp.csv')
Omalley_exp =pd.read_csv('../../Data/exp/2016_ind_cand_exp/OMalley_exp.csv')


def eng_fet_2020(df1,df2,df3):
    for i in df1.index:
        data_frame = df2[i]
        data_frame.set_index('TRANSACTION_DT',inplace = True)
        data_frame.drop(['Unnamed: 0'], axis = 1,inplace = True)
        data_frame.drop(['Unnamed: 0.1'], axis = 1,inplace = True) 
        q1 = data_frame.loc['2015-01-01':'2015-03-31']
        q2 = data_frame.loc['2015-04-01':'2015-06-30']
        q3 = data_frame.loc['2015-07-01':'2015-09-30']
        q4 = data_frame.loc['2015-10-01':'2015-12-31']
        q1_16 = data_frame.loc['2016-01-01':'2016-03-31']
        q2_16 = data_frame.loc['2016-04-01':'2016-06-30']
        q3_16 = data_frame.loc['2016-07-01':'2016-09-30']
        df1.loc[i,'Q1_Don1'] = q1['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don1'] = q2['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don1'] = q3['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_Don1'] = q4['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_Don2'] = q1_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don2'] = q2_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don2'] = q3_16['TRANSACTION_AMT'].sum()
    for i in  df1.index:
        data_frame_exp = df3[i]
        data_frame_exp.set_index('TRANSACTION_DT',inplace = True)
        data_frame_exp.drop(['Unnamed: 0'], axis = 1,inplace = True)
        q1_exp = data_frame_exp.loc['2015-01-01':'2015-03-31']
        q2_exp = data_frame_exp.loc['2015-04-01':'2015-06-30']
        q3_exp = data_frame_exp.loc['2015-07-01':'2015-09-30']
        q4_exp = data_frame_exp.loc['2015-10-01':'2015-12-31']
        q1_16_exp = data_frame_exp.loc['2016-01-01':'2016-03-31']
        q2_16_exp = data_frame_exp.loc['2016-04-01':'2016-06-30']
        q3_16_exp = data_frame_exp.loc['2016-07-01':'2016-09-30']
        df1.loc[i,'Q1_exp1'] = q1_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp1'] = q2_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp1'] = q3_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_exp1'] = q4_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_exp2'] = q1_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp2'] = q2_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp2'] = q3_16_exp['TRANSACTION_AMT'].sum()
        
    
    return(df1)
    df_2016_GOP = eng_fet_2016(df_2016_features_GOP,[Trump, Cruz, Kasich, Rubio , Carson, Bush,
                              Paul, Christie, Huckabee, Fiorina, Gilmore,
                              Santorum, Perry, Walker, Jindal ,Grahm, Pataki],
                           [Trump_exp, Cruz_exp, Kasich_exp,Rubio_exp , Carson_exp, Bush_exp,
                              Paul_exp, Christie_exp, Huckabee_exp, Fiorina_exp, Gilmore_exp,
                              Santorum_exp, Perry_exp, Walker_exp, Jindal_exp ,Grahm_exp,
                            Pataki_exp])
df_2016_DCCC = eng_fet_2016(df_2016_features_DCCC,[Clinton,Sanders,Omalley],
                            [Clinton_exp,Sanders_exp,Omalley_exp])
df_2016_GOP['Dropped_out'] = 1
df_2016_DCCC['Dropped_out'] = 1
df_2016_GOP.loc[0,'Dropped_out']=0
df_2016_DCCC.loc[0,'Dropped_out']=0
df_2016_GOP['Days_in_race'] = 0
df_2016_DCCC['Days_in_race'] = 0
days_in_race_GOP = [323,407,288,337,306,250,302,225,272,282,198,252,99,70,146,203,215]
for i in df_2016_GOP.index:
    df_2016_GOP.loc[i,'Days_in_race'] = days_in_race_GOP[i]
days_in_race_DCCC = [329,427,247]
for i in df_2016_DCCC.index:
    df_2016_DCCC.loc[i,'Days_in_race'] = days_in_race_DCCC[i]
df_2016_GOP.to_csv('../../Data/Model/2016_modeling_GOP.csv')
df_2016_DCCC.to_csv('../../Data/Model/2016_modeling_DCCC.csv')

Biden = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Biden.csv')
Booker = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Booker.csv')
Buttigieg = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Buttigieg.csv')
Castro = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Castro.csv')
Delaney = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Delaney.csv')
Gabbard = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Gabbard.csv')
Klobuchar = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Klobuchar.csv')
Sanders = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Sanders.csv')
Steyer = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Steyer.csv')
Warren = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Warren.csv')
Williamson = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Williamson.csv')
Yang = pd.read_csv('../../Data/don/2017_2020_ind_cand_final/Yang.csv')

Biden_exp = pd.read_csv('../../Data/exp/2020_exp/Biden_exp.csv')
Booker_exp = pd.read_csv('../../Data/exp/2020_exp/Booker_exp.csv')
Buttigieg_exp = pd.read_csv('../../Data/exp/2020_exp/Buttigieg_exp.csv')
Castro_exp = pd.read_csv('../../Data/exp/2020_exp/Castro_exp.csv')
Delaney_exp = pd.read_csv('../../Data/exp/2020_exp/Delaney_exp.csv')
Gabbard_exp = pd.read_csv('../../Data/exp/2020_exp/Gabbard_exp.csv')
Klobuchar_exp = pd.read_csv('../../Data/exp/2020_exp/Klobuchar_exp.csv')
Sanders_exp = pd.read_csv('../../Data/exp/2020_exp/Sanders_exp.csv')
Steyer_exp = pd.read_csv('../../Data/exp/2020_exp/Steyer_exp.csv')
Warren_exp = pd.read_csv('../../Data/exp/2020_exp/Warren_exp.csv')
Williamson_exp = pd.read_csv('../../Data/exp/2020_exp/Williamson_exp.csv')
Yang_exp = pd.read_csv('../../Data/exp/2020_exp/Yang_exp.csv')

df_2020_features_DCCC = pd.DataFrame(columns = ['Candidate']) 

df_2020_features_DCCC['Candidate'] = ['Biden','Booker','Buttigieg','Castro',
                                     'Gabbard','Klobuchar','Sanders','Steyer','Warren',
                                     'Williamson','Yang']
def eng_fet_2020(df1,df2,df3):
    for i in df1.index:
        data_frame = df2[i]
        data_frame.set_index('TRANSACTION_DT',inplace = True)
        data_frame.drop(['Unnamed: 0'], axis = 1,inplace = True)
        data_frame.drop(['Unnamed: 0.1'], axis = 1,inplace = True) 
        q1 = data_frame.loc['2019-01-01':'2019-03-31']
        q2 = data_frame.loc['2019-04-01':'2019-06-30']
        q3 = data_frame.loc['2019-07-01':'2019-09-30']
        q4 = data_frame.loc['2019-10-01':'2019-12-31']
        q1_16 = data_frame.loc['2020-01-01':'2020-03-31']
        q2_16 = data_frame.loc['2020-04-01':'2020-06-30']
        q3_16 = data_frame.loc['2020-07-01':'2020-09-30']
        df1.loc[i,'Q1_Don1'] = q1['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don1'] = q2['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don1'] = q3['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_Don1'] = q4['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_Don2'] = q1_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_Don2'] = q2_16['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_Don2'] = q3_16['TRANSACTION_AMT'].sum()
    for i in  df1.index:
        data_frame_exp = df3[i]
        data_frame_exp.set_index('TRANSACTION_DT',inplace = True)
        data_frame_exp.drop(['Unnamed: 0'], axis = 1,inplace = True)
        q1_exp = data_frame_exp.loc['2019-01-01':'2019-03-31']
        q2_exp = data_frame_exp.loc['2019-04-01':'2019-06-30']
        q3_exp = data_frame_exp.loc['2019-07-01':'2019-09-30']
        q4_exp = data_frame_exp.loc['2019-10-01':'2019-12-31']
        q1_16_exp = data_frame_exp.loc['2020-01-01':'2020-03-31']
        q2_16_exp = data_frame_exp.loc['2020-04-01':'2020-06-30']
        q3_16_exp = data_frame_exp.loc['2020-07-01':'2020-09-30']
        df1.loc[i,'Q1_exp1'] = q1_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp1'] = q2_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp1'] = q3_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q4_exp1'] = q4_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q1_exp2'] = q1_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q2_exp2'] = q2_16_exp['TRANSACTION_AMT'].sum()
        df1.loc[i,'Q3_exp2'] = q3_16_exp['TRANSACTION_AMT'].sum()
        
    
    return(df1)
df_2020_dccc = eng_fet_2020(df_2020_features_DCCC,[Biden,Booker,Buttigieg,Castro,
                                     Gabbard,Klobuchar,Sanders,Steyer,Warren,
                                     Williamson,Yang],[Biden_exp,Booker_exp,Buttigieg_exp,
                                                       Castro_exp,Gabbard_exp,Klobuchar_exp,
                                                       Sanders_exp,Steyer_exp,Warren_exp,
                                                       Williamson_exp,Yang_exp])
df_2020_dccc['Dropped_out'] = 0
df_2020_dccc['Days_in_race'] = 0
days_in_race_DCCC_2020 = [223,306,234,326,327,297,288,148,288,384,290]
for i in df_2020_dccc.index:
    df_2020_dccc.loc[i,'Days_in_race'] = days_in_race_DCCC_2020[i]
df_2020_dccc.to_csv('../../Data/Model/2020_modeling_DCCC.csv')



















