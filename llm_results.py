import assemblyai as aai

def transcribe(api_key, filename):

    print("Transcribing file")
    aai.settings.api_key = api_key    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(filename)
    transcript_id = transcript.id

    return transcript_id


def group_analyse(ids_list):
    
    print("Starting analysis")
    transcript_group = aai.TranscriptGroup.get_by_ids(ids_list)

    pros_prompt = "Create a list of pros about the product at hand, commonly mentioned in these video reviews. Limit it to 10 most relevant points. Only return the pros as a list, do not return any other text."
    pros_result = transcript_group.lemur.task(
                pros_prompt, final_model=aai.LemurModel.claude3_5_sonnet
                )
    
    cons_prompt = "Create a list of cons about the product at hand, commonly mentioned in these video reviews. Limit it to 10 most relevant points. Only return the cons as a list, do not return any other text."
    cons_result = transcript_group.lemur.task(
                cons_prompt, final_model=aai.LemurModel.claude3_5_sonnet
                )

    return pros_result.response, cons_result.response