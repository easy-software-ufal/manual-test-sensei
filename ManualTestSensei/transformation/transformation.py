import os
from data import get_filtered_df_by_smell_name

SMELL_NAMES = ['Misplaced Precondition']

def transformation_closure(df):
    def already_transformed(start_pos, contents):
        dt_pos = contents[:start_pos].rfind('<dt>')
        if start_pos == dt_pos + 4:
            return False
        return True 

    def misplaced_precondition(df):
        filtered_df = get_filtered_df_by_smell_name(df,'Misplaced Precondition')
        #for path in df['Copy Path']:
        for _, row in filtered_df.iterrows():
            #breakpoint()
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                # open the file for reading and writing
                with open(row['Copy Path'], 'r+') as file:
                # read the entire contents of the file into a string
                    contents = file.read()
                    # find the start and end positions of the block of text to move
                    start_pos = contents.find(row['Sentence']) #this is where the smell will be

                    if not already_transformed(start_pos, contents):
                        end_pos = start_pos + len(row['Sentence'])
                        
                        # extract the block of text to move
                        block = contents[start_pos:end_pos]

                        # find the <dt> and </dt> tags to remove
                        dt_end_pos = contents.find("</dt>", start_pos) + len("</dt>")
                        dt_start_pos = contents[:start_pos].rfind('<dt>')

                        # remove the block from its original location
                        contents = contents[:dt_start_pos] + contents[dt_end_pos:]

                        # find the position where the block should be moved to, i.e, before the <dl> tag
                        dl_pos = contents[:start_pos].rfind('<dl>')
                        
                        # insert the block into its new location
                        contents = contents[:dl_pos] + block + "\n" + contents[dl_pos:]

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

    def unverified_action(df):
        pass

    def eager_action(df):
        pass
    
    switcher = {
    'Misplaced Precondition': misplaced_precondition(df)
    }
    for smell_name in SMELL_NAMES:
        switcher.get(smell_name)