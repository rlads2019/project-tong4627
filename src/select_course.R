rm(list=ls())

library(tidyverse)
library(jsonlite)

## 先設定 working directory 在 source file location

## 讀取原檔
my_course <- fromJSON("original_course_data_108-1.json")
head(my_course)
df_course <- as.tibble(my_course)

## 整理資料
course_no_need <- "健康體適能|全民國防教育軍事訓練課程|進階英語|高階英語|服務學習|專題討論一"

new_df_course <- df_course %>%
  filter(!授課對象=="體育室") %>%                     # to delete all PE class
  select(流水號, 課程名稱, 授課老師, 課程大綱) %>%    # select 4 colomns
  filter(授課老師 != "") %>%                          # to delete the class dont have teacher
  filter(!str_detect(.$課程名稱, course_no_need))     # some class we dont need

## 寫入檔案
#write_csv(new_df_course, path="selected_course_data_108-1.csv")

## 由於檔案太大電腦爆了，所以先隨機選100筆課程以利測試
set.seed(1288)
#partial_100_course_data <- sample_n(new_df_course, 100)
partial_1000_course_data <- sample_n(new_df_course, 1000)
write_csv(partial_1000_course_data, path="partial_1000_course_data.csv")

## 讀入檔案
#data <- read_csv("selected_course_data_108-1.csv")
#partial_data <- read_csv("partial_100_course_data.csv")
