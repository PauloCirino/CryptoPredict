import argparse
import itertools
import os
import twitterscraper
import datetime
import time

def main(hashtag_array, language_array, output_folder, verbose, init_year):

    comb_list = list(itertools.product(language_array, hashtag_array))

    for iter_arg in comb_list :
        (language, hashtag) = iter_arg

        if verbose:
            print('Hashtag =', hashtag, 'Lang =', language,
                  'at', time.strftime('%X %x') )

        if verbose:
            print('Quering', hashtag, ' in ', language, 'language at', datetime.datetime.now())

        saving_path = os.path.join(output_folder, '/'.join(iter_arg))
        if not os.path.exists(saving_path) :
            if verbose :
                print('Creating path ', str(saving_path))
            os.makedirs(saving_path)

        saving_path = os.path.join(saving_path, 'main.csv')

        init_date = datetime.date(init_year, 1, 1)
        end_date = datetime.date.today()
            
        if verbose :
            print('Initializing query ', str(saving_path),
                  ' at', time.strftime('%X %x') )

        querry_result = twitterscraper.query_tweets(query = hashtag, 
                                                    begindate = init_date, 
                                                    enddate = end_date,
                                                    limit = None,
                                                    lang = language)

            
        if verbose :
            print('Saving tweets to file', str(saving_path), 
                  'at', time.strftime('%X %x') )

        with open(saving_path, 'w') as file:
            header_list = ['timestamp', 'full_name', 'ID', 'url',
                           'user', 'html', 'text', 'likes', 'replies'] 
            file.write('\t'.join(header_list) + '\n')

            for item in querry_result :
                timestamp = item.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                full_name = item.fullname
                ID = item.id
                url = item.url
                user = item.user
                html = item.html
                text = item.text
                likes = item.likes
                replies = item.replies
                retweets = item.retweets

                items_list = [timestamp, full_name, ID, url, user, html, text, likes, replies, retweets]
                file.write('\t'.join(items_list) + '\n')

        print('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--hashTagsFile", required = True, 
                        help = "File that includes all hashtags to be scraped")

    parser.add_argument("--languageFile", required = True,
                        help = "File that includes all languages in which twitters will be scraped")

    parser.add_argument("--outputFolder", required = True,
                        help = "Folder in which all Scraped Twitters will be saved")

    parser.add_argument("--initYear", default = 2010, required = False, type = int,
                        help = "Print Scraped Twitters")

    parser.add_argument("--verbose", default = False, required = False, action = "store_true",
                        help = "Print Scraped Twitters")

    args = parser.parse_args()

    hashtag_array = []
    with open(args.hashTagsFile, "r") as file:
        for line in file:
            hashtag_array.append(line.strip('\n').lower())
    hashtag_array = list( set(hashtag_array) ) ## Removes Duplicates Hashtags

    language_array = []
    with open(args.languageFile, "r") as file:
        for line in file:
            language_array.append(line.strip('\n').lower())
    language_array = list( set(language_array) )

    main(hashtag_array  = hashtag_array, 
         language_array = language_array,
         output_folder  = args.outputFolder,
         verbose        = args.verbose,
         init_year = args.initYear)
