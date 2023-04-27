library(tidyverse)
journal <- read_csv('../data/journals.csv')
View(journal)
journal2 <- journal %>%
  head(500) %>%
  #mutate(text=str_replace_all(text_only_transcript,"\\[.*\\]{1,2}",''),
         #text=str_replace_all(text,'\\^','')) %>%
  mutate(pieces = str_split(text_only_transcript,'\\.|\\r')) %>%
  select(c(internal_id,pieces)) %>%
  unnest() %>%
  filter(!str_detect(pieces, "\\[|\\]|\\{")) %>%
  filter(pieces != '') %>%
  #get dates
  #mutate(finddates = str_extract('[JFMASOND].*\\s\\d{1,2},?\\s')) %>%
  filter(!str_detect(pieces,'\\d|\\n')) %>%
  mutate(pieces = tolower(str_replace(pieces,'\\&amp\\;','and'))) %>%
  filter(str_length(pieces)>4)

write.csv(journal2,'first500.csv')

only_period <- journal %>%
  head(100) %>%
  #mutate(text=str_replace_all(text_only_transcript,"\\[.*\\]{1,2}",''),
  #text=str_replace_all(text,'\\^','')) %>%
  mutate(pieces = str_split(text_only_transcript,'\\.')) %>%
  select(c(internal_id,pieces)) %>%
  unnest() %>%
  #(!str_detect(pieces, "\\[|\\]|\\{")) %>%
  filter(pieces != '') %>%
  #get dates
  #mutate(finddates = str_extract('[JFMASOND].*\\s\\d{1,2},?\\s')) %>%
  filter(!str_detect(pieces,'\\d')) %>% #questionable
  mutate(pieces = tolower(str_replace(pieces,'\\&amp\\;','and')))

check <- journal2 %>%
  filter(internal_id==11809)
