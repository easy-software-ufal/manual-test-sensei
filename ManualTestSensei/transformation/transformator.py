import os, re, logging, spacy, ast
try:
    from . import transformation_data
except ImportError:
    import transformation_data
#SMELL_NAMES = ['Misplaced Precondition', 'Unverified Action', 'Misplaced Action', 'Misplaced Verification']
SMELL_NAMES = ['Eager Action']
skipped_tests = 0

def transformation_closure(df):
    #breakpoint()
    log = logging.getLogger(__name__)
    def sentence_not_found(start_pos):
        return start_pos == -1
    def misplaced_precondition(df):
        breakpoint()
        log.debug('MisPre')
        global skipped_tests
        filtered_df = transformation_data.get_filtered_df_by_smell_name(df,'Misplaced Precondition')
        for _, row in filtered_df.iterrows():
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                # open the file for reading and writing
                with open(row['Copy Path'], 'r+', encoding='utf8') as file:
                    # read the entire contents of the file into a string
                    contents = file.read()
                    # find the start and end positions of the block of text to move
                    start_pos = contents.find('<dt>' + row['Sentence'] + '</dt>') #this is where the smell will be
                    if sentence_not_found(start_pos):
                        skipped_tests += 1
                        continue

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
        log.debug('UnvAct')
        global skipped_tests
        filtered_df = transformation_data.get_filtered_df_by_smell_name(df,'Unverified Action')
        for _, row in filtered_df.iterrows():
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                # open the file for reading and writing
                with open(row['Copy Path'], 'r+', encoding='utf8') as file:
                    # read the entire contents of the file into a string
                    contents = file.read()
                    # find the start and end positions of the block of text to move
                    start_pos = contents.find('<dt>' + row['Sentence'] + '</dt>') #this is where the smell will be
                    if sentence_not_found(start_pos):
                        skipped_tests += 1
                        continue

                    end_pos = start_pos + len('<dt>' + row['Sentence'] + '</dt>')

                    #insert a verification block
                    contents = contents[:end_pos] + "\n\t\t<dd>[FILL VERIFICATION]</dd>" + contents[end_pos:]
                    # go back to the beginning of the file and overwrite its contents
                    file.seek(0)
                    file.truncate(0)
                    file.write(contents)

    def misplaced_action(df):
        log.debug('MisAct')
        global skipped_tests

        filtered_df = transformation_data.get_filtered_df_by_smell_name(df,'Misplaced Action')
        breakpoint()
        for _, row in filtered_df.iterrows():
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                with open(row['Copy Path'], 'r+', encoding='utf8') as file:
                    contents = file.read()

                    start_pos = contents.find('<dd>' + row['Sentence'] + '</dd>')
                    if sentence_not_found(start_pos):
                        skipped_tests += 1
                        continue

                    end_pos = start_pos + len('<dd>' + row['Sentence'] + '</dd>')

                    dt_pos = contents[:start_pos].rfind('<dt>')
                    dd_pos = contents.find("</dd>", dt_pos)
                    dd_last_pos = contents.rfind("</dd>", dd_pos, contents.find ("<dt>", dd_pos)) + len("</dd>") + 1
                    block = "<dt>" + contents[start_pos+len('<dd>'):end_pos-len('</dd>')] + "</dt>"

                    contents = contents[:dd_last_pos] + "\t" + block + "\n\t\t<dd>[FILL VERIFICATION]</dd>\n" + contents[dd_last_pos:]
                    start_pos = contents.find('<dd>' + row['Sentence'] + '</dd>')
                    end_pos = start_pos + len('<dd>' + row['Sentence'] + '</dd>')
                    contents = contents[:start_pos] + contents[end_pos:]

                    start_pos = contents.find('<dt>' + row['Sentence'] + '</dt>')

                    prev_dt = contents[:start_pos].rfind('<dt>')
                    prev_dt_end_pos = contents.find("</dt>", prev_dt) + len("</dt>")
                    temp = contents[:prev_dt_end_pos] + re.sub(r'\s+', '', contents[prev_dt_end_pos:])
                    dd_pos = temp.find("<dd>", prev_dt_end_pos-1)

                    if prev_dt_end_pos != dd_pos:
                        contents = contents[:prev_dt_end_pos] + "\n\t\t<dd>[FILL VERIFICATION]</dd>" + contents[prev_dt_end_pos:]
                    # go back to the beginning of the file and overwrite its contents
                    file.seek(0)
                    file.truncate(0)
                    file.write(contents)

    def misplaced_verification(df):
        log.debug('MisVer')
        global skipped_tests
        filtered_df = transformation_data.get_filtered_df_by_smell_name(df,'Misplaced Verification')
        for _, row in filtered_df.iterrows():
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                with open(row['Copy Path'], 'r+', encoding='utf8') as file:
                    contents = file.read()
                    start_pos = contents.find('<dt>' + row['Sentence'] + '</dt>')
                    if sentence_not_found(start_pos):
                        skipped_tests += 1
                        continue
                    end_pos = start_pos + len('<dt>' + row['Sentence'] + '</dt>')
                    contents = contents[:start_pos] + "\t<dd>" + row['Sentence'] + '</dd>' + contents[end_pos:]
                    file.seek(0)
                    file.truncate(0)
                    file.write(contents)

    def ambiguous_test(df):
        pass

    def conditional_test_logic(df):
        pass

    def eager_action(df):
        global skipped_tests
        filtered_df = transformation_data.get_filtered_df_by_smell_name(df,'Eager Action')
        for _, row in filtered_df.iterrows():
            if os.path.exists(row['Copy Path']) and os.path.isfile(row['Copy Path']):
                # open the file for reading and writing
                with open(row['Copy Path'], 'r+', encoding='utf8') as file:
                    contents = file.read()
                    start_pos = contents.find('<dt>' + row['Sentence'] + '</dt>')
                    if sentence_not_found(start_pos):
                        skipped_tests += 1
                        continue

                    end_pos = start_pos + len('<dt>' + row['Sentence'] + '</dt>')
                    
                    nlp = spacy.load("en_core_web_sm")
                    terms = row['Term']
                    terms = ast.literal_eval(terms)
                    terms = terms[1:]
                    for index, item in enumerate(terms):
                        doc = nlp(item)
                        if doc[0].pos_ == 'CCONJ' or doc[0].text == ',':
                            sentence = item.split()
                            sentence = ' '.join(sentence[1:])
                            terms[index] = sentence
                    
                    sentence = '<dt>' + row['Sentence'] + '</dt>'
                    output = sentence
                    for term in terms:
                        output = output.replace(term, "</dt>\n\t<dt> " + term)

                    pattern = r"<dt>(.*?)</dt>"
                    result = [item.strip() for item in re.findall(pattern, output)]

                    new_result = []
                    for item in result:
                        doc = nlp(item)
                        if len(doc) > 0:
                            if doc[-1].pos_ == 'CCONJ' or doc[-1].text == ',':
                                new_result.append(doc[:-1])
                            else:
                                new_result.append(doc)
                    output = ''
                    for i, element in enumerate(new_result):
                        output += "<dt>" + str(element) + "</dt>"
                        if i != len(new_result)-1:
                            output += "\n\t"
                    contents = contents[:start_pos] + output + contents[end_pos:]

                    file.seek(0)
                    file.truncate(0)
                    file.write(contents)

    switcher = {
    #'Misplaced Precondition': misplaced_precondition(df),
    'Eager Action': eager_action(df)
    #'Unverified Action': unverified_action(df),
    #'Misplaced Action': misplaced_action(df),
    #'Misplaced Verification': misplaced_verification(df)
    }
    for smell_name in SMELL_NAMES:
        switcher.get(smell_name)