import json
import pandas as pd

def load_results(json_files):
    results = []
    for file in json_files:
        with open(file) as json_file:
            data = json.load(json_file)
            for result in data['individualResults']:
                print(result['displayName'], result['companyName'], result['bestFinishTime'])
                results.append({
                    'displayName': result['displayName'], 
                    'companyName': result['companyName'], 
                    'bestFinishTime': result['bestFinishTime']
                })
    return results

def process_results(results, scorer_count):
    df = pd.DataFrame(results)

    df2 = (
        df.groupby('companyName')
        .head(scorer_count)
        .groupby('companyName')
        .filter(lambda x: len(x) >= scorer_count)
        .sort_values(by=['companyName'])
    )

    print(df2)

    df3 = (
        df2.groupby('companyName')['bestFinishTime']
        .sum()
        .sort_values()
        .reset_index()
    )

    print(df3)

    df3.to_csv('jpm_score.csv', header=True)

def main():
    json_files = ['results100.json','results200.json','results300.json']
    results = load_results(json_files)
    # can adjust scorer_count as desired. companies with less than scorer_count will not be included.
    process_results(results, scorer_count=5)

if __name__ == "__main__":
    main()