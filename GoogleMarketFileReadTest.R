# install.packages('readr')
# 설명에 특수문자가 많아 readr 패키지가 필요로 합니다
library(readr)
library(KoNLP)
library(wordcloud)
library(RColorBrewer)
library(tm)
topGrossing = read_tsv(file="raw/topGrossing_20160613.tsv")
topPaid = read_tsv(file="raw/topPaid_20160613.tsv")
topFree = read_tsv(file="raw/topFree_20160613.tsv")

# 장르
sort(table(topGrossing$category), decreasing = T)
sort(table(topPaid$category), decreasing = T)
sort(table(topFree$category), decreasing = T)

#write.table(sort(table(topPaid$category), decreasing = T), file = "clipboard", sep = ",", quote = F, row.names = F)
# 다운로드
sort(table(topPaid$download), decreasing = T)

# WORD CLOUD 그려보기
useSejongDic()
NOUNS = unlist(sapply(topGrossing$description, extractNoun, USE.NAMES = F))
NOUNS.REAL = Filter(function(x){ nchar(x) > 1 }, NOUNS)
NOUNS.REAL = unlist(sapply(NOUNS.REAL, extractNoun, USE.NAMES = F))
wordcloud(rownames(table(NOUNS.REAL)), table(NOUNS.REAL), scale=c(4, 2), max.words = 20, random.order = F, colors = brewer.pal(8, "Dark2"), family=windowsFont("맑은고딕"))
table(NOUNS.REAL)

t = Corpus(VectorSource(topGrossing$description))
t = tm_map(t, removeNumbers)
t = tm_map(t, removePunctuation)
t = tm_map(t, extractNoun)
tdm <- TermDocumentMatrix(t)
tdm.non_sparse = removeSparseTerms(tdm, 0.99)



toClipboard <- function(object) {
  write.table(object, file = "clipboard", sep = ",", quote = F, row.names = T)
}

toClipboard(findAssocs(tdm, terms = "rpg", corlimit = 0.4))
