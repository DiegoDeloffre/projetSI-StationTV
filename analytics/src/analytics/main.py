import os
from datetime import date, timedelta, datetime, time

import numpy as np
import matplotlib.pyplot as plt


class Analytics:
    """
        Constructor for the Analytics class

        Parameters:
            data (list): List of data for each recording
            keywords (list): List of keywords for each recording
            metadata (list): List of metadata for each recording
    """
    def __init__(self, data, keywords, metadata):
        self.data = data
        self.keywords = keywords
        self.metadata = metadata
        self._pre_process()

    """
        Returns the path without the file
        So the audio file and the XML file have the same path

        Parameters:
            path (str): The path of the file

        Returns:
            str: The path without the file
    """
    def _normalize_path(self, path):
        return os.sep.join(os.path.normpath(path).split(os.sep)[:-1])

    """
        Pre-processes the data and metadata by creating dictionaries with a normalised path as the key
    """
    def _pre_process(self):
        # Creates dicts with normalised path as key
        self.metadata_per_file = {}
        for emission in self.metadata:
            file_path = self._normalize_path(emission['file'])

            self.metadata_per_file[file_path] = emission

        self.data_per_file = {}
        for emission in self.data:
            self.data_per_file[self._normalize_path(emission['file'])] = emission

    """
        Returns the channel of the emission

        Parameters:
            emission (dict): The emission data

        Returns:
            str: The channel of the emission
    """
    def _get_channel(self, emission):
        if "programme" not in emission or "@channel" not in emission["programme"]: return None
        return emission["programme"]["@channel"]

    """
        Returns the list of recorded channels

        Returns:
            list: The list of recorded channels
    """
    def get_channels(self):
        channels = set()
        for emission in self.metadata:
            channels.add(self._get_channel(emission))

        if None in channels: channels.remove(None)
        return channels

    """
        Returns the category of the emission

        Parameters:
            emission (dict): The emission data

        Returns:
            str: The category of the emission
    """
    def _get_category(self, emission):
        if "programme" not in emission or "category" not in emission["programme"] or "#text" not in \
                emission["programme"]["category"]: return None
        return emission["programme"]["category"]["#text"]

    """
        Returns the list of recorded categories

        Returns:
            list: The list of recorded categories
    """
    def get_categories(self):
        categories = set()
        for emission in self.metadata:
            categories.add(self._get_category(emission))

        if None in categories: categories.remove(None)
        return categories

    """
        Returns a date object from string

        Parameters:
            datestamp (str): The string representation of a date

        Returns:
            date: The date object corresponding to the input string
    """
    def _get_date_from_datestamp(self, datestamp):
        return date(int(str(datestamp)[0:4]), int(str(datestamp)[4:6]), int(str(datestamp)[6:8]))

    """
        Returns a list of all days between two dates

        Parameters:
            start_date (date): The starting date
            end_date (date): The end date

        Returns:
            list: List of dates between start_date and end_date
        """
    def _get_date_range(self, start_date, end_date):
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)
        return date_range

    """
        Returns a list of recorded days

        Returns:
            list: List of recorded days
    """
    def get_days(self):

        first_day = 999999999
        last_day = 0

        for emission in self.data:
            file_date = self._get_datestamp_from_file(emission["file"])

            if file_date <= first_day: first_day = file_date
            if file_date >= last_day: last_day = file_date

        start_date = self._get_date_from_datestamp(first_day)
        end_date = self._get_date_from_datestamp(last_day)

        return self._get_date_range(start_date, end_date)

    """
        Returns a list of days and a dictionary of keyword occurences for each day. The list of days and the list of
        dictionaries have the same length, days[i] is the dictionary of occurences for the date in timeline[i].

        Parameters:
            top_n_keywords (int, optional): The number of top keywords to analyze. Defaults to None.
            keywords (list, optional): The list of keywords to analyze. Defaults to None.

        Returns:
            list, list: A list of dates and a list of dictionaries of keyword occurences for each date.
    """
    def analyse_keywords_per_day(self, top_n_keywords=None, keywords=None):

        if keywords is None:
            keywords = self.keywords

        if top_n_keywords is not None:
            if top_n_keywords < len(keywords):
                keywords = keywords[:top_n_keywords]

        timeline = self.get_days()
        days = [{} for i in range(len(timeline))]
        for day in days:
            for keyword in keywords:
                day[keyword] = 0

        for emission in self.data :
            file_date = self._get_date_from_datestamp(self._get_datestamp_from_file(emission['file']))
            index_in_days = timeline.index(file_date)
            for keyword in keywords :
                days[index_in_days][keyword] += emission['keywords'][keyword]

        return timeline, days

    """
        Returns hour from file path.
    """
    def _get_hourstamp_from_file(self, file_path):

        # Normalize the file path and split it by the file separator.
        file_path = os.path.normpath(file_path).split(os.sep)
        # Return the second part of the second-last element in the split file path.
        return file_path[-2].split('_')[1]

    """
        Returns time object from string.
    """
    def _get_date_from_hourstamp(self, hourstamp):

        # Extract the first two characters of the hourstamp as the hour,
        # and the next two characters as the minute.
        # Create a time object with the hour and minute.
        return time(int(str(hourstamp)[0:2]), int(str(hourstamp)[2:4]))

    """
        Returns a list of all minutes in a day.
   """
    def _get_time_range(self):
        time_range = []
        # Create a datetime object for the current time, with the date set to today
        # and the time set to the minimum time possible.
        current_time = datetime.combine(datetime.today(), time.min)
        # Iterate through all the times in a day.
        while current_time <= datetime.combine(datetime.today(), time.max):
            # Append the time part of the datetime object to the list of times.
            time_range.append(current_time.time())
            # Increment the current time by one minute.
            current_time += timedelta(minutes=1)
        return time_range

    """
        Returns the list of all minutes in a day.
    """
    def get_hours(self):
        return self._get_time_range()

    """
        This function returns two lists of equal length, `timeline` and `result`.
        `timeline[i]` represents the time of day and `result[i]` is a dictionary of occurences for each keyword for that time.
    """
    def analyse_keywords_per_hour(self, top_n_keywords=None, keywords=None):
        # Setting keywords to use for analysis
        if keywords is None:
            keywords = self.keywords

        # Truncating the keywords list to the top N if specified
        if top_n_keywords is not None:
            if top_n_keywords < len(keywords):
                keywords = keywords[:top_n_keywords]

        # Getting the hours to use as the timeline
        timeline = self.get_hours()
        # Initializing a dictionary of keyword occurences for each hour
        result = [{keyword: 0 for keyword in keywords} for _ in range(len(timeline))]

        # Looping through the data to count the occurences of each keyword for each hour
        for emission in self.data:
            # Getting the hour from the emission's file
            file_date = self._get_date_from_hourstamp(self._get_hourstamp_from_file(emission['file']))
            # Finding the index of the hour in the timeline
            index_in_days = timeline.index(file_date)
            # Incrementing the count of each keyword for that hour
            for keyword in keywords:
                result[index_in_days][keyword] += emission['keywords'][keyword]

        return timeline, result

    """
        This function returns a list of channels and a list of dictionaries of keyword occurences for each channel recorded.
        Both lists have the same length, result[i] is the dict of occurences for the channel in channels[i].
    """
    def analyse_keywords_per_channel(self, top_n_keywords=None, keywords=None):

        # Use all keywords if none are specified
        if keywords is None:
            keywords = self.keywords

        # Truncate the keyword list if the specified number of keywords is less than the total number of keywords
        if top_n_keywords is not None:
            if top_n_keywords < len(keywords):
                keywords = keywords[:top_n_keywords]

        # Get the list of channels recorded
        channels = self.get_channels()
        results = [{} for i in range(len(channels))]
        # Initialize the dict of keyword occurences to 0 for each channel
        for result in results:
            for keyword in keywords:
                result[keyword] = 0

        # Iterate through the data and count the occurences of keywords in each channel
        for emission in self.data:
            file_channel = self._get_channel(self.metadata_per_file[self._normalize_path(emission['file'])])
            if file_channel is not None:
                index_in_channels = list(channels).index(file_channel)
                for keyword in keywords:
                    if keyword in emission['keywords']:
                        results[index_in_channels][keyword] += emission['keywords'][keyword]

        return list(channels), results

    """
        Returns a list of categories and a list of dictionaries containing keyword occurences for each category.
        Both lists have the same length, result[i] is the dictionary of occurences for the category in categories[i].
    """
    def analyse_keywords_per_category(self, top_n_keywords=None, keywords=None):

        # If keywords argument is not provided, use the default keywords stored in self.keywords
        if keywords is None:
            keywords = self.keywords

        # If top_n_keywords argument is provided, only use the specified number of keywords if it's smaller than the length of keywords
        if top_n_keywords is not None:
            if top_n_keywords < len(keywords):
                keywords = keywords[:top_n_keywords]

        # Get the list of categories recorded
        categories = self.get_categories()

        # Create a list of dictionaries to store keyword occurences for each category
        results = [{} for i in range(len(categories))]

        # Initialize keyword occurences to 0 for each category
        for result in results:
            for keyword in keywords:
                result[keyword] = 0

        # Loop through each emission in self.data
        for emission in self.data:
            # Get the category of the emission
            file_category = self._get_category(self.metadata_per_file[self._normalize_path(emission['file'])])

            # If the category is not None, update keyword occurences for the category
            if file_category is not None:
                # Get the index of the category in the list of categories
                index_in_categories = list(categories).index(file_category)

                # Update keyword occurences for the category
                for keyword in keywords:
                    if keyword in emission['keywords']:
                        results[index_in_categories][keyword] += emission['keywords'][keyword]

        # Return the list of categories and the list of keyword occurences for each category
        return list(categories), results

    """
        This function displays a bar graph with the given data.
        categories: list of categories to be plotted on x-axis
        data: list of dictionaries, where each dictionary represents data of one category
    """
    def display_graph(self, categories, data):
        if len(data) == 0:
            return

        keywords = data[0].keys()

        # Parsing data to create a list of lists with all keywords in the same order
        data_to_display = []
        for keyword in keywords:
            current_category = []
            for element in data:
                current_category.append(element[keyword])
            data_to_display.append(current_category)

        # Calculate the width and placement of the bars in the bar graph
        bar_width = 1 / len(keywords)
        bars = []
        for i in range(len(data_to_display)):
            if i == 0:
                bars.append(np.arange(len(data_to_display[0])))
            else:
                bars.append([x + bar_width for x in bars[i - 1]])

        for bar, element, label in zip(bars, data_to_display, keywords):
            # Plot all bars
            plt.bar(bar, element, width=bar_width, label=label)

        # Add labels and ticks to the graph
        plt.xlabel("Category", fontweight="bold", fontsize=15)
        plt.ylabel("Occurrences", fontweight="bold", fontsize=15)
        plt.xticks([r + bar_width for r in range(len(data_to_display[0]))], categories, rotation=90)

        # Add legend
        plt.legend()

        # Show the graph
        plt.show()

