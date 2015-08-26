$(document).ready(function(){
  console.info("ready")

  $.ajax({
    dataType: "json",
    url: "./data/images.json",
    success: decoratePage
  });
});


function decoratePage(images){
  console.info("whatup")
  var $body     = $("body"),
      $content  = $('<div id="content" class="container">'),
      $imagerow = $('<div id="images" class="row">');
  $content.append($imagerow)
  $body.append($content);
  $content.append("<h1>Images</h1>")
  $content.append("<h5>" + images.length + " found</h5>")
  console.log(images.length)
  // now add images
  for(var i = 0, lth = images.length; i < lth; i++){
    console.log(i)
    var image = images[i];
    var page_url  = image.link,
        img_url   = image.images.thumbnail.url;

    var $col  = $('<div class="col-sm-4"></div>'),
        $a    = $('<a href="' + page_url + '"></a>'),
        $img  = $('<img src="' + img_url +'">');

    $a.append($img);
    $col.append($a);
    $imagerow.append($col);
    console.info(image['id'])
  }
}
