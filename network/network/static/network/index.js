document.addEventListener("DOMContentLoaded", function () {
  // resizing text area
  document.querySelectorAll("textarea").forEach((textarea) => {
    const heightLimit = textarea.style.height;
    textarea.onkeyup = function () {
      textarea.style.height = "";
      textarea.style.height = `${Math.max(
        textarea.scrollHeight,
        parseInt(heightLimit)
      )}px`;
    };
  });

  // unfollow button hover design
  try {
    const following_button = document.querySelector("#following_button");
    following_button.onmouseover = function () {
      change_button("unfollow");
    };
    following_button.onmouseout = function () {
      change_button("following");
    };
  } catch (e) {
    console.log("following button being hidden");
  }

  // toggling popover
  $("[data-bs-toggle=tooltip]").tooltip();

  // Editing Post
  document.querySelectorAll(".edit_post").forEach((button) => {
    button.onclick = () => {
      edit_post(button.dataset.post);
    };
  });

  // Save Post
  document.querySelectorAll(".save_post").forEach((button) => {
    button.onclick = () => {
      save_post(button);
    };
  });

  // Giving love
  document.querySelectorAll(".heart_icon").forEach((icon) => {
    icon.onclick = () => {
      love_post(icon.dataset.post, icon.dataset.action);
    };
  });
});

function change_button(action) {
  const button = document.querySelector("#following_button");
  if (action === "unfollow") {
    button.style.backgroundColor = "brown";
    button.innerHTML = "Unfollow";
    button.style.transition = "background 1s";
  } else {
    button.style.backgroundColor = "blue";
    button.innerHTML = "Following";
  }
}

function edit_post(post_id) {
  const post = document.querySelector(`#post${post_id}`);
  const message = document.querySelector(`#post${post_id} p`).innerText;
  const edit_form = document.querySelector(`#edit_form${post_id}`);
  const textarea = document.querySelector(`#edit_form${post_id} textarea`);
  const save = document.querySelector(`#edit_form${post_id} .save`);
  const back = document.querySelector(`#edit_form${post_id} .back`);

  post.style.display = "none";
  edit_form.style.display = "block";
  textarea.value = message;

  save.onclick = () => {
    post.style.display = "block";
    edit_form.style.display = "none";
    document.querySelector(`#post${post_id} p`).innerText = textarea.value;

    fetch(`/edit/${post_id}`, {
      method: "PUT",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: textarea.value,
      }),
    });
  };
  back.onclick = () => {
    post.style.display = "block";
    edit_form.style.display = "none";
  };
}

function save_post(button) {
  post_id = button.dataset.post;
  const status = document.querySelector(`#save_status${post_id}`);

  if (button.dataset.action === "save") {
    fetch(`/save/post/${post_id}`);
    status.innerHTML = "Unsave";
    button.setAttribute("data-action", "unsave");
  } else {
    fetch(`/unsave/post/${post_id}`);
    if (button.dataset.reload === "True") {
      window.location.reload();
    } else {
      status.innerHTML = "Save";
      button.setAttribute("data-action", "save");
    }
  }
}

function love_post(post_id, action) {
  fetch(`/love/${post_id}?action=${action}`)
    .then((response) => response.text())
    .then((love_count) => {
      const original_love_count = document.querySelector(
        `#love_count${post_id}`
      );
      const empty_heart = document.querySelector(`#empty_heart${post_id}`);
      const heart = document.querySelector(`#heart${post_id}`);

      if (action === "love") {
        original_love_count.style.visibility = "visible";
        original_love_count.innerText = love_count;
        empty_heart.style.display = "none";
        heart.style.display = "block";
      } else {
        original_love_count.innerText = love_count;
        if (original_love_count.innerText === "0") {
          original_love_count.style.visibility = "hidden";
        }
        empty_heart.style.display = "block";
        heart.style.display = "none";
      }
    });
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
