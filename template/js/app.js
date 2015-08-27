$(document).ready(function(){
  console.info("ready")

  $.ajax({
    dataType: "json",
    url: "./data/images.json",
    success: decoratePage
  });
});


function decoratePage(images){
  insertImages(images);
  doIsotope();
}

function insertImages(images){
  console.info("whatup")
  var $body     = $("body"),
      $content  = $('<div id="content" class="container"></div>'),
      $imagerow = $('<div id="images"></div>');
  $content.append("<h1>Images</h1>")
  $content.append("<h5>" + images.length + " found</h5>")
  $content.append($imagerow)
  $body.append($content);
  console.log(images.length)
  // now add images
  for(var i = 0, lth = images.length; i < lth; i++){
    var image = images[i];
    var page_url  = image.link,
        img_url   = image.images.thumbnail.url,
        likes_count = image.likes['count'];

    var $idiv  = $('<div class="image" data-likes-count="' +
                    likes_count + '"></div>'),
        $a    = $('<a target="_instagram" href="' + page_url + '"></a>'),
        $img  = $('<img src="' + img_url +'">');

    $a.append($img);
    $idiv.append($a);
    $imagerow.append($idiv);
  }
}

function doIsotope(){
  var $grid_el = $("#images")
  console.info("in doIsotope")
  $grid_el.isotope({
    itemSelector: '.image',
    layoutMode: 'fitRows'
  });
}


function filterIsotope(){
    var number = $(this).data('likes-count');
    return parseInt( number) > 100;
}


$(document).ready(function(){
  $("#filter-button").click(function(){
    var $grid_el = $("#images");
    console.info("filter button clicked")
    $grid_el.isotope({
      filter: filterIsotope
    });
  })
});
