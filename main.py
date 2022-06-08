import multiprocessing
import os

from Parser import parse_today
from Extractor import extract_data, get_all_words
from Analyzer import show_MNK
from BarAnalyzer import show_BarGraph
from Creator import create_excel, create_txt
from Cleaner import clean_excel, clean_txt


file_news = 'news.txt'
file_stat = 'stat.xlsx'
# word = 'україні'
# word_count = 50


def parse():
    parse_today(file_news)


def open_news():
    os.startfile(file_news)


def extract():
    return extract_data(file_news, file_stat)


def get_data():
    return get_all_words(file_stat)


def open_stat():
    os.startfile(file_stat)


def analyze(word):
    return show_MNK(file_stat, word)


def bar_analyze(word_count):
    return show_BarGraph(file_stat, word_count)


def create():
    create_txt(file_news)
    create_excel(file_stat)


def clean():
    clean_excel(file_stat)
    clean_txt(file_news)


process = multiprocessing.Process(target=parse)

