library(Rfacebook)
myAuth <- fbOAuth(app_id = "119980435291125", app_secret = "144e0f46eb76ac16ae5884ea5a8e2b04")
save(myAuth, file = "myAuth")

getpagedata <- getPage(367963843082, token = myAuth, since = "2017-01-01", feed = TRUE, reactions = TRUE)

getcommentdata <- getPost(post = getpagedata$id[1], myAuth, n = 1000) 
for (i in 1:25){
  getcommentdata2 <- rbind(getcommentdata, getPost(post = getpagedata$id[i], myAuth, n = 1000))
}