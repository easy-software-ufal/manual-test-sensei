import os
from data import get_filtered_df_by_smell_name
SMELL_NAMES = ['Misplaced Precondition', 'Unverified Action']

def transformation_closure(df):
    def sentence_not_found(start_pos):
        return start_pos == -1
    def misplaced_precondition(df):
        filtered_df = get_filtered_df_by_smell_name(df,'Misplaced Precondition')
        for _, row in filtered_df.iterrows():
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                # open the file for reading and writing
                with open(row['Copy Path'], 'r+') as file:
                    # read the entire contents of the file into a string
                    contents = file.read()
                    # find the start and end positions of the block of text to move
                    start_pos = contents.find('<dt>' + row['Sentence'] + '</dt>') #this is where the smell will be
                    end_pos = start_pos + len('<dt>' + row['Sentence'] + '</dt>')
                    
                    # extract the block of text to move
                    block = contents[start_pos+len('<dt>'):end_pos-len('</dt>')]

                    # remove the block from its original location
                    contents = contents[:start_pos] + contents[end_pos:]
                    
                    # find the position where the block should be moved to, i.e, before the <dl> tag
                    dl_pos = contents[:start_pos].rfind('<dl>')
                    
                    # insert the block into its new location
                    contents = contents[:dl_pos] + block + "\n" + contents[dl_pos:]

                    # go back to the beginning of the file and overwrite its contents
                    file.seek(0)
                    file.truncate(0)
                    file.write(contents)

    def unverified_action(df):
        filtered_df = get_filtered_df_by_smell_name(df,'Unverified Action')
        for _, row in filtered_df.iterrows():
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                # open the file for reading and writing
                with open(row['Copy Path'], 'r+') as file:
                    # read the entire contents of the file into a string
                    contents = file.read()
                    # find the start and end positions of the block of text to move
                    start_pos = contents.find('<dt>' + row['Sentence'] + '</dt>') #this is where the smell will be
                    if sentence_not_found(start_pos):
                        continue
                    
                    end_pos = start_pos + len('<dt>' + row['Sentence'] + '</dt>')

                    #insert a verification block
                    contents = contents[:end_pos] + "\n\t\t<dd>[FILL VERIFICATION]</dd>" + contents[end_pos:]
                    # go back to the beginning of the file and overwrite its contents
                    file.seek(0)
                    file.truncate(0)
                    file.write(contents)

    def misplaced_action(df):
        pass

    def misplaced_verification(df):
        pass

    def ambiguous_test(df):
        pass

    def conditional_test_logic(df):
        pass

    def eager_action(df):
        pass
    
    switcher = {
    'Misplaced Precondition': misplaced_precondition(df),
    'Unverified Action' : unverified_action(df)
    }
    for smell_name in SMELL_NAMES:
        switcher.get(smell_name)