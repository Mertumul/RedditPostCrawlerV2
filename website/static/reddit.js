document.addEventListener("DOMContentLoaded", function() {
    let redditPost = {
      title: [],
      author: [],
      score: [],
      url: []
    };
  
    fetch('http://127.0.0.1:8001/redditCheck')
      .then(response => response.json())
      .then(data => {
        for (let i = 0; i < data.length; i++) {
          redditPost.title.push(data[i].title);
          redditPost.author.push(data[i].author);
          redditPost.score.push(data[i].score);
          redditPost.url.push(data[i].url);
        }
  
        for (let i = 0; i < redditPost.title.length; i++) {
          var titElement = document.getElementById("reddit-element-" + (i + 1));
          var authElement = document.getElementById("auth-element-" + (i + 1));
          var detailElement = document.getElementById("detail-element-" + (i + 1));
          var readmoreElement = document.getElementById("readmore-element-" + (i + 1));
  
          titElement.innerHTML = redditPost.author[i];
          authElement.innerHTML = redditPost.title[i];
          detailElement.innerHTML = redditPost.score[i];
          readmoreElement.href=redditPost.url[i];

        }
      })
      .catch(error => {
        console.log('API ile veri alınamadı:', error);
      });
  });