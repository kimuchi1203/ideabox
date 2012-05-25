function edit_idea(idea_id){
  var idea=document.getElementById(idea_id);
  var idea_content=idea.getElementsByTagName("p")[0];
  var post_text=document.getElementById("post_text");
  post_text.value=idea_content.innerHTML;
  var post_id=document.getElementById("post_id");
  post_id.value=idea_id;
}
