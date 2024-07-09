const NBBox = document.getElementById('NB');
NBBox.textContent =
  'This currently defaults to Covent Garden pending inclusion of geolocation code';

const NBBoxHeader = document.getElementById('NBHeader');
NBBoxHeader.innerHTML = '<h2>To Note</h2>';

const placesBox = document.getElementById('places-box');
const spinnerBox = document.getElementById('spinner-box');
const loadBtn = document.getElementById('load-btn');
const endBox = document.getElementById('end-box');

const placeNoteForm = document.getElementById('place-note-form');
const place_name = document.getElementById('id_name');
const place_mynotes = document.getElementById('id_mynotes');

const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = window.location.href;
const alertBox = document.getElementById('alert-box');

//Standard code for getting the csrftoken as per https://docs.djangoproject.com/en/4.0/ref/csrf/
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
const csrftoken = getCookie('csrftoken');

const likeUnlikePosts = () => {
  const likeUnlikeForms = [
    ...document.getElementsByClassName('like-unlike-forms'),
  ];
  likeUnlikeForms.forEach((form) =>
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const clickedId = e.target.getAttribute('places-form-id');
      const clickedBtn = document.getElementById(`like-unlike-${clickedId}`);
      $.ajax({
        type: 'POST',
        url: '/ukheritage/make_favourite/',
        data: { csrfmiddlewaretoken: csrftoken, pk: clickedId },
        success: function (response) {
          clickedBtn.textContent = response.favourite
            ? `Remove from Favourites (${response.count})`
            : `Add to Favourites (${response.count})`;
        },
        error: function (error) {
          console.log(error);
        },
      });
    })
  );
};

let visible = 6;

const getData = () => {
  $.ajax({
    type: 'GET',
    url: `/ukheritage/get_myplaces/${visible}/`,
    success: function (response) {
      const myplaces = response.places;
      spinnerBox.classList.add('hidden');
      //console.log(buildings)
      myplaces.forEach((element) => {
        //Code for if bootstrap card boxes are not required
        //<tr><td>${Number((element.distance).toFixed(1))}</td><td>${element.listed_building}</td></tr>
        placesBox.innerHTML += `
                    <div class="card mb-2">
                        <div class="card-body">
                            <h5 class="card-title">id: ${element.id}</h5>
                            <p class="card-text">${element.name}</p>
                        </div>
    
                        <div class="card-footer">
                            <div class="row">
                                <div class="col-2"><a href="/ukheritage/myplace/${
                                  element.id
                                }" class="btn btn-primary">Listing Details</a></div>
                                <div class="col-2"><a href="/ukheritage/myplace/${
                                  element.id
                                }" class="btn btn-primary">Edit Note</a></div>
                                <div class="col-2"><a href="${
                                  element.hyperlink
                                }" class="btn btn-primary">Weblink</a></div>
                                <div class="col-2">
                                    <form class="like-unlike-forms" places-form-id="${
                                      element.id
                                    }">
                                    <button href="#" class="btn btn-primary" id="like-unlike-${
                                      element.id
                                    }">${
          element.favourite
            ? `Remove from Favourites (${element.count})`
            : `Add to Favourites (${element.count})`
        }</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
      });

      likeUnlikePosts();

      if (response.size === 0) {
        endBox.textContent = 'No places added yet....';
      } else if (response.size <= visible) {
        loadBtn.classList.add('not-visible');
        endBox.textContent = 'No more places to load';
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
};

loadBtn.addEventListener('click', () => {
  spinnerBox.classList.remove('hidden');
  visible += 6;
  getData();
});

placeNoteForm.addEventListener('submit', (e) => {
  e.preventDefault(); //Stops the default form submission as ajax/Django will handle this

  $.ajax({
    type: 'POST',
    url: '', // Blank because we are reusing the current page url
    data: {
      csrfmiddlewaretoken: csrf[0].value,
      name: place_name.value,
      mynotes: place_mynotes.value,
    },
    success: function (response) {
      placesBox.insertAdjacentHTML(
        'afterbegin',
        `
                <div class="card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">id: ${response.id}</h5>
                        <p class="card-text">${response.name}</p>
                    </div>

                    <div class="card-footer">
                        <div class="row">
                            <div class="col-2"><a href="/ukheritage/myplace/${response.id}" class="btn btn-primary">Listing Details</a></div>
                            <div class="col-2"><a href="/ukheritage/myplace/${response.id}" class="btn btn-primary">Edit Note</a></div>
                            <div class="col-2"><a href="${response.name}" class="btn btn-primary">Weblink</a></div>
                            <div class="col-2">
                                <form class="like-unlike-forms" places-form-id="${response.id}">
                                <button href="#" class="btn btn-primary" id="like-unlike-${response.id}">Add to Favourites</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            `
      );
      likeUnlikePosts();
      $('#addNoteModal').modal('hide');
      handleAlerts('success', 'New MyPlace Added');
      placeNoteForm.reset();
    },
    error: function (error) {
      handleAlerts('danger', 'An error occurred');
    },
  });
});

//initial run of getData
getData();
