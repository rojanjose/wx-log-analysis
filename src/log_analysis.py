import json
import csv
import io

from utils.model_infer import ModelInference
from utils.presto_conn import PrestoConnection

#Run LLM model inference
def run_inference(generator):
    generator.get_token()
    model_response = generator.generate_text()
    print(f"Model response: \n{model_response}")

# Create a CSV writer object with a custom line terminator
def rows_to_csv_string(data):
    output = io.StringIO()
    csv_writer = csv.writer(output, lineterminator='\n')

    for row in data:
        csv_writer.writerow(row)

    # Retrieve the CSV content as a string
    csv_string = output.getvalue()
    output.close()

    return csv_string


def run_fileio_analysis(presto_inst, generator):

    # Presto query to extract file read/write data for a time window
    query = "SELECT * from prostgre_log.public.file_io \
                WHERE io_timestamp BETWEEN TIMESTAMP '2024-05-09 17:00:00.000' AND TIMESTAMP '2024-05-09 20:12:00.000'"
    
    print("Fetching read/write metadata from log database...")
    data = presto_inst.query(query)
    presto_inst.close_connection()
    csv_string = rows_to_csv_string(data)
    print(csv_string)

    print("\nGenerating LLM prompt using the log context...")
    prompt_file = './prompts/file_reads_writes_summarization.txt'
    with open(prompt_file, 'r') as file:
        prompt = file.read()

    payload_templ_file = './data/payload_templ.json'
    with open(payload_file, 'r') as file:
        payload = json.load(file)

    payload_file = './data/payload_file_reads_writes_summarization.json'
    with open(payload_file, 'w') as file:
        payload['input'] = prompt.format(context_data=csv_string)
        json.dump(payload, file, indent=4)

    print("\nAnalyzing log data using GenAI...")
    generator.set_payload(payload_file)
    run_inference(generator)


def main():
    
    presto_inst = PrestoConnection()
    presto_inst.connect(False)

    generator = ModelInference()

    run_fileio_analysis(presto_inst, generator)

    # run_disk_analysis(presto_inst, generator)
    # run_user_session_analysis(presto_inst, generator)


if __name__ == "__main__":
    main()



