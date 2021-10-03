from os.path import exists
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import process_survey_data


def main():
    # load processed survey data
    if exists(r".\data\processed_survey_data.csv"):
        df_survey_combined = pd.read_csv(r".\data\processed_survey_data.csv")
    else:
        process_survey_data.main()
        df_survey_combined = pd.read_csv(r".\data\processed_survey_data.csv")

    # get overall count and the count of each language for each year
    python_worked, python_want, r_worked, r_want, julia_worked, julia_want = ({} for i in range(6))
    years = (2021, 2020, 2019, 2018, 2017)
    for year in years:
        df_curr_year = df_survey_combined[df_survey_combined["Year"] == year]
        total_entries = df_curr_year["Year"].size
        python_worked[year] = df_curr_year[df_curr_year["PythonWorkedWith"]]["PythonWorkedWith"].size / total_entries
        r_worked[year] = df_curr_year["RWorkedWith"][df_curr_year["RWorkedWith"]].size / total_entries
        julia_worked[year] = df_curr_year["JuliaWorkedWith"][df_curr_year["JuliaWorkedWith"]].size / total_entries
        python_want[year] = df_curr_year["PythonWantWorkWith"][df_curr_year["PythonWantWorkWith"]].size / total_entries
        r_want[year] = df_curr_year["RWantWorkWith"][df_curr_year["RWantWorkWith"]].size / total_entries
        julia_want[year] = df_curr_year["JuliaWantWorkWith"][df_curr_year["JuliaWantWorkWith"]].size / total_entries

    # plot a column chart of the count of each language
    print("Creating charts")
    fig1, ax1 = plt.subplots(1, figsize=(11, 8.5), dpi=400)

    num_column_groups = 3
    counts_worked_2021 = (python_worked[2021], r_worked[2021], julia_worked[2021])
    counts_want_2021 = (python_want[2021], r_want[2021], julia_want[2021])

    column_group_pos = np.arange(num_column_groups)
    width = 0.35
    ax1.bar(column_group_pos, counts_worked_2021, width -0.01, label="Worked with", color="steelblue")
    ax1.bar(column_group_pos + width, counts_want_2021, width - 0.01, label="Want to work with", color="goldenrod")

    ax1.set_xlabel("Language")
    ax1.set_ylabel("Percent of Developers")
    ax1.set_title("Use of and Interest in Data Science Languages in 2021")
    ax1.set_xticks(column_group_pos + width / 2)
    ax1.set_xticklabels(["Python", "R", "Julia"])
    ax1.tick_params(axis="x", which="both", bottom=False)
    ax1.set_ylim(ymin=0, ymax=1)
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
    ax1.legend(loc="best")
    ax1.annotate("Source: $\it{Stack\ Overflow\ Developer\ Survey}$", xy=(0, 0), xytext=(-110, -30), 
                 textcoords='offset points', color="black", fontsize=8)

    fig1.savefig(r".\output\data-science-languages.png")

    # plot line chart showing growth of developers using Julia and wanting to use Julia
    # missing 2019 data points for Julia
    fig2, ax2 = plt.subplots(1, figsize=(11, 8.5), dpi=400)

    years = (2017, 2018, 2020, 2021)
    worked_julia = (julia_worked[2017], julia_worked[2018], julia_worked[2020], julia_worked[2021])
    want_julia = (julia_want[2017], julia_want[2018], julia_want[2020], julia_want[2021])
    ax2.plot(years, worked_julia, marker="o", label="Worked with Julia", color="steelblue")
    ax2.plot(years, want_julia, marker="o", label="Want to work with Julia", color="mediumseagreen")

    ax2.set_ylabel("Percent of Developers")
    ax2.set_title("Growth of Use and Interest in Julia")
    ax2.set_xticks((2017, 2018, 2019, 2020, 2021))
    ax2.set_ylim(ymin=0, ymax=.18)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
    ax2.legend(loc="best")
    ax2.annotate("Source: $\it{Stack\ Overflow\ Developer\ Surveys}$", xy=(2017, 0), xytext=(-68, -30), 
                 textcoords='offset points', color="black", fontsize=8)

    fig2.savefig(r".\output\julia.png")

    # plot line chart showing growth of developers using and and wanting to use Python and R
    fig3, ax3 = plt.subplots(1, figsize=(11, 8.5), dpi=400)

    python_color = "mediumseagreen"
    r_color = "steelblue"
    years = (2017, 2018, 2019, 2020, 2021)
    worked_python = (python_worked[2017], python_worked[2018], python_worked[2019], python_worked[2020], python_worked[2021])
    want_python = (python_want[2017], python_want[2018], python_want[2019], python_want[2020], python_want[2021])
    worked_r = (r_worked[2017], r_worked[2018], r_worked[2019], r_worked[2020], r_worked[2021])
    want_r = (r_want[2017], r_want[2018], r_want[2019], r_want[2020], r_want[2021])
    ax3.plot(years, worked_python, marker="o", linestyle="solid", color=python_color, label="Worked with Python")
    ax3.plot(years, want_python, marker="o", linestyle="dashed", color=python_color, label="Want to work with Python")
    ax3.plot(years, worked_r, marker="o", linestyle="solid", color=r_color, label="Worked with R")
    ax3.plot(years, want_r, marker="o",  linestyle="dashed", color=r_color, label="Want to work with R")

    ax3.set_ylabel("Percent of Developers")
    ax3.set_title("Growth of Use and Interest in Python and R")
    ax3.set_xticks((2017, 2018, 2019, 2020, 2021))
    ax3.set_ylim(ymin=0, ymax=1)
    ax3.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
    ax3.yaxis.grid()
    ax3.legend(loc="best")
    ax3.annotate("Python2 deprecated", xy=(2020, python_want[2020]), xytext=(-30, -30),
                 textcoords='offset points', color="white",
                 arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=-90", color=python_color, linewidth=2),
                 bbox=dict(boxstyle="round", fc=python_color, color=python_color))
    ax3.annotate("Source: $\it{Stack\ Overflow\ Developer\ Surveys}$", xy=(2017, 0), xytext=(-75, -30), 
                 textcoords='offset points', color="black", fontsize=8)

    fig3.savefig(r".\output\python-and-r.png")


if __name__ == "__main__":
    main()
