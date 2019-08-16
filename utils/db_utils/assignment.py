# -*- coding: utf-8 -*-
from pymongo import MongoClient


class MongodbClient(object):
    def __init__(self,mongodb_conf =None):
        self.mongodb_conf = mongodb_conf
        self.client = MongoClient(host=self.mongodb_conf['host'], port=self.mongodb_conf['port'])
        self.db = self.client[self.mongodb_conf['db_name']]
        self.books = self.db[self.mongodb_conf['table_names'][0]]
        self.users = self.db[self.mongodb_conf['table_names'][1]]
        self.checkouts = self.db[self.mongodb_conf['table_names'][2]]

    def insert_users(self,data):

        return self.users.insert(data)

    def insert_books(self ,data):

        self.books.insert(data)

    def insert_checkouts(self ,data):

        self.checkouts.insert(data)

    def find_books_checked(self,input_time):

        result = self.checkouts.find({"checked_out_date": {"$gte": input_time}}, {"book_name": 1, "_id": 0})
        return result

    def find_users_by_checked_bookname(self,bookname):

        result = self.checkouts.find({"book_name": {"$gte": bookname}},{"user_name": 1, "_id": 0})
        return result

    def find_books_count_by_topic(self,topic):

        result = self.books.find({'topic': {"$in":[topic]}}).count()
        return result

    def find_users_by_date_topic_and_university_affiliation(self,topic,university_affiliation,start_date,end_date):

        result = self.checkouts.find({'topic': {"$in":[topic]},"university_affiliation": university_affiliation,
                                      "checked_out_date": {"$gte": start_date,"$lte": end_date}},
                                     {"user_name": 1, "_id": 0})
        return result

    def find_comments_by_date_bookname_and_username(self, user_name, book_name, start_date, end_date):
        result = self.checkouts.find({'user_name': user_name, "book_name": book_name,
                                      "checked_out_date": {"$gte": start_date, "$lte": end_date}},
                                     {"comments": 1, "_id": 0})
        return result

    def find_comments_by_bookname_and_username(self, user_name, book_name):

        result = self.checkouts.find({'user_name': user_name, "book_name": book_name},
                                     {"comments": 1, "_id": 0})
        return result


if __name__ == "__main__":

    db = MongodbClient(mongodb_conf ={'host': '101.132.113.50', 'port': 27017, 'db_name': 'ebook', 'table_names': ['books','users','checkouts']})

    books = [
            {"book_id": 1, "title": "Wuthering Heights", "primary_author": "Emily Bronte", "date_of_first_publication": "1847-01-01", "number_of_pages": 500, "publisher": "The Floating Press", "topic": ["fiction"], "checked_out_by": [101,102,103]},
            {"book_id": 2, "title": "The Story of the Stone", "primary_author": "Cao Xueqin", "date_of_first_publication": "1791-01-01", "number_of_pages": 600, "publisher": "Penguin Books Ltd", "translator": "David Hawkes", "topic": ["fiction"], "checked_out_by": [102,103,104]},
            {"book_id": 3, "title": "Intro to Machine Learning", "primary_author": "Alison Dilarentuas", "secondary_authors": "Jonny Fields", "date_of_first_publication": "2012-01-01", "number_of_pages": 700, "publisher": "Modern Publication", "topic": ["machine learning"], "checked_out_by": [102,105]},
            {"book_id": 4, "title": "Business Model Generation", "primary_author": "Alexander Osterwalder", "secondary_authors": "Yves Pigneur", "date_of_first_publication": "2010-01-01", "number_of_pages": 800, "publisher": "Wiley", "topic": ["business", "management"], "checked_out_by": [105]}]

    users = [
            {"user_id": 101, "name": "Amy", "phone": 1234567891, "address": "1 W 1 St", "university_affiliation": "Columbia University", "checked_book": [1]},
            {"user_id": 102, "name": "Ben", "phone": 1234567892, "address": "2 W 2 St", "university_affiliation": "Columbia University", "checked_book": [1,2,3]},
            {"user_id": 103, "name": "Cindy", "phone": 1234567893, "address": "3 W 3 St", "university_affiliation": "Columbia University", "checked_book": [1,2]},
            {"user_id": 104, "name": "Dan", "phone": 1234567894, "address": "4 W 4 St", "university_affiliation": "New York University", "checked_book": [2]},
            {"user_id": 105, "name": "Eric", "phone": 1234567895, "address": "5 W 5 St", "checked_book": [3,4]}]


    checkouts = [
            {"id": 201, "user_id": 101, "user_name": "Amy", "university_affiliation": "Columbia University", "book_id": 1, "book_name": "Wuthering Heights", "topic": ["fiction"], "checked_out_date": "2019-01-01","comments":"A MUST READ for any book lovers."},
            {"id": 202, "user_id": 102, "user_name": "Ben", "university_affiliation": "Columbia University", "book_id": 1, "book_name": "Wuthering Heights", "topic": ["fiction"], "checked_out_date": "2019-02-02","comments":"A MUST READ for any book lovers."},
            {"id": 203, "user_id": 102, "user_name": "Ben", "university_affiliation": "Columbia University", "book_id": 2, "book_name": "The Story of the Stone", "topic": ["fiction"], "checked_out_date": "2019-02-02","comments":"My second book by this author. Highly recommend. I can't wait for the next book."},
            {"id": 204, "user_id": 102, "user_name": "Ben", "university_affiliation": "Columbia University", "book_id": 3, "book_name": "Intro to Machine Learning", "topic": ["machine learning"], "checked_out_date": "2019-02-02","comments":"Overall, it was a fantastic book and I highly recommend it."},

            {"id": 205, "user_id": 103, "user_name": "Cindy", "university_affiliation": "Columbia University", "book_id": 1, "book_name": "Wuthering Heights", "topic": ["fiction"], "checked_out_date": "2019-03-03","comments":"My second book by this author. Highly recommend. I can't wait for the next book."},
            {"id": 206, "user_id": 103, "user_name": "Cindy", "university_affiliation": "Columbia University", "book_id": 2, "book_name": "The Story of the Stone", "topic": ["fiction"], "checked_out_date": "2019-03-03","comments":" I am very picky as to which I like, and am harder on them rating wise then other genres. But this, this was incredible, you really never knew where the next page was going to take you."},
            {"id": 207, "user_id": 104, "user_name": "Dan", "university_affiliation": "New York University", "book_id": 2, "book_name": "The Story of the Stone", "topic": ["fiction"], "checked_out_date": "2019-03-04","comments":"Overall, it was a fantastic book and I highly recommend it."},
            {"id": 208, "user_id": 105, "user_name": "Eric", "book_id": 3, "book_name": "Intro to Machine Learning", "topic": ["machine learning"], "checked_out_date": "2019-03-05","comments":"In so many ways. I made myself finish it."},
            {"id": 209, "user_id": 105, "user_name": "Eric", "book_id": 4, "book_name": "Business Model Generation", "topic": ["business", "management"], "checked_out_date": "2019-03-05","comments":"My second book by this author. Highly recommend. I can't wait for the next book."}
            ]
    # db.insert_users(users)
    # db.insert_books(books)
    # db.insert_checkouts(checkouts)

    print("Question 1 ,Which books have been checked out since such and such date?")
    input_time = "2019-02-28"
    for item in db.find_books_checked(input_time):
        print(item)
    print()


    print("Question 2 ,Which users have checked out such and such book?")
    book_name = "Wuthering Heights"
    for item in db.find_users_by_checked_bookname(book_name):
        print(item)
    print()


    print("Question 3 ,How many books does the library have on such and such topic?")
    topic = "fiction"
    result = db.find_books_count_by_topic(topic)
    print(result)
    print()

    print("Question 4 .Which users from Columbia University have checked out books on Machine Learning between this date and that date.")
    start_date = "2000-01-01"
    end_date = "2019-04-04"
    university_affiliation = "Columbia University"
    topic = "machine learning"
    for item in db.find_users_by_date_topic_and_university_affiliation(topic,university_affiliation,start_date,end_date):
        print(item)
    print()

    print("Question 5 What comments have been made by any User about such and such book between such and such dates, ordered from the most recent to the least recent.")
    start_date = "2000-01-01"
    end_date = "2019-04-04"
    user_name = "Amy"
    book_name = "Wuthering Heights"
    for item in db.find_comments_by_date_bookname_and_username(user_name, book_name, start_date, end_date):
        print(item)
    print()

    print("Question 6 Show for a given User, what comments they have made about such and such book.")
    user_name = "Ben"
    book_name = "Intro to Machine Learning"
    for item in db.find_comments_by_bookname_and_username(user_name,book_name):
        print(item)


