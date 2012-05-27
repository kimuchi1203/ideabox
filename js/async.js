var xmlHttp;

function loadText(){
  xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = checkStatus;
  xmlHttp.open("GET", "/idealist", true);

  xmlHttp.send(null);
}

function checkStatus(){
  if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
    showIdeaList(eval('('+xmlHttp.responseText+')'));
    //alert(xmlHttp.responseText);
  }
}

function showIdeaList(responseData){
  idlist = responseData[0];
  user_name = idlist[0].user_name;
  for(i=1;i<responseData.length;++i){
    showIdea(user_name, idlist[i], responseData[i]);
  }
}

function showIdea(user_name, id, idea){
  var e_idea = document.createElement("div");
  e_idea.setAttribute("class", "idea");
  e_idea.id = id.id;
  var e_content = document.createElement("p");
  e_content.setAttribute("class", "idea_content");
  if(!idea.delete_flag){
	  e_content.innerHTML = idea.content;
	  e_idea.appendChild(e_content);
	  var e_author = document.createElement("p");
	  e_author.setAttribute("class", "author");
		if(idea.author){
	  	e_author.innerHTML = idea.author.nickname;
		}else{
			e_author.innerHTML = "None";
		}
	  e_idea.appendChild(e_author);
	  var e_date = document.createElement("p");
	  e_date.setAttribute("class", "date");
	  e_date.innerHTML = idea.date.ctime;
	  e_idea.appendChild(e_date);
    var e_btndiv = document.createElement("div");
		if(idea.parent_id){
			var e_reply = document.createElement("a");
			e_reply.setAttribute("name", "idea_info");
			e_reply.setAttribute("href", "#"+idea.parent_id);
    	e_reply.innerHTML = "reply to " + idea.parent_id;
    	e_btndiv.appendChild(e_reply);
    }
    var e_form = document.createElement("form");
    e_form.setAttribute("action", "/ideadelete");
    e_form.setAttribute("class", "idea_btn");
    e_form.setAttribute("method", "post");
		var e_btn_rep = document.createElement("input");
		e_btn_rep.setAttribute("type", "button");
		e_btn_rep.setAttribute("class", "btn-mini");
		e_btn_rep.setAttribute("value", "reply");
		e_btn_rep.setAttribute("onclick", "reply_idea("+id.id+")");
		e_form.appendChild(e_btn_rep);
		var e_hid_id = document.createElement("input");
		e_hid_id.setAttribute("type", "hidden");
		e_hid_id.setAttribute("name", "idea_id");
		e_hid_id.setAttribute("value", id.id);
		e_form.appendChild(e_hid_id);
		if((idea.author)&&(idea.author.nickname==user_name)){
      var e_sub_del = document.createElement("input");
			e_sub_del.setAttribute("type", "submit");
			e_sub_del.setAttribute("class", "btn-mini");
			e_sub_del.setAttribute("value", "delete");
			e_form.appendChild(e_sub_del);
			var e_btn_edit = document.createElement("input");
			e_btn_edit.setAttribute("type", "button");
			e_btn_edit.setAttribute("class", "btn-mini");
			e_btn_edit.setAttribute("value", "edit");
			e_btn_edit.setAttribute("onclick", "edit_idea("+id.id+")");
      e_form.appendChild(e_btn_edit);
		}
		e_btndiv.appendChild(e_form);
    e_idea.appendChild(e_btndiv);
  }else{
    e_content.innerHTML = "(deleted)";
    e_idea.appendChild(e_content);
  }
  var idea_list = document.getElementById("idea_list");
  idea_list.appendChild(e_idea);
}
