# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import src.data_download as dwn
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Example usage:
    competition = 'competitions/web-traffic-time-series-forecasting'
    destination = '../data/zip/'
    kaggle_json_path = 'C:/Users/albyd/python_group_project/group3_project_wikipedia/.kaggle/kaggle.json'

    dwn.download_and_unzip_kaggle_data(competition, destination, kaggle_json_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

