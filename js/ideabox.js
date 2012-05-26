function edit_idea(idea_id){
  var idea=document.getElementById(idea_id);
  var idea_info=idea.getElementsByTagName("p");
  var idea_content=idea_info[0];
  var post_info=document.getElementById("post_info");
  post_info.innerHTML = "(edit post)"
  var post_text=document.getElementById("post_text");
  post_text.value=idea_content.innerHTML;
  var post_id=document.getElementById("post_id");
  post_id.value=idea_id;
}
function reply_idea(idea_id){
  var idea=document.getElementById(idea_id);
  var idea_info=idea.getElementsByTagName("p");
  var idea_content=idea_info[0];
  var post_info=document.getElementById("post_info");
  post_info.innerHTML = "reply to " + idea_info[1].innerHTML;
  var post_text=document.getElementById("post_text");
  post_text.value="> "+idea_content.innerHTML;
  var reply_id=document.getElementById("reply_id");
  reply_id.value=idea_id;
}
