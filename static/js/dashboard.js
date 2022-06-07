function delConform(event) {
  let postTitle = event.target.getAttribute("posttitle");
  let postSno = event.target.getAttribute("postSno");
  document.getElementById("modalPostTitle").innerText = postTitle;
  document.getElementById("delPost").href = `/dashboard/delete/${postSno}`;
  const myModal = new bootstrap.Modal(
    document.getElementById("deleteConfomation")
  );
  myModal.show();
}

function editPost(event) {
  let postSno = event.target.getAttribute("postSno");
  let postImg = event.target.getAttribute("postImg");
  let postTitle = event.target.getAttribute("postTitle");
  let postTagline = event.target.getAttribute("postTagline");
  let postCato = event.target.getAttribute("postCato");
  let postContent = event.target.getAttribute("postContent");
  document.getElementById("editImg2").src = `static/img/blogs/${postImg}`;
  document.getElementById("editForm").action = `/dashboard/edit/${postSno}`;
  document.getElementById("postTitle").value = postTitle;
  document.getElementById("postTagline").value = postTagline;
  document.getElementById("postCato").value = postCato;
  document.getElementById("postContent").value = postContent;
  const myModal = new bootstrap.Modal(document.getElementById("editPost"));
  myModal.show();
}

function createPost() {
  const myModal = new bootstrap.Modal(document.getElementById("createPost"));
  myModal.show();
}

function setting() {
  const myModal = new bootstrap.Modal(document.getElementById("settingModal"));
  myModal.show();
}

function loadImg(event) {
  let showImg = document.getElementById("showimg");
  showImg.src = URL.createObjectURL(event.target.files[0]);
}

function galleryloadImg(event) {
  let showImg = document.getElementById("galleryShow");
  showImg.src = URL.createObjectURL(event.target.files[0]);
}

setInterval(setDropDown, 1);
function setDropDown() {
  if (screen.width > 500) {
    document.getElementById("nav-dropdown").classList.add("ms-auto");
  } else {
    document.getElementById("nav-dropdown").classList.remove("ms-auto");
  }
}



function addPhoto(){
  const myModal = new bootstrap.Modal(document.getElementById("addPhoto"));
  myModal.show();
}