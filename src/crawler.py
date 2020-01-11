#!/usr/bin/python
# -*- coding: big5 -*-

# first line is indicating python
# second line is indicating encoding
# hierachy of the variables: there are a lot of course in one page
 
import html2text
import requests
import re
import time
import json

# something like headers

requests.adapters.DEFAULT_RETRIES = 5 
s = requests.session()
s.keep_alive = False
 
# set parameters

prefix = 'http://nol.ntu.edu.tw/nol/coursesearch/'
num_course_in_one_page = 130  # how many courses in one page
current_sem = '108-2'  # which semster to crawl

# starts from first page

first_page_url = (prefix + 
                 ('search_result.php?alltime=yes&allproced=yes&cstype=1&csname=&current_sem=' + current_sem +
                  '&op=stu&'
                  'startrec=0'
                  '&week1=&week2=&week3=&week4=&week5=&week6=&'
                  'proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&'
                  'procedA=&procedB=&procedC=&procedD=&'
                  'allsel=yes&selCode1=&selCode2=&selCode3=&'
                  'page_cnt=') + str(num_course_in_one_page))

# url parameters explained
# startrec indicates the course id on the top of the page
# page_cnt indicates the number of courses in one page

# the course website is encoded through big5

response_first_page = requests.get( first_page_url )
response_first_page.encoding = 'big5'                 

# get the total number of courses

pattern_total_num_course = re.compile( ' <b>(.+)</b>' )
total_num_course = int(re.search(pattern_total_num_course, response_first_page.text).group()[4:-4])
print(total_num_course)

# pattern for each column in detail page

pattern_course_inform   = re.compile( '�ҵ{�W��\|(.*)�}�ҾǴ�\|' )
pattern_course_semster  = re.compile( '�}�ҾǴ�\|(.*)�½ҹ�H\|' )
pattern_course_student  = re.compile( '�½ҹ�H\|(.*)�½ұЮv\|' )
pattern_course_teacher  = re.compile( '�½ұЮv\|(.*)�Ҹ�\|' )
pattern_course_code     = re.compile( '�Ҹ�\|(.*)�ҵ{�ѧO�X\|' )
pattern_course_ID       = re.compile( '�ҵ{�ѧO�X\|(.*)�Z��\|' )
pattern_course_class    = re.compile( '�Z��\|(.*)�Ǥ�\|' )
pattern_course_credits  = re.compile( '�Ǥ�\|(.*)��/�b�~\|' )
pattern_course_year     = re.compile( '��/�b�~\|(.*)��/���\|' )
pattern_course_category = re.compile( '��/���\|(.*)�W�Үɶ�\|' )
pattern_course_time     = re.compile( '�W�Үɶ�\|(.*)�W�Ҧa�I\|' )
pattern_course_location = re.compile( '�W�Ҧa�I\|(.*)�Ƶ�\|' )
pattern_course_bonus    = re.compile( '�Ƶ�\|(.*)Ceiba �ҵ{����\|' )
pattern_course_ceiba    = re.compile( 'Ceiba �ҵ{����\|(.*)�ҵ{²���v��\|' )
pattern_course_no_ceiba = re.compile( '�Ƶ�\|(.*)�ҵ{²���v��\|' )            # for those no ceiba columns page
pattern_course_half     = re.compile( '�Ƶ�\|(.*)�ҵ{�j��\|' )                # for those page only have half page

# �e14�����O��"�ҵ{�W��","�}�ҾǴ�","�½ҹ�H","�½ұЮv","�Ҹ�","�ҵ{�ѧO�X","�Z��","�Ǥ�","���~/�b�~","����/���","�W�Үɶ�","�W�Ҧa�I","�Ƶ�","ceiba�ҵ{����"
# ��15����"�ҵ{�j��"�]syllabus�^�A�ҵ{�j���]�t�Ӻ������Ҧ���r���e
# ��16����"�ҵ{�j�����}"�]url�^
# �|����بҥ~�G�u���@�b(�����)�B�S��ceiba(���Ǥh�פ�U)

# pattern for clean teacher information that contains [] and url

pattern_clean_teacher = re.compile( '\[(.*)\]' )

# frame for saving information 

frame = []
course_number = 0

# pattern for info in search page

pattern_course_all        = re.compile( r'<tr (.+?)</td></tr>' ) # search for course information in outside search page
pattern_course_water_code = re.compile( r'align=\"center\"><TD>(.*?)</TD>' ) 
pattern_course_limit      = re.compile( r'<TD ALIGN="left" VALIGN="TOP">(.*?)</TD><TD ALIGN="left" VALIGN="TOP">' )
pattern_course_name       = re.compile( r'108-1&lang=CH">(.+?)</A>' ) 
pattern_courses           = re.compile( r'print_table(.+?)lang=CH' )  

# if there is no '?', re will search for longest string, which will lead to error in our case

start_time = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(start_time) # record start time

while course_number < total_num_course:
    
    page_url = (prefix + 
               ('search_result.php?alltime=yes&allproced=yes&cstype=1&csname=&current_sem=' + current_sem +
                '&op=stu&'
                'startrec=' + str(course_number) +
                '&week1=&week2=&week3=&week4=&week5=&week6=&'
                'proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&'
                'procedA=&procedB=&procedC=&procedD=&'
                'allsel=yes&selCode1=&selCode2=&selCode3=&'
                'page_cnt=' ) + str( num_course_in_one_page ) )

    page_response = requests.get( page_url )
    page_response.encoding = 'big5'
    
    courses_in_page          = pattern_courses.findall(page_response.text) # save all courses url in one search page as a list
    courses_water_code_list  = pattern_course_water_code.findall(page_response.text) # save all water code in one search page as a list
    courses_limit_list       = pattern_course_limit.findall(page_response.text) 
    courses_name_list        = pattern_course_name.findall(page_response.text)
    # courses_total_man_list   = pattern_total_man.findall(page_response.text)
    # courses_plus_method_list = pattern_plus_method.findall(page_response.text)      
    # courses_all_html_list      = pattern_course_all.findall(page_response.text)
    # courses_all_list         = [ html2text.html2text(i).split('|') for i in courses_all_html_list ]
     
    for course in range( len( courses_in_page ) ): # iterate over course as index in course_in_page list

        course_url         = prefix + 'print_table' + courses_in_page[course] + 'lang=CH'
        course_water_code  = courses_water_code_list[course]
        course_limit       = courses_limit_list[course]
        course_name        = courses_name_list[course]
        # course_total_man   = courses_all_list[course][13]
        # course_plus_method = courses_all_list[course + 1][11]
        
        print(course_name) # url
        # print(course_total_man)        
        # print(course_plus_method)
 
        course_response = requests.get(course_url)
        print(course_response.status_code)
        course_response.encoding = 'big5'
        
        raw_text = html2text.html2text(course_response.text)
        syllabus = re.sub('---', '', "".join(raw_text.split('\n')))
        # print(syllabus)

        teacher_full_info = re.search(pattern_course_teacher , syllabus).group().split('|')[1][:-2].strip()        
        
        course_dict = {}
        course_dict['�y����']         = course_water_code	
        course_dict['��ҭ������']   = course_limit
        course_dict['�ҵ{�W��']       = course_name
        #�@course_dict['�`�H��']         = course_total_man
        # course_dict['�[��覡']       = course_plus_method

#        course_dict['�ҵ{�W��']       = re.search(pattern_course_inform  , syllabus).group().split('|')[1].strip()
#        course_dict['�ҵ{�W��']       = re.sub(r'[a-zA-Z]', "", course_dict['�ҵ{�W��'])

        course_dict['�}�ҾǴ�']       = re.search(pattern_course_semster , syllabus).group().split('|')[1][:-4].strip()
        course_dict['�½ҹ�H']       = re.search(pattern_course_student , syllabus).group().split('|')[1][:-4].strip()
        course_dict['�½ҦѮv']       = re.search(pattern_clean_teacher  , teacher_full_info).group()[1:-1]
        course_dict['�Ҹ�']           = re.search(pattern_course_code    , syllabus).group().split('|')[1][:-5].strip()
        course_dict['�ҵ{�ѧO�X']     = re.search(pattern_course_ID      , syllabus).group().split('|')[1][:-2].strip()
        course_dict['�Z��']           = re.search(pattern_course_class   , syllabus).group().split('|')[1][:-2].strip()
        course_dict['�Ǥ�']           = re.search(pattern_course_credits , syllabus).group().split('|')[1][:-4].strip()
        course_dict['��/�b�~']        = re.search(pattern_course_year    , syllabus).group().split('|')[1][:-4].strip()
        course_dict['��/���']        = re.search(pattern_course_category, syllabus).group().split('|')[1][:-4].strip()
        course_dict['�W�Үɶ�']       = re.search(pattern_course_time    , syllabus).group().split('|')[1][:-4].strip()
        course_dict['�W�Ҧa�I']       = re.search(pattern_course_location, syllabus).group().split('|')[1][:-2].strip()
        course_dict['�ҵ{�j��']       = syllabus.strip()     
        course_dict['�ҵ{�j�����}']   = course_url
        
        # print(course_dict)
        
        try:
            course_dict['�Ƶ�']           = re.search(pattern_course_bonus   , syllabus).group().split('|')[1][:-10].strip()
            course_dict['Ceiba �ҵ{����'] = re.search(pattern_course_ceiba   , syllabus).group().split('|')[1][:-6].strip()

        except AttributeError:
            try:
                course_dict['�Ƶ�']           = re.search(pattern_course_half     , syllabus).group().split('|')[1][:-4].strip()
            except AttributeError:
                course_dict['�Ƶ�']           = re.search(pattern_course_no_ceiba , syllabus).group().split('|')[1].strip()    
                # �o�̧ڥR���F�ôb�A�쩳�O�n���n�[[:-n]
        # print(course_dict)
        
        frame.append(course_dict)
 
    print('page starts from course' + str(course_number) + ' is done!')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    course_number += num_course_in_one_page
    time.sleep(2)

print(start_time)

# save as json
final_file = 'original_course_data_' + current_sem + '.json'
with open(final_file, 'w') as fout:
    json.dump(frame, fout)    









