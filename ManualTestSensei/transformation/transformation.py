
from data import get_filtered_df_by_smell_name


SMELL_NAMES = ['Conditional Test Logic', 'Eager Action', 'Misplaced Action',
       'Ambiguous Test', 'Unverified Action', 'Misplaced Verification',
       'Misplaced Precondition']


def transformation_closure():
    def misplaced_precondition(df):
        filtered_df = get_filtered_df_by_smell_name(df,'Misplaced Precondition')
        
        # open the file for reading and writing
        with open('file.txt', 'r+') as file:
        # read the entire contents of the file into a string
            contents = file.read()

            # find the start and end positions of the block of text to move
            start_pos = contents.find(smell_sentence) #this is where the smell will be
            end_pos = start_pos + len(smell_sentence)

            # extract the block of text to move
            block = contents[start_pos:end_pos]

            # remove the block from its original location
            contents = contents[:start_pos] + contents[end_pos:]

            # find the position where the block should be moved to
            new_pos = contents.find('PLACE TO MOVE BLOCK')

            # insert the block into its new location
            contents = contents[:new_pos] + block + contents[new_pos:]

            # go back to the beginning of the file and overwrite its contents
            file.seek(0)
            file.write(contents)
        pass

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

    return 1