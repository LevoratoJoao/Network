// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelector('#profile').addEventListener('click', () => load_profile(document.querySelector('#profile').textContent));
// });

// function load_profile(profile) {
//     document.querySelector('.posts').style.display = 'none';
//     document.querySelector('#profile-page').style.display = 'block';

//     fetch(`/profile/${profile}`)
// 	.then(response => response.json())
// 	.then(posts => {
//         console.log(posts)
//     });
// }

function editHandler(id) {
    if (document.querySelector(`#edit_post_${id}`).value == "") {
        const errorMessage = document.createElement('p');
        errorMessage.innerHTML = "You can't post an empty post!";
        console.log(errorMessage)
        document.querySelector('.modal-body').appendChild(errorMessage);
        return;
    }
    fetch(`/edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: document.querySelector(`#edit_post_${id}`).value
        })
    })
    .then((response) => response.json())
    .then(post => {
        console.log(post);
        $(`#editModal_${id}`).modal('hide')
        document.querySelector(`#post_${id}_content`).textContent = post.data.content;
    });
}

function likeHandler(id, liked) {
    fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: liked
        })
    })
    .then((response) => response.json())
    .then(post => {
        console.log(post);
        document.querySelector(`#post_${id}_likes`).textContent = `Likes: ${post.data.likes}`;
    });
}

function followHandler(profile_name) {
    fetch(`/follow/${profile_name}`, {
        method: 'POST',
        body: JSON.stringify({
            username: profile_name
        })
    })
    .then((response) => response.json())
    .then(follow => {
        console.log(follow);
    })
}

function unfollowHandler(profile_name) {
    fetch(`/unfollow/${profile_name}`, {
        method: 'POST',
        body: JSON.stringify({
            username: profile_name
        })
    })
    .then((response) => response.json())
    .then(follow => {
        console.log(follow);
    })
}