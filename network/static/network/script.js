document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#profile').addEventListener('click', () => load_profile(document.querySelector('#profile').textContent));
});

function load_profile(profile) {
    document.querySelector('.posts').style.display = 'none';
    document.querySelector('#profile-page').style.display = 'block';

    fetch(`/profile/${profile}`)
	.then(response => response.json())
	.then(posts => {
        console.log(posts)
    });
}