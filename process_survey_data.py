import pandas as pd
import sys

def rename_df_index_and_columns(mapping, df):
    df_temp = df.copy()
    df_temp.index.names = list(map(lambda name: mapping.get(name, name), df_temp.index.names))
    return df_temp.rename(columns=mapping)


def check_for_lang(lang, string_to_check):
    return (lang.lower() + ";") in string_to_check.lower() \
           or (";" + lang.lower()) in string_to_check.lower() \
           or ("; " + lang.lower()) in string_to_check.lower() \
           or string_to_check.lower() == lang.lower()


def check_for_dev_types(string_to_check):
    return "data scientist" in string_to_check.lower() \
           or "machine learning" in string_to_check.lower() \
           or "statistics" in string_to_check.lower()


def main():
    # import the survey results
    print("Loading survey data")
    df_survey_2021 = pd.read_csv(r".\data\developer_survey_2021\survey_results_public.csv")
    df_survey_2020 = pd.read_csv(r".\data\developer_survey_2020\survey_results_public.csv")
    df_survey_2019 = pd.read_csv(r".\data\developer_survey_2019\survey_results_public.csv")
    # ambiguous dtypes in 2018 survey, handled by setting them all to object
    df_survey_2018 = pd.read_csv(r".\data\developer_survey_2018\survey_results_public.csv",
                                 dtype=object)
    df_survey_2017 = pd.read_csv(r".\data\developer_survey_2017\survey_results_public.csv")

    # add a year field to each dataframe
    df_survey_2021["Year"] = 2021
    df_survey_2020["Year"] = 2020
    df_survey_2019["Year"] = 2019
    df_survey_2018["Year"] = 2018
    df_survey_2017["Year"] = 2017

    # make a combined dataframe for all years
    df_survey_combined = df_survey_2021[["Year", "DevType", "LanguageHaveWorkedWith", "LanguageWantToWorkWith"]].copy()

    mapping = {"LanguageWorkedWith": "LanguageHaveWorkedWith", "LanguageDesireNextYear": "LanguageWantToWorkWith"}
    df_survey_sliced = df_survey_2020[["Year", "DevType", "LanguageWorkedWith", "LanguageDesireNextYear"]].copy()
    df_survey_sliced = rename_df_index_and_columns(mapping, df_survey_sliced)
    df_survey_combined = df_survey_combined.append(df_survey_sliced)

    df_survey_sliced = df_survey_2019[["Year", "DevType", "LanguageWorkedWith", "LanguageDesireNextYear"]].copy()
    df_survey_sliced = rename_df_index_and_columns(mapping, df_survey_sliced)
    df_survey_combined = df_survey_combined.append(df_survey_sliced)

    mapping = {"LanguageWorkedWith": "LanguageHaveWorkedWith", "LanguageDesireNextYear": "LanguageWantToWorkWith"}
    df_survey_sliced = df_survey_2018[["Year", "DevType", "LanguageWorkedWith", "LanguageDesireNextYear"]].copy()
    df_survey_sliced = rename_df_index_and_columns(mapping, df_survey_sliced)
    df_survey_combined = df_survey_combined.append(df_survey_sliced)

    mapping = {"DeveloperType": "DevType", "HaveWorkedLanguage": "LanguageHaveWorkedWith",
               "WantWorkLanguage": "LanguageWantToWorkWith"}
    df_survey_sliced = df_survey_2017[["Year", "DeveloperType", "HaveWorkedLanguage", "WantWorkLanguage"]].copy()
    df_survey_sliced = rename_df_index_and_columns(mapping, df_survey_sliced)
    df_survey_combined = df_survey_combined.append(df_survey_sliced)

    # reduce survey to only responses from data science related developers
    series_data_scientist = df_survey_combined.apply(lambda x:
                                                     True if check_for_dev_types(str(x["DevType"]))
                                                     else False, axis=1)
    df_survey_combined["IsDataScientist"] = series_data_scientist
    df_survey_combined = df_survey_combined[df_survey_combined["IsDataScientist"]]

    # engineer features determining if response indicated worked with applicable languages
    print("Engineering new features")
    series_python_worked = df_survey_combined.apply(lambda x:
                                                    True if check_for_lang("Python", str(x["LanguageHaveWorkedWith"]))
                                                    else False, axis=1)
    series_r_worked = df_survey_combined.apply(lambda x:
                                               True if check_for_lang("R", str(x["LanguageHaveWorkedWith"]))
                                               else False, axis=1)
    series_julia_worked = df_survey_combined.apply(lambda x:
                                                   True if check_for_lang("Julia", str(x["LanguageHaveWorkedWith"]))
                                                   else False, axis=1)
    df_survey_combined["PythonWorkedWith"] = series_python_worked
    df_survey_combined["RWorkedWith"] = series_r_worked
    df_survey_combined["JuliaWorkedWith"] = series_julia_worked

    # engineer features determining if response indicated wanted to work with applicable languages
    series_python_want = df_survey_combined.apply(lambda x:
                                                  True if check_for_lang("Python", str(x["LanguageWantToWorkWith"]))
                                                  else False, axis=1)
    series_r_want = df_survey_combined.apply(lambda x:
                                             True if check_for_lang("R", str(x["LanguageWantToWorkWith"]))
                                             else False, axis=1)
    series_julia_want = df_survey_combined.apply(lambda x:
                                                 True if check_for_lang("Julia", str(x["LanguageWantToWorkWith"]))
                                                 else False, axis=1)
    df_survey_combined["PythonWantWorkWith"] = series_python_want
    df_survey_combined["RWantWorkWith"] = series_r_want
    df_survey_combined["JuliaWantWorkWith"] = series_julia_want

    # remove responses that did not list any languages
    print("Cleaning data set")
    df_survey_combined.dropna(subset=("LanguageHaveWorkedWith", "LanguageWantToWorkWith"), inplace=True)
    df_survey_combined.to_csv(r".\data\processed_survey_data.csv")
